# Copyright (c) 2015, Dwight Hubbard
# Copyrights licensed under the Apache 2.0 License
# See the accompanying LICENSE.txt file for terms.
"""
----------------------------------

Tests for `redislite` module.
"""
from __future__ import print_function
import confset
import logging
import os
import shutil
import tempfile
import unittest


# noinspection PyPep8Naming
class TestConfset(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        self.config_file = 'testconf'
        self.config_file_full = os.path.join(self.tempdir, self.config_file)
        confset.CONF_PATH.append(self.tempdir)

    def tearDown(self):
        if os.path.exists(self.tempdir):
            shutil.rmtree(self.tempdir)
        confset.CONF_PATH.remove(self.tempdir)
        self.tempdir = None

    def test_config_create(self):
        self.assertFalse(os.path.exists(self.config_file_full))
        config = confset.ConfigSettings(self.config_file)
        self.assertFalse(os.path.exists(self.config_file_full))
        config.set('test', 'value', help_text='Helpful comment')
        self.assertTrue(os.path.exists(self.config_file_full))

    def test_config_create_setting(self):
        self.assertFalse(os.path.exists(self.config_file_full))

        # Set a value in the new config file
        config = confset.ConfigSettings(self.config_file)
        config.set('test', 'value', help_text='Helpful comment')

        # New config file exists
        self.assertTrue(os.path.exists(self.config_file_full))

        # new config contents are correct
        with open(self.config_file_full) as file_handle:
            result = file_handle.read()
            print(result)
            self.assertIn('test=value', result, "Config setting is missing")
            self.assertIn('# Helpful comment', result, "Help comment missing")

    def test_config_create_setting_multiline_help(self):
        self.assertFalse(os.path.exists(self.config_file_full))

        # Set a value in the new config file
        config = confset.ConfigSettings(self.config_file)
        config.set('test', 'value', help_text=['Really long', 'Helpful comment'])

        # New config file exists
        self.assertTrue(os.path.exists(self.config_file_full))

        # new config contents are correct
        with open(self.config_file_full) as file_handle:
            result = file_handle.read()
            print(result)
            self.assertIn('test=value', result, "Config setting is missing")
            self.assertIn('# Really long\n# Helpful comment', result, "Help comment missing")

    def test_config_update_setting(self):
        self.test_config_create_setting()
        config = confset.ConfigSettings(self.config_file)
        print(config.available_settings())
        config.set('test2', 'test2', help_text=['Multi line', 'help text'])
        config.set('test', 'valuenew', help_text='New Helpful comment')
        with open(self.config_file_full) as file_handle:
            result = file_handle.read()
            print(result)
            self.assertNotIn('test=value\n', result, "Old config setting still in config file")
            self.assertIn('test=valuenew', result, "Config setting is missing")
            self.assertIn('# New Helpful comment', result, "Help comment missing")
            self.assertIn('test2=test2', result, "Second setting missing")


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()