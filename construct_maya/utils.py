# -*- coding: utf-8 -*-
from __future__ import absolute_import
import logging


_log = logging.getLogger('construct.maya.utils')


def remove_unknown_plugin_nodes(plugin):
    '''Remove unknown nodes provided by a plugin'''

    from maya import cmds

    nodes = cmds.ls(type='unknown')
    for node in nodes:
        provider = cmds.unknownNode(node, query=True, plugin=True)
        if plugin == provider:
            _log.debug('Deleting unknownNode %s' % node)
            cmds.lockNode(node, lock=False)
            cmds.delete(node)

    cmds.flushUndo()


def remove_plugin_nodes(plugin):
    '''Danger...deletes all nodes provided by a plugin and flushes
    your undo queue.'''

    from maya import cmds

    try:
        types = cmds.pluginInfo(plugin, query=True, dependNode=True)
    except RuntimeError:
        return

    for type in types:
        nodes = cmds.ls(type=type, recursive=True)
        for node in nodes:
            _log.debug('Deleting node %s' % node)
            cmds.lockNode(node, lock=False)
            cmds.delete(node)

    cmds.flushUndo()


def remove_unknown_plugins():
    '''Danger...Forcefully removes all unknown plugins from your scene'''

    from maya import cmds

    unknown_plugins = cmds.unknownPlugin(query=True, list=True)
    if not unknown_plugins:
        _log.debug('No unknown plugins found.')
        return

    for plugin in unknown_plugins:
        _log.debug('Removing unknown plugin %s.' % plugin)
        remove_plugin_nodes(plugin)
        remove_unknown_plugin_nodes(plugin)
        cmds.unknownPlugin(plugin, remove=True)
