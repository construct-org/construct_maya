# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
import inspect
__file__ = inspect.stack()[0][1]


print('[construct] Initializing construct_maya...')
import construct
import construct_maya as cmaya
construct.init()

ctx = construct.get_context()
if 'workspace' in ctx:
    print('[construct] Setting workspace...')

    cmaya.set_workspace(ctx.workspace.path)
