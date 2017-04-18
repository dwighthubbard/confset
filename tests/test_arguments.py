import logging
import os
import confset
import shutil
import tempfile
import unittest
from confset.arguments import ConfsetArguments, create_arg_parser
try:
    from unittest import mock
except:
    import mock


# noinspection PyPep8Naming
class TestConfsetArguments(unittest.TestCase):

    def setUp(self):
        self.parser = create_arg_parser()
        self.tempdir = tempfile.mkdtemp()
        self.config_file = 'testarg'
        self.config_file_full = os.path.join(self.tempdir, self.config_file)
        confset.CONF_PATH.append(self.tempdir)

    def tearDown(self):
        if os.path.exists(self.tempdir):
            shutil.rmtree(self.tempdir)
        confset.CONF_PATH.remove(self.tempdir)
        self.tempdir = None

    @mock.patch('confset.confset.ConfigSettings.print_settings')
    def test_get_conf_without_arguments(self, mock_print):
        cmd = ''
        (options, args) = self.parser.parse_args(cmd.split(' '))
        test_instance = ConfsetArguments(args, options)

        self.assertIsNone(test_instance.name)
        self.assertIsNone(test_instance.attr)
        self.assertIsNone(test_instance.value)
        self.assertFalse(test_instance.arg_options.info)
        self.assertEqual(test_instance.get_filters(), '')
        test_instance.execute()
        self.assertTrue(mock_print.called)

        cmd = '--info'
        (options, args) = self.parser.parse_args(cmd.split(' '))
        test_instance = ConfsetArguments(args, options)

        self.assertIsNone(test_instance.name)
        self.assertIsNone(test_instance.attr)
        self.assertIsNone(test_instance.value)
        self.assertTrue(test_instance.arg_options.info)
        self.assertEqual(test_instance.get_filters(), '')
        test_instance.execute()
        self.assertTrue(mock_print.called)

    @mock.patch('confset.confset.ConfigSettings.print_settings')
    def test_get_conf_with_name(self, mock_print):
        cmd = 'test_name'
        (options, args) = self.parser.parse_args(cmd.split(' '))
        test_instance = ConfsetArguments(args, options)

        self.assertEqual(test_instance.name, 'test_name')
        self.assertIsNone(test_instance.attr)
        self.assertIsNone(test_instance.value)
        self.assertFalse(test_instance.arg_options.info)
        self.assertEqual(test_instance.get_filters(), '')
        test_instance.execute()
        mock_print.assert_called_with(setting_filter='', info=False)

        cmd = 'test_name12345'
        (options, args) = self.parser.parse_args(cmd.split(' '))
        test_instance = ConfsetArguments(args, options)

        self.assertEqual(test_instance.name, 'test_name12345')
        self.assertIsNone(test_instance.attr)
        self.assertIsNone(test_instance.value)
        self.assertFalse(test_instance.arg_options.info)
        self.assertEqual(test_instance.get_filters(), '')
        self.assertIsNone(test_instance.execute())
        test_instance.execute()
        mock_print.assert_called_with(setting_filter='', info=False)

        cmd = 'test_name --info'
        (options, args) = self.parser.parse_args(cmd.split(' '))
        test_instance = ConfsetArguments(args, options)

        self.assertEqual(test_instance.name, 'test_name')
        self.assertIsNone(test_instance.attr)
        self.assertIsNone(test_instance.value)
        self.assertTrue(test_instance.arg_options.info)
        self.assertEqual(test_instance.get_filters(), '')
        test_instance.execute()
        mock_print.assert_called_with(setting_filter='', info=True)

    @mock.patch('confset.confset.ConfigSettings.print_settings')
    def test_get_conf_with_name_attr(self, mock_print):
        cmd = 'test_name.test_attr'
        (options, args) = self.parser.parse_args(cmd.split(' '))
        test_instance = ConfsetArguments(args, options)

        self.assertEqual(test_instance.name, 'test_name')
        self.assertEqual(test_instance.attr, 'test_attr')
        self.assertIsNone(test_instance.value)
        self.assertFalse(test_instance.arg_options.info)
        self.assertEqual(test_instance.get_filters(), 'test_name.test_attr')
        test_instance.execute()
        mock_print.assert_called_with(setting_filter='test_name.test_attr', info=False)

        cmd = 'test_name.test_attr_12345'
        (options, args) = self.parser.parse_args(cmd.split(' '))
        test_instance = ConfsetArguments(args, options)

        self.assertEqual(test_instance.name, 'test_name')
        self.assertEqual(test_instance.attr, 'test_attr_12345')
        self.assertIsNone(test_instance.value)
        self.assertFalse(test_instance.arg_options.info)
        self.assertEqual(test_instance.get_filters(), 'test_name.test_attr_12345')
        self.assertIsNone(test_instance.execute())
        test_instance.execute()
        mock_print.assert_called_with(setting_filter='test_name.test_attr_12345', info=False)

        cmd = 'test_name._test_attr'
        (options, args) = self.parser.parse_args(cmd.split(' '))
        test_instance = ConfsetArguments(args, options)

        self.assertEqual(test_instance.name, 'test_name')
        self.assertEqual(test_instance.attr, '_test_attr')
        self.assertIsNone(test_instance.value)
        self.assertFalse(test_instance.arg_options.info)
        self.assertEqual(test_instance.get_filters(), 'test_name._test_attr')
        self.assertIsNone(test_instance.execute())
        test_instance.execute()
        mock_print.assert_called_with(setting_filter='test_name._test_attr', info=False)

        cmd = 'test_name.TEST_ATTR'
        (options, args) = self.parser.parse_args(cmd.split(' '))
        test_instance = ConfsetArguments(args, options)

        self.assertEqual(test_instance.name, 'test_name')
        self.assertEqual(test_instance.attr, 'TEST_ATTR')
        self.assertIsNone(test_instance.value)
        self.assertFalse(test_instance.arg_options.info)
        self.assertEqual(test_instance.get_filters(), 'test_name.TEST_ATTR')
        self.assertIsNone(test_instance.execute())
        test_instance.execute()
        mock_print.assert_called_with(setting_filter='test_name.TEST_ATTR', info=False)

        cmd = 'test_name.TEST_ATTR --info'
        (options, args) = self.parser.parse_args(cmd.split(' '))
        test_instance = ConfsetArguments(args, options)

        self.assertEqual(test_instance.name, 'test_name')
        self.assertEqual(test_instance.attr, 'TEST_ATTR')
        self.assertIsNone(test_instance.value)
        self.assertTrue(test_instance.arg_options.info)
        self.assertEqual(test_instance.get_filters(), 'test_name.TEST_ATTR')
        self.assertIsNone(test_instance.execute())
        test_instance.execute()
        mock_print.assert_called_with(setting_filter='test_name.TEST_ATTR', info=True)

    @mock.patch('confset.confset.ConfigSettings.set')
    @mock.patch('confset.confset.ConfigSettings.print_settings')
    def test_set_key(self, mock_print, mock_set):
        cmd = 'test_name.test_attr=test_value'
        (options, args) = self.parser.parse_args(cmd.split(' '))
        test_instance = ConfsetArguments(args, options)

        self.assertEqual(test_instance.name, 'test_name')
        self.assertEqual(test_instance.attr, 'test_attr')
        self.assertEqual(test_instance.value, 'test_value')
        self.assertFalse(test_instance.arg_options.info)
        self.assertEqual(test_instance.get_filters(), 'test_name.test_attr')
        self.assertIsNone(test_instance.execute())
        test_instance.execute()
        mock_set.assert_called_with('test_attr', 'test_value')
        mock_print.assert_called_with(setting_filter='test_name.test_attr', info=False)

        cmd = 'test_name.test_attr="test value with space"'
        (options, args) = self.parser.parse_args(cmd.split(' '))
        test_instance = ConfsetArguments(args, options)

        self.assertEqual(test_instance.name, 'test_name')
        self.assertEqual(test_instance.attr, 'test_attr')
        self.assertEqual(test_instance.value, '"test value with space"')
        self.assertFalse(test_instance.arg_options.info)
        self.assertEqual(test_instance.get_filters(), 'test_name.test_attr')
        self.assertIsNone(test_instance.execute())
        test_instance.execute()
        mock_set.assert_called_with('test_attr', '"test value with space"')
        mock_print.assert_called_with(setting_filter='test_name.test_attr', info=False)

        cmd = 'test_name.test_attr=\'test value with space and single quote\''
        (options, args) = self.parser.parse_args(cmd.split(' '))
        test_instance = ConfsetArguments(args, options)

        self.assertEqual(test_instance.name, 'test_name')
        self.assertEqual(test_instance.attr, 'test_attr')
        self.assertEqual(test_instance.value, '\'test value with space and single quote\'')
        self.assertFalse(test_instance.arg_options.info)
        self.assertEqual(test_instance.get_filters(), 'test_name.test_attr')
        self.assertIsNone(test_instance.execute())
        test_instance.execute()
        mock_set.assert_called_with('test_attr', '\'test value with space and single quote\'')
        mock_print.assert_called_with(setting_filter='test_name.test_attr', info=False)

        cmd = 'test_name.test_attr="test value with space and number 13454.2314"'
        (options, args) = self.parser.parse_args(cmd.split(' '))
        test_instance = ConfsetArguments(args, options)

        self.assertEqual(test_instance.name, 'test_name')
        self.assertEqual(test_instance.attr, 'test_attr')
        self.assertEqual(test_instance.value, '"test value with space and number 13454.2314"')
        self.assertFalse(test_instance.arg_options.info)
        self.assertEqual(test_instance.get_filters(), 'test_name.test_attr')
        self.assertIsNone(test_instance.execute())
        test_instance.execute()
        mock_set.assert_called_with('test_attr', '"test value with space and number 13454.2314"')
        mock_print.assert_called_with(setting_filter='test_name.test_attr', info=False)

        cmd = 'test_name.test_attr="special characters %#$&%#!%"'
        (options, args) = self.parser.parse_args(cmd.split(' '))
        test_instance = ConfsetArguments(args, options)

        self.assertEqual(test_instance.name, 'test_name')
        self.assertEqual(test_instance.attr, 'test_attr')
        self.assertEqual(test_instance.value, '"special characters %#$&%#!%"')
        self.assertFalse(test_instance.arg_options.info)
        self.assertEqual(test_instance.get_filters(), 'test_name.test_attr')
        self.assertIsNone(test_instance.execute())
        test_instance.execute()
        mock_set.assert_called_with('test_attr', '"special characters %#$&%#!%"')
        mock_print.assert_called_with(setting_filter='test_name.test_attr', info=False)

    def test_invalid_arguments(self):
        """
        Test all invalid commands. Any command from here should all raise sys.exit(1)
        :return:
        """
        cmd = '.test_attr'
        with self.assertRaises(SystemExit) as cm:
            (options, args) = self.parser.parse_args(cmd.split(' '))
            _ = ConfsetArguments(args, options)

        self.assertEqual(cm.exception.code, 1)

        cmd = '.test_attr=test_value'
        with self.assertRaises(SystemExit) as cm:
            (options, args) = self.parser.parse_args(cmd.split(' '))
            _ = ConfsetArguments(args, options)

        self.assertEqual(cm.exception.code, 1)

        cmd = '=test_value'
        with self.assertRaises(SystemExit) as cm:
            (options, args) = self.parser.parse_args(cmd.split(' '))
            _ = ConfsetArguments(args, options)

        self.assertEqual(cm.exception.code, 1)

        cmd = 'test_name=test_value'
        with self.assertRaises(SystemExit) as cm:
            (options, args) = self.parser.parse_args(cmd.split(' '))
            _ = ConfsetArguments(args, options)

        self.assertEqual(cm.exception.code, 1)

        cmd = 'test_name.name.attr=test_value'
        with self.assertRaises(SystemExit) as cm:
            (options, args) = self.parser.parse_args(cmd.split(' '))
            _ = ConfsetArguments(args, options)

        self.assertEqual(cm.exception.code, 1)

        cmd = 'test name.test_attr=test_value'
        with self.assertRaises(SystemExit) as cm:
            (options, args) = self.parser.parse_args(cmd.split(' '))
            _ = ConfsetArguments(args, options)

        cmd = 'test%name.test_attr=test_value'
        with self.assertRaises(SystemExit) as cm:
            (options, args) = self.parser.parse_args(cmd.split(' '))
            _ = ConfsetArguments(args, options)

        cmd = 'test_name.test_attr = test_value'
        with self.assertRaises(SystemExit) as cm:
            (options, args) = self.parser.parse_args(cmd.split(' '))
            _ = ConfsetArguments(args, options)

        self.assertEqual(cm.exception.code, 1)

        cmd = 'test_name.test_attr test_name1.test_attr1'
        with self.assertRaises(SystemExit) as cm:
            (options, args) = self.parser.parse_args(cmd.split(' '))
            ConfsetArguments(args, options)

        self.assertEqual(cm.exception.code, 1)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
