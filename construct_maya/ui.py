# -*- coding: utf-8 -*-
from __future__ import absolute_import
from Qt import QtWidgets


class ContextualMenu(QtWidgets.QMenu):
    # TODO: Implement drop down menu generated from current context
    #       Organize by action dotted path
    #        __________
    #       |construct|  _______
    #       |     file|>|  open|  - file.open
    #       |  publish| |  save|  - file.save
    #       |_________| |______|
