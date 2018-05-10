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
        action = construct.actions.get('file.open')
        parent = host.get_qt_parent()
        form_cls = construct.get_form(action.identifier)
        form = form_cls(action, ctx, parent)
        form.setStyleSheet(resources.style('dark'))
        form.show()


executeDeferred(setup)
