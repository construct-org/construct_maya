# -*- coding: utf-8 -*-
from __future__ import absolute_import


def get_maya_window():
    '''Get Maya MainWindow as a QWidget.'''
    from Qt import QtWidgets

    for widget in QtWidgets.QApplication.instance().topLevelWidgets():
        if widget.objectName() == 'MayaWindow':
            return widget
    raise RuntimeError('Could not locate MayaWindow...')


def get_maya_menu_bar():
    '''Get Maya's menubar as a real QMenuBar'''

    from Qt import QtWidgets
    try:
        from shiboken import wrapInstance, getCppPointer
    except ImportError:
        from shiboken2 import wrapInstance, getCppPointer
    maya_window = get_maya_window()
    menubar_widget = maya_window.layout().menuBar()

    pointer = long(getCppPointer(menubar_widget)[0])
    qmenubar = wrapInstance(pointer, QtWidgets.QMenuBar)
    return qmenubar
