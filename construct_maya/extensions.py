# -*- coding: utf-8 -*-
from __future__ import absolute_import

__all__ = ['Maya']

from os.path import join, dirname, basename, splitext
from construct.extension import HostExtension
from construct_maya import tasks


FILE_TYPE_MAP = {
    '.ma': 'mayaAscii',
    '.mb': 'mayaBinary',
    '.mel': 'mel',
    '.obj': 'OBJ',
    '.wav': 'audio',
    '.aif': 'audio',
    '.ai': 'Adobe(R) Illustrator(R)',
    '.eps': 'EPS',
    '.png': 'image',
    '.jpeg': 'image',
    '.jpg': 'image',
    '.exr': 'image',
    '.iff': 'image',
    '.tiff': 'image',
}


class Maya(HostExtension):
    '''Construct Autodesk Maya integration'''

    name = 'maya'
    attr_name = 'maya'

    def available(self, ctx):
        return True

    def load(self):
        self.add_template_path(join(dirname(__file__), 'templates'))
        self.add_task('launch.maya*', tasks.setup_construct_maya)
        self.add_task('publish', tasks.flatten_references)

    def modified(self):
        from maya import cmds

        return (
            cmds.file(query=True, modified=True) and
            self.get_filename()
        )

    def save_file(self, file):
        from maya import cmds

        cmds.file(rename=file)
        ext = splitext(file)[-1]
        cmds.file(save=True, type=FILE_TYPE_MAP[ext])

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

    def get_frame_rate(self):
        from maya import cmds

        unit = cmds.currentUnit(query=True, time=True)
        fps = {
            'game': '15fps',
            'film': '24fps',
            'pal': '25fps',
            'ntsc': '30fps',
            'show': '48fps',
            'palf': '50fps',
            'ntscf': '60fps',
        }.get(unit, unit)
        return float(fps.rstrip('fps'))

    def set_frame_rate(self, fps):
        from maya import cmds

        whole, decimal = str(float(fps)).split('.')
        if int(decimal) == 0:
            fps = whole + 'fps'
        else:
            fps = str(fps) + 'fps'
        unit = {
            'game': '15fps',
            'film': '24fps',
            'pal': '25fps',
            'ntsc': '30fps',
            'show': '48fps',
            'palf': '50fps',
            'ntscf': '60fps',
        }.get(fps, fps)
        cmds.currentUnit(time=unit)

    def get_frame_range(self):
        from maya import cmds

        return [
            cmds.playbackOptions(query=True, animationStartTime=True),
            cmds.playbackOptions(query=True, minTime=True),
            cmds.playbackOptions(query=True, maxTime=True),
            cmds.playbackOptions(query=True, animationEndTime=True),
        ]

    def set_frame_range(self, min, start, end, max):
        from maya import cmds

        cmds.playbackOptions(
            animationStartTime=min,
            minTime=start,
            maxTime=end,
            animationEndTime=max,
        )

    def get_qt_parent(self):
        from Qt import QtWidgets
        app = QtWidgets.QApplication.instance()

        for widget in app.topLevelWidgets():
            if widget.objectName() == 'MayaWindow':
                return widget
