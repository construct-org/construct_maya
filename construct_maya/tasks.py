# -*- coding: utf-8 -*-
from __future__ import absolute_import

__all__ = [
    'setup_construct_maya',
]

import os
from construct.tasks import (
    task,
    pass_kwargs,
    pass_context,
    returns,
    artifact,
    store,
    params,
    success,
    requires,
)
from construct import types, get_host, utils
from construct_launcher.constants import BEFORE_LAUNCH


# Before launch task

@task(priority=BEFORE_LAUNCH)
@requires(success('build_app_env'))
@params(store('app'))
def setup_construct_maya(app):
    '''Setup Maya environment.'''

    userSetup = os.path.join(os.path.dirname(__file__), 'userSetup')
    scpath = os.pathsep.join([
        userSetup,
        app.env.get('MAYA_SCRIPT_PATH', '')
    ])
    pypath = os.pathsep.join([
        userSetup,
        app.env.get('PYTHONPATH', ''),
        os.path.join(os.path.dirname(__file__), '..')
    ])

    app.env['MAYA_SCRIPT_PATH'] = scpath
    app.env['PYTHONPATH'] = pypath


# Publish Tasks

@task(priority=types.VALIDATE)
@requires(success('ensure_saved'))
def flatten_references():
    '''Flatten references in published scene file.'''
    from maya import cmds

    refs = sorted(cmds.ls(references=True))

    if not refs:
        return

    namespaces = []
    for ref in refs:
        valid = validate_ref(ref)
        if not valid:
            continue

        ref_path = cmds.referenceQuery(ref, f=True)
        is_loaded = cmds.referenceQuery(ref, isLoaded=True)
        namespace = cmds.referenceQuery(ref, namespace=True)

        if not is_loaded:
            cmds.file(ref_path, loadReference=True)
            cmds.file(ref_path, removeReference=True)
        else:
            cmds.file(ref_path, importReference=True)
            namespaces.append(namespace)

    for namespace in namespaces:
        if namespace == ':':
            continue
        cmds.namespace(mv=(namespace, ':'), f=1)
        cmds.namespace(rm=namespace)

    flatten_references()


def validate_ref(ref):
    '''Sometimes references can be "empty" - not actually referencing a file
    path. This method checks for that case and deletes the reference if
    it is invalid.
    '''
    from maya import cmds

    try:
        return not cmds.referenceQuery(ref, rfn=True, parent=True)
    except:
        cmds.lockNode(ref, lock=False)
        cmds.delete(ref)
    return False
