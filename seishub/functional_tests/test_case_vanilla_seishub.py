import unittest
from utils import send_http_request, BASE_URL


class VanillaSeisHubTestCase(unittest.TestCase):
    """
    Simple test case that checks that the basic original setup is correct
    directly after running the initenv command.
    """
    def setUp(self):
        pass

    def test_manage_url_only_accessible_by_admin(self):
        """
        The /manage URL should only be accessible from admins.
        """
        url = BASE_URL + "/manage"
        # Admin should be able to access it.
        code, msg, req = send_http_request(url, "GET", "admin", "admin", "")
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
        code, msg, req = send_http_request(url, "GET", "admin", "", "")
        self.assertEqual(code, 401)
        self.assertEqual(req, None)


def run():
    suite = unittest.TestLoader().loadTestsFromTestCase(VanillaSeisHubTestCase)
    unittest.TextTestRunner(verbosity=1).run(suite)
