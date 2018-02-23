# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

__title__ = 'construct_maya'
__description__ = 'Construct Maya Actions'
__version__ = '0.0.1'
__author__ = 'Dan Bradham'
__email__ = 'danielbradham@gmail.com'
__license__ = 'No License'
__url__ = 'https://github.com/construct-org/construct_maya'

from construct_maya import tasks
from construct_maya.api import *


def available(ctx):
    return True


def register(cons):

    ctx = cons.get_context()

    cons.action_hub.connect('launch.maya*', tasks.setup_construct_maya)

    if ctx.host == 'maya':
        # Tasks available only from within maya
        pass

def unregister(cons):
    ctx = cons.get_context()

    cons.action_hub.disconnect('launch.maya*', tasks.setup_construct_maya)

    if ctx.host == 'maya':
        # Tasks available only from within maya
        pass
