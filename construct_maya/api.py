# -*- coding: utf-8 -*-
import os


def save_file(file):
    from maya import cmds

    cmds.file(rename=file)
    cmds.file(save=True)


def open_file(file):
    from maya import cmds

    cmds.file(file, open=True)


def active_selection():
    return cmds.ls(sl=True, long=True)


def set_workspace(directory):
    from maya import cmds

    cmds.workspace(directory, openWorkspace=True)


def get_filepath():
    from maya import cmds

    return cmds.file(q=True, sceneName=True)


def get_frame_range():
    from maya import cmds

    return [
        cmds.playbackOptions(q=True, minTime=True),
        cmds.playbackOptions(q=True, maxTime=True)
    ]


def set_frame_range(start_frame, end_frame):
    from maya import cmds

    cmds.playbackOptions(minTime=start_frame, maxTime=end_frame)
