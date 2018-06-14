# -*- coding: utf-8 -*-
from __future__ import absolute_import

__all__ = ['Maya']

from os.path import join, dirname, basename
from construct.extension import HostExtension
from construct_maya.tasks import (
    setup_construct_maya
)
from construct_launcher.constants import BEFORE_LAUNCH


class Maya(HostExtension):
    '''Construct Autodesk Maya integration'''

    name = 'Maya'
    attr_name = 'maya'

    def available(self, ctx):
        return True

    def load(self):
        self.add_template_path(join(dirname(__file__), 'templates'))
        self.add_task(
            'launch.maya*',
            setup_construct_maya,
            priority=BEFORE_LAUNCH
        )

    def modified(self):
        from maya import cmds

        return (
            cmds.file(query=True, modified=True) and
            self.get_filename()
        )

    def save_file(self, file):
        from maya import cmds

        cmds.file(rename=file)
        cmds.file(save=True)

    def open_file(self, file):
        from maya import cmds
        from construct_ui.dialogs import ask

        if self.modified():
            if ask('Would you like to save?', title='Unsaved changes'):
                cmds.file(save=True, force=True)

        cmds.file(new=True, force=True)
        cmds.file(file, open=True, ignoreVersion=True)

    def get_selection(self):
        from maya import cmds

        return cmds.ls(selection=True, long=True)

    def set_selection(self, selection):
        from maya import cmds

        cmds.select(selection, replace=True)

    def get_workspace(self):
        from maya import cmds
        return cmds.workspace(query=True, openWorkspace=True)

    def set_workspace(self, directory):
        from maya import cmds

        cmds.workspace(directory, openWorkspace=True)

    def get_filepath(self):
        from maya import cmds

        return cmds.file(query=True, sceneName=True)

    def get_filename(self):
        from maya import cmds

        return basename(cmds.file(query=True, sceneName=True))

    def get_frame_range(self):
        from maya import cmds

        return [
            cmds.playbackOptions(query=True, minTime=True),
            cmds.playbackOptions(query=True, maxTime=True)
        ]

    def set_frame_range(self, start_frame, end_frame):
        from maya import cmds

        cmds.playbackOptions(minTime=start_frame, maxTime=end_frame)

    def get_qt_parent(self):
        from Qt import QtWidgets
        app = QtWidgets.QApplication.instance()

        for widget in app.topLevelWidgets():
            if widget.objectName() == 'MayaWindow':
                return widget
