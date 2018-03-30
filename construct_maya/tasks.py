# -*- coding: utf-8 -*-
from __future__ import absolute_import

__all__ = [
    'setup_construct_maya',
]

import os
from construct.tasks import (
    task,
    requires,
    success,
    params,
    store
)


@task
@requires(success('build_app_env'))
@params(store('app'))
def setup_construct_maya(app):

    userSetup = os.path.join(os.path.dirname(__file__), 'userSetup')
    scpath = os.pathsep.join([
        userSetup,
        app.env.get('MAYA_SCRIPT_PATH', '')
    ])
    pypath = os.pathsep.join([
        userSetup,
        app.env.get('PYTHONPATH', ''),
        os.path.join(os.path.dirname(__file__), '..')
    ])

    app.env['MAYA_SCRIPT_PATH'] = scpath
    app.env['PYTHONPATH'] = pypath
