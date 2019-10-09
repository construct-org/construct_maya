# -*- coding: utf-8 -*-
from __future__ import absolute_import
from functools import wraps
from construct_maya import utils


class ConstructMenu(object):
    '''
    Stores Menu QObject and Partial callback to ensure they are
    not garbage collected.
    '''
    name = 'ConstructMenu'
    qmenu = None
    show_menu = None

    @classmethod
    def setup(cls):
        '''Setup Construct Action Menu'''
        from Qt import QtWidgets
        from maya import OpenMayaUI
        from maya import cmds
        from functools import partial
        from construct_ui.menus import create_action_menu
        try:
            from shiboken import wrapInstance
        except ImportError:
            from shiboken2 import wrapInstance

        cmds.menu(cls.name, label='Construct', parent='MayaWindow')

        pointer = OpenMayaUI.MQtUtil.findControl(cls.name)
        cls.qmenu = wrapInstance(long(pointer), QtWidgets.QMenu)
        cls.show = partial(create_action_menu, parent=cls.qmenu)
        cls.qmenu.aboutToShow.connect(cls.show)
