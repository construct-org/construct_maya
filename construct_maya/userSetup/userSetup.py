# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
import logging
import construct
from Qt import QtWidgets
from functools import partial
from maya.utils import executeDeferred
from construct_maya import callbacks, menus
from construct_ui import resources

_log = logging.getLogger('construct.maya.userSetup')
construct_menu = None


def setup():
    _log.debug('Configuring Construct for Maya!')
    construct.init()
    resources.init()

    ctx = construct.get_context()
    host = construct.get_host()
    if ctx.workspace:
        _log.debug('Setting workspace to ' + ctx.workspace.path)
        host.set_workspace(ctx.workspace.path)

    _log.debug('Registering callbacks...')
    callbacks.register()

    _log.debug('Creating Construct menu...')
    menus.setup_construct_menu()

    if ctx.workspace and not host.get_filename():
        if ctx.workspace.get_work_files():
            action_identifier = 'file.open'
        else:
            action_identifier = 'file.save'

        construct.show_form(action_identifier)


executeDeferred(setup)
