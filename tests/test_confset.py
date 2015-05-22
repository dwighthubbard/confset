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
        config.set('test', 'value', help='Helpful comment')
        self.assertTrue(os.path.exists(self.config_file_full))

    def test_config_create_setting(self):
        self.assertFalse(os.path.exists(self.config_file_full))

        # Set a value in the new config file
        config = confset.ConfigSettings(self.config_file)
        config.set('test', 'value', help='Helpful comment')

        # New config file exists
        self.assertTrue(os.path.exists(self.config_file_full))

        # new config contents are correct
        with open(self.config_file_full) as file_handle:
            result = file_handle.read()
            print(result)
            self.assertIn('test=value', result, "Config setting is missing")
            self.assertIn('# Helpful comment', result, "Help comment missing")


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()