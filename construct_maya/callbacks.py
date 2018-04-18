# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
import logging
import construct
from construct_maya import api


_log = logging.getLogger('construct.maya.callbacks')
_callback_ids = []


def after_open(*args):
    '''kAfterOpen callback'''

    _log.debug('after_open')
    set_context_to_maya_scene()
    # TODO:


def after_save(*args):
    '''kAfterSave callback'''

    _log.debug('after_open')
    set_context_to_maya_scene()


def before_create_reference():
    # TODO: Implement kBeforeCreateReference callback
    #       Ensure references are up to date
    _log.debug('before_create_reference')


def set_context_to_maya_scene():
    '''Sets context to the currently open Maya scene.'''

    full_path = api.get_filepath()
    path = os.path.dirname(full_path)

    new_ctx = construct.Context.from_path(path)
    if new_ctx.workspace:
        _log.debug('Setting context to %s' % path)
        construct.set_context(new_ctx)
    else:
        _log.debug(
            'Not setting context. '
            'Script is not in a construct workspace...'
        )

    # Look for a workspace.mel
    for _ in range(5):
        if os.path.isfile(path + '/workspace.mel'):
            _log.debug('Setting Maya workspace %s' % path)
            api.set_workspace(path)
            break
        path = os.path.dirname(path)


def register():
    '''Register scene callbacks'''

    from maya.api import OpenMaya

    after_open_id = OpenMaya.MSceneMessage.addCallback(
        OpenMaya.MSceneMessage.kAfterOpen,
        after_open
    )
    _callback_ids.append(after_open_id)

    after_save_id = OpenMaya.MSceneMessage.addCallback(
        OpenMaya.MSceneMessage.kAfterSave,
        after_save
    )
    _callback_ids.append(after_save_id)

    before_create_reference_id = OpenMaya.MSceneMessage.addCallback(
        OpenMaya.MSceneMessage.kBeforeCreateReference,
        before_create_reference
    )
    _callback_ids.append(before_create_reference_id)


def unregister():
    '''Unregister scene callbacks'''

    from maya.api import OpenMaya

    while _callback_ids:
        _id = _callback_ids.pop()
        OpenMaya.MMessage.removeCallback(_id)
