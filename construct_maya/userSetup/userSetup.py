# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
import logging
import construct
from Qt import QtWidgets
from functools import partial
from maya.utils import executeDeferred
from construct_maya import api, callbacks, ui

_log = logging.getLogger('construct.maya.userSetup')
construct_menu = None


def setup():
    _log.debug('Configuring Construct for Maya!')
    construct.init()

    ctx = construct.get_context()
    if ctx.workspace:
        _log.debug('Setting workspace to ' + ctx.workspace.path)
        api.set_workspace(ctx.workspace.path)

    _log.debug('Registering callbacks...')
    callbacks.register()

    _log.debug('Creating Construct menu...')
    ui.setup_construct_menu()


executeDeferred(setup)
