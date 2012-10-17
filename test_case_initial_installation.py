import os
import sqlite3
import unittest

from utils import AUTH_DB, SEISHUB_DB, BIN_DIR, TEST_DIRECTORY


class InitialSetupTestCase(unittest.TestCase):
    """
    Simple test case that checks that the basic original setup is correct
    directly after running the initenv command.
    """
    def setUp(self):
        pass

    def test_files(self):
        """
        A number of files should be present in any case. Mainly the start
        scripts, databases and the config file.
        """
        files = [AUTH_DB, SEISHUB_DB,
            os.path.join(BIN_DIR, "start.sh"),
            os.path.join(BIN_DIR, "stop.sh"),
            os.path.join(BIN_DIR, "debug.sh"),
            os.path.join(TEST_DIRECTORY, "conf", "seishub.ini")]
        for file in files:
            self.assertTrue(os.path.exists(file))

    def test_check_default_user(self):
        """
        At init time, only one user should be present: admin. Check it by
        directly reading the database.

        admin is part of two groups: admin and users
        """
        conn = sqlite3.connect(AUTH_DB)
        c = conn.cursor()
        c.execute("SELECT user_name, groups from users")
        users = c.fetchall()
        self.assertEqual(len(users), 1)
        admin = users[0]
        self.assertEqual(admin[0], "admin")
        self.assertEqual(admin[1], "admin, users")

    def test_check_default_group(self):
        """
        At init time, only two groups should be present: admin and users. Check
        it by directly reading the database.
        """
        conn = sqlite3.connect(AUTH_DB)
        c = conn.cursor()
        c.execute("SELECT group_name, group_owner from groups")
        groups = c.fetchall()
        self.assertEqual(len(groups), 2)
        self.assertTrue(("admin", "admin") in groups)
        self.assertTrue(("users", "admin") in groups)


def run():
    suite = unittest.TestLoader().loadTestsFromTestCase(InitialSetupTestCase)
    unittest.TextTestRunner(verbosity=1).run(suite)
