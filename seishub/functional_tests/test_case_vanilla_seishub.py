import unittest
from utils import send_http_request, BASE_URL


class VanillaSeisHubTestCase(unittest.TestCase):
    """
    Simple test case that checks that the basic original setup is correct
    directly after running the initenv command.

    The server should be configured to have three users:
        * admin, pw: admin, groups: users, admin
        * admin_2, pw: admin_pw, group: users, admin
        * user, pw: user_pw, groups: users
    """
    def setUp(self):
        pass

    def test_non_existing_websites_raise_404(self):
        """
        Non existing websites should raise 404 in any case.
        """
        urls = [BASE_URL + "/asdfghjkl",
                BASE_URL + "/asdfghjkl/asdfjkl",
                BASE_URL + "/manage/asdfghkjkl"]
        for url in urls:
            code, msg, req = send_http_request(url, "GET", "admin", "admin",
                "")
            self.assertEqual(code, 404)
            self.assertEqual(req, None)
            code, msg, req = send_http_request(url, "GET", "", "", "")
            self.assertEqual(code, 404)
            self.assertEqual(req, None)
            code, msg, req = send_http_request(url, "GET", "adf", "", "")
            self.assertEqual(code, 404)
            self.assertEqual(req, None)
            code, msg, req = send_http_request(url, "GET", "lo", "sd", "")
            self.assertEqual(code, 404)
            self.assertEqual(req, None)
            code, msg, req = send_http_request(url, "GET", "admin", "a", "")
            self.assertEqual(code, 404)
            self.assertEqual(req, None)
            code, msg, req = send_http_request(url, "GET", "admin", "", "")
            self.assertEqual(code, 404)
            self.assertEqual(req, None)
            code, msg, req = send_http_request(url, "GET", "user", "user_pw",
                "")
            self.assertEqual(code, 404)
            self.assertEqual(req, None)

    def test_manage_url_only_accessible_by_admin(self):
        """
        The /manage URL and those below it should only be accessible from
        admins.
        """
        urls = [BASE_URL + "/manage",
                BASE_URL + "/manage/admin/basic",
                BASE_URL + "/manage/admin/database"]
        for url in urls:
            # Admins should be able to access it.
            code, msg, req = send_http_request(url, "GET", "admin", "admin",
                "")
            self.assertEqual(code, 200)
            self.assertTrue(req is not None)
            # Admins should be able to access it.
            code, msg, req = send_http_request(url, "GET", "admin_2",
                "admin_pw", "")
            self.assertEqual(code, 200)
            self.assertTrue(req is not None)
            # Others should be denied
            code, msg, req = send_http_request(url, "GET", "", "", "")
            self.assertEqual(code, 401)
            self.assertEqual(req, None)
            code, msg, req = send_http_request(url, "GET", "adf", "", "")
            self.assertEqual(code, 401)
            self.assertEqual(req, None)
            code, msg, req = send_http_request(url, "GET", "lo", "sd", "")
            self.assertEqual(code, 401)
            self.assertEqual(req, None)
            # Also the wrong password should be denied.
            code, msg, req = send_http_request(url, "GET", "admin", "a", "")
            self.assertEqual(code, 401)
            self.assertEqual(req, None)
            # Also the wrong password should be denied.
            code, msg, req = send_http_request(url, "GET", "admin", "", "")
            self.assertEqual(code, 401)
            self.assertEqual(req, None)
            code, msg, req = send_http_request(url, "GET", "admin_2", "admin",
                "")
            self.assertEqual(code, 401)
            self.assertEqual(req, None)
            # Non-admins with the correct password also have no access.
            code, msg, req = send_http_request(url, "GET", "user", "user_pw",
                "")
            self.assertEqual(code, 401)
            self.assertEqual(req, None)


def run():
    suite = unittest.TestLoader().loadTestsFromTestCase(VanillaSeisHubTestCase)
    unittest.TextTestRunner(verbosity=1).run(suite)
