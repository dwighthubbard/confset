#!/usr/bin/env python
"""
Manage package settings
"""
import os
import shutil
import time
import logging

CONF_PATH = ['/etc/default', '/etc/sysconfig']


class ConfigSettings(object):
    """
    Configuration settings class
    :param conffile:
    """

    def __init__(self, conffile):
        self.conffile = conffile
        self.filename = self.search_for_conf(conffile)
        self.settings, self.order = self.available_settings()
        self.__dict__.update(self.settings)

    def search_for_conf(self, conffile):
        """
        Search for a configuration file
        :return:
        """
        global CONF_PATH
        filename = None
        for d in CONF_PATH:
            filename = os.path.join(d, conffile)
            if os.path.isfile(filename):
                break
            else:
                filename = None
        return filename

    def available_settings(self):
        """
        Return the settings available in a conf file

        :return:
        """
        comments = []
        order = []
        settings = {}
        if self.filename:
            fh = open(self.filename, 'r')
            for line in fh.readlines():
                line = line.strip()
                if line:
                    if line.startswith('#'):
                        temp = line.strip('#').strip()
                        if temp:
                            comments.append(temp)
                    else:
                        if '=' in line:
                            setting = '%s.%s' % (self.conffile, line.split('=')[0])
                            settings[setting] = {'help': comments, 'value': '='.join(line.split('=')[1:]).strip()}
                            comments = []
                            order.append(setting)
                else:
                    comments = []
        return settings, order

    def print_settings(self, setting_filter=None, sort=False):
        """
        Print the current settings
        :param setting_filter:
        :param sort:
        """
        if sort:
            temp = self.settings.keys()
            temp.sort()
        else:
            temp = self.order
        max_len = 0
        for setting in temp:
            if len(setting) + len(self.settings[setting]['value']) + 1 > max_len:
                max_len = len(setting) + len(self.settings[setting]['value']) + 1
        for setting in temp:
            if not setting_filter or setting == setting_filter:
                setting_and_value = '%s=%s' % (setting, self.settings[setting]['value'])
                print(
                    '%s - %s' % (
                        setting_and_value.ljust(max_len, ' '),
                        self.settings[setting]['help'][0] if self.settings[setting]['help'] else ''
                    )
                )
                for line in self.settings[setting]['help'][1:]:
                    print('%s   %s' % ((' ' * max_len), line))

    def set(self, key, value):
        """
        Set a setting in a conf file
        :param key:
        :param value:
        """
        shutil.copy(self.filename, '%s.confset.%s' % (self.filename, time.strftime("%Y%m%d%H%M%S")))
        data = open(self.filename, 'r').readlines()
        changed = False
        fh = open(self.filename, 'w')
        for line in data:
            if not line.strip().startswith('#') and '=' in line:
                tkey = line.strip().split('=')[0].strip()
                tvalue = line.strip().split('=')[1].strip()
                if key == tkey:
                    line = '%s=%s\n' % (key, value)
                    changed = True
            fh.write(line)
        if not changed:
            fh.write('%s=%s\n' % (key, value))
        fh.close()
