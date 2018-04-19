# -*- coding: utf-8 -*-
from __future__ import absolute_import
from functools import wraps


def get_maya_window(widget_cls=None):
    '''Get Maya MainWindow as a QWidget.'''
    from Qt import QtWidgets
    try:
        from shiboken import wrapInstance, getCppPointer
    except ImportError:
        from shiboken2 import wrapInstance, getCppPointer

    for widget in QtWidgets.QApplication.instance().topLevelWidgets():
        if widget.objectName() == 'MayaWindow':

            if not widget_cls or widget_cls == QtWidgets.QWidget:
                return widget

            pointer = long(getCppPointer(widget)[0])
            return wrapInstance(pointer, widget_cls)

    raise RuntimeError('Could not locate MayaWindow...')


def get_maya_menu_bar():
    '''Get Maya's menubar as a real QMenuBar'''
    from Qt import QtWidgets

    window = get_maya_window(QtWidgets.QMainWindow)
    return window.menuBar()


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
