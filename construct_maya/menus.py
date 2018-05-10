# -*- coding: utf-8 -*-
from __future__ import absolute_import
from functools import wraps
from construct_maya import utils


def setup_construct_menu():
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

    name = 'ConstructMenu'
    cmds.menu(name, label='Construct', parent='MayaWindow')

    pointer = OpenMayaUI.MQtUtil.findControl(name)
    menu = wrapInstance(long(pointer), QtWidgets.QMenu)
    menu.aboutToShow.connect(partial(create_action_menu, parent=menu))
