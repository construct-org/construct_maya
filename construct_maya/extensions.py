# -*- coding: utf-8 -*-
from __future__ import absolute_import

__all__ = ['Maya']

from os.path import join, dirname
from construct.extension import Extension
from construct_maya.tasks import (
    setup_construct_maya
)


class Maya(Extension):
    '''Construct Autodesk Maya integration'''

    name = 'Maya'
    attr_name = 'maya'

    def available(self, ctx):
        return True

    def load(self):

        self.add_template_path(join(dirname(__file__), 'templates'))

        # Extend cpenv_launcher to activate cpenv modules before launch
        from construct_launcher.constants import BEFORE_LAUNCH

        self.add_task(
            'launch.maya*',
            setup_construct_maya,
            priority=BEFORE_LAUNCH
        )
