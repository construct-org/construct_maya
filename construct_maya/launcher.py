# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

__all__ = [
    'setup_construct_maya',
    'register',
    'unregister',
]

import os
import subprocess
from construct_launcher import BEFORE_LAUNCH
from construct import (
    context,
    to_env_dict,
    task,
    requires,
    success,
    params,
    store,
    returns
)


@task(priority=BEFORE_LAUNCH)
@requires(success('build_app_env'))
@params(store('app'))
@returns(store('app'))
def setup_construct_maya(app):

    userSetup = os.path.join(os.path.dirname(__file__), 'userSetup')
    scpath = os.pathsep.join([
        userSetup,
        app['env'].get('MAYA_SCRIPT_PATH', '')
    ])
    pypath = os.pathsep.join([
        userSetup,
        app['env'].get('PYTHONPATH', ''),
        os.path.join(os.path.dirname(__file__), '..')
    ])
    app['env']['MAYA_SCRIPT_PATH'] = scpath
    app['env']['PYTHONPATH'] = pypath
    return app


def register(cons):

    cons.action_hub.connect('launch.maya*', setup_construct_maya)


def unregister(cons):

    cons.action_hub.disconnect('launch.maya*', setup_construct_maya)
