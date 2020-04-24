# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
import os
import re
import logging
import construct
from construct.utils import unipath
from construct_ui import dialogs
import glob


_log = logging.getLogger('construct.maya.callbacks')
_callback_ids = []


def after_open(*args):
    '''kAfterOpen callback'''

    _log.debug('after_open')
    set_context_to_maya_scene()


def after_save(*args):
    '''kAfterSave callback'''

    _log.debug('after_open')
    set_context_to_maya_scene()


def before_create_reference_check(mfile, client_data):
    _log.debug('before_create_reference_check')

    reference = unipath(mfile.expandedFullName())
    reference_name = os.path.basename(reference)
    latest = get_latest_version(reference)
    latest_name = os.path.basename(latest)
    if reference != latest:
        update = dialogs.ask(
            'A newer version is available, would you like to update?',
            latest_name,
            title='Referencing ' + reference_name + '...'
        )
        if update:
            mfile.setRawFullName(latest)

    return True


def rreplace(string, search, repl, count=1):
    modified = string[::-1].replace(search[::-1], repl[::-1], count)
    return modified[::-1]


def get_latest_version(filepath):
    '''Returns latest version, or the original file if it is not versioned'''

    root = os.path.dirname(filepath)

    # Check if this is a versioned file.
    versions = re.findall(r'\d+', filepath)
    if not versions:
        return filepath
    else:
        version = versions[-1]

    # Okay let's get the latest version
    name_pattern = rreplace(filepath, version, '*')
    path_pattern = unipath(root, name_pattern)
    versions = sorted(glob.glob(path_pattern))

    if not versions:
        return filepath

    return unipath(versions[-1])


def set_context_to_maya_scene():
    '''Sets context to the currently open Maya scene.'''

    host = construct.get_host()
    path = host.get_filepath()

    new_ctx = construct.Context.from_path(path)
    new_ctx.file = path

    if new_ctx.workspace:
        _log.debug('Setting context to %s' % path)
        construct.set_context(new_ctx)
        new_ctx.to_env()
    else:
        _log.debug(
            'Not setting context. '
            'Maya file is not in a construct workspace...'
        )

    # Look for a workspace.mel
    for _ in range(5):
        if os.path.isfile(path + '/workspace.mel'):
            _log.debug('Setting Maya workspace %s' % path)
            host.set_workspace(path)
            break
        path = os.path.dirname(path)


def register():
    '''Register scene callbacks'''

    from maya.api import OpenMaya
    MSceneMessage = OpenMaya.MSceneMessage

    after_open_id = MSceneMessage.addCallback(
        MSceneMessage.kAfterOpen,
        after_open
    )
    _callback_ids.append(after_open_id)

    after_save_id = MSceneMessage.addCallback(
        MSceneMessage.kAfterSave,
        after_save
    )
    _callback_ids.append(after_save_id)

    before_create_reference_check_id = MSceneMessage.addCheckFileCallback(
        MSceneMessage.kBeforeCreateReferenceCheck,
        before_create_reference_check
    )
    _callback_ids.append(before_create_reference_check_id)


def unregister():
    '''Unregister scene callbacks'''

    from maya.api import OpenMaya

    while _callback_ids:
        _id = _callback_ids.pop()
        OpenMaya.MMessage.removeCallback(_id)
