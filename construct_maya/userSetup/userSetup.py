# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
import logging
import construct
from maya.utils import executeDeferred
from construct_ui import ActionMenu
from construct_maya import api, callbacks
from construct_maya.ui import get_maya_menu_bar


def setup():
    _log = logging.getLogger('construct.maya.userSetup')
    _log.debug('Configuring Construct for Maya!')
    construct.init()

    ctx = construct.get_context()
    if ctx.workspace:
        _log.debug('Setting workspace to ' + ctx.workspace.path)
        api.set_workspace(ctx.workspace.path)

    _log.debug('Registering callbacks...')
    callbacks.register()

    _log.debug('Creating Construct menu...')
    menubar = get_maya_menu_bar()
    menubar.addMenu(ActionMenu('Construct', menubar))


executeDeferred(setup)
