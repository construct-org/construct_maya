# -*- coding: utf-8 -*-
from __future__ import absolute_import

__all__ = [
    'save_file',
    'open_file',
    'get_scene_selection',
    'set_scene_selection',
    'get_workspace',
    'set_workspace',
    'get_filepath',
    'get_filename',
    'get_frame_range',
    'set_frame_range',
]

import os


def save_file(file):
    from maya import cmds

    cmds.file(rename=file)
    cmds.file(save=True)


def open_file(file):
    from maya import cmds

    cmds.file(file, open=True)


def get_scene_selection():
    from maya import cmds

    return cmds.ls(sl=True, long=True)


def set_scene_selection(selection):
    from maya import cmds

    cmds.select(selection, replace=True)


def get_workspace():
    from maya import cmds
    return cmds.workspace(q=True, openWorkspace=True)


def set_workspace(directory):
    from maya import cmds

    cmds.workspace(directory, openWorkspace=True)


def get_filepath():
    from maya import cmds

    return cmds.file(q=True, sceneName=True)


def get_filename():
    from maya import cmds

    return os.path.basename(cmds.file(q=True, sceneName=True))


def get_frame_range():
    from maya import cmds

    return [
        cmds.playbackOptions(q=True, minTime=True),
        cmds.playbackOptions(q=True, maxTime=True)
    ]


def set_frame_range(start_frame, end_frame):
    from maya import cmds

    cmds.playbackOptions(minTime=start_frame, maxTime=end_frame)
