import unittest

from Code.systems.access_manager import AccessFlags


class TestAccessFlags(unittest.TestCase):
    def setUp(self):
        self.access_flags = AccessFlags()

    def test_set_flag(self):
        self.access_flags.set_flag('change_password', True)
        self.assertEqual(self.access_flags['change_password'], True)

        with self.assertRaises(ValueError):
            self.access_flags.set_flag('non_existent_flag', True)

    def test_get_flag(self):
        self.assertEqual(self.access_flags['change_password'], False)
        self.assertIsNone(self.access_flags['non_existent_flag'])

    def test_toggle_flag(self):
        self.access_flags.toggle_flag('change_password')
        self.assertEqual(self.access_flags['change_password'], True)

        self.access_flags.toggle_flag('change_password')
        self.assertEqual(self.access_flags['change_password'], False)

        with self.assertRaises(ValueError):
            self.access_flags.toggle_flag('non_existent_flag')

    def test_to_bytes(self):
        serialized = self.access_flags.to_bytes()
        deserialized = AccessFlags.from_bytes(serialized)
        self.assertEqual(str(self.access_flags), str(deserialized))

    def test_from_bytes(self):
        serialized = self.access_flags.to_bytes()
        deserialized = AccessFlags.from_bytes(serialized)
        self.assertEqual(self.access_flags['change_password'], deserialized['change_password'])
        self.assertEqual(self.access_flags['change_access'], deserialized['change_access'])
        self.assertEqual(self.access_flags['delete_users'], deserialized['delete_users'])

    def test_str(self):
        self.assertEqual(str(self.access_flags), str(self.access_flags._flags))

if __name__ == '__main__':
    unittest.main()
