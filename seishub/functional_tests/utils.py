#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Utility methods for the SeisHub functional test suite.

:copyright:
    Lion Krischer (krischer@geophysik.uni-muenchen.de), 2012
:license:
    GNU Lesser General Public License, Version 3
    (http://www.gnu.org/copyleft/lesser.html)
"""
import colorama
import os
import tempfile
import urllib2

__all__ = ["TEST_DIRECTORY", "BIN_DIR", "DB_DIR", "AUTH_DB", "SEISHUB_DB",
    "BASE_URL", "send_http_request", "print_info", "print_error"]

# Make sure it works on Windows.
colorama.init()

HTTP_ACCEPTED_METHODS = ["PUT", "POST", "HEAD", "GET", "DELETE"]


def _get_installation_directory():
    tempdir = tempfile.gettempdir()
    if not tempdir:
        msg = "Could not get temporary directory."
        raise Exception(msg)
    tempdir = os.path.abspath(os.path.join(tempdir,
        "__temp_seishub_instance__"))
    return tempdir

TEST_DIRECTORY = _get_installation_directory()

BIN_DIR = os.path.join(TEST_DIRECTORY, "bin")
DB_DIR = os.path.join(TEST_DIRECTORY, "db")
AUTH_DB = os.path.join(DB_DIR, "auth.db")
SEISHUB_DB = os.path.join(DB_DIR, "seishub.db")

BASE_URL = "http://localhost:8080"


def send_http_request(url, method, user, password, data):
    """
    Simple convenience method to send (and receive from) HTTP requests.

    Return a tuple of code, message,  and request (can be None)
    """
    # Create an OpenerDirector for Basic HTTP Authentication
    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, url, user, password)
    auth_handler = urllib2.HTTPBasicAuthHandler(password_mgr)
    opener = urllib2.build_opener(auth_handler)
    # install globally
    urllib2.install_opener(opener)
    code, msg, request = _HTTP_request(url, method, data)
    return code, msg, request


class _RequestWithMethod(urllib2.Request):
    """
    Improved urllib2.Request Class for which the HTTP Method can be set to
    values other than only GET and POST.  See
    http://benjamin.smedbergs.us/blog/2008-10-21/\
    putting-and-deleteing-in-python-urllib2/
    """
    def __init__(self, method, *args, **kwargs):
        if method not in HTTP_ACCEPTED_METHODS:
            msg = "HTTP Method not supported. " + \
                  "Supported are: %s." % HTTP_ACCEPTED_METHODS
            raise ValueError(msg)
        urllib2.Request.__init__(self, *args, **kwargs)
        self._method = method

    def get_method(self):
        return self._method


def _HTTP_request(url, method, data):
    """
    Send a HTTP request via urllib2.

    :type url: String
    :param url: Complete URL of resource
    :type method: String
    :param method: HTTP method of request, e.g. "PUT"
    :type data: String
    :param data: XML for a send request (PUT/POST)
    """
    req = _RequestWithMethod(method=method, url=url, data=data)
    # it seems the following always ends in a urllib2.HTTPError even with
    # nice status codes...?!?
    try:
        response = urllib2.urlopen(req)
        return response.code, response.msg, response
    except urllib2.HTTPError, e:
        return e.code, e.msg, None


def print_log(color, msg):
    print color + msg + colorama.Style.RESET_ALL


def print_info(msg):
    print_log(colorama.Fore.GREEN, msg)


def print_error(msg):
    print_log(colorama.Fore.RED, msg)
