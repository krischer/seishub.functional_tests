#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Functional SeisHub tests.

Rather expensive, as they always create a new SeisHub instance, launch it and
then send and receive REST request, but this tests the whole SeisHub chain.

:copyright:
    Lion Krischer (krischer@geophysik.uni-muenchen.de), 2012
:license:
    GNU Lesser General Public License, Version 3
    (http://www.gnu.org/copyleft/lesser.html)
"""
import os
import shutil
import subprocess
import sys
import time
import urllib2

from utils import print_info, print_error, TEST_DIRECTORY, BIN_DIR, BASE_URL

import test_case_vanilla_seishub
import test_case_initial_installation


def init_seishub_instance():
    """
    Creates a new SeisHub instance at TEST_DIRECTORY.
    """
    print_info("Creating new SeisHub instance...")

    if os.path.exists(TEST_DIRECTORY):
        shutil.rmtree(TEST_DIRECTORY)

    cmd = ["seishub-admin", "initenv", TEST_DIRECTORY]
    try:
        subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError, e:
        print_error("Error creating seishub instance. Exited with return "
            "code %s. Full output follows:" % (str(e.returncode)))
        print ""
        print e.output
        print ""
        sys.exit(1)


def launch_seishub_server():
    """
    Launches the SeisHub instance, loops until the startup sequence is finished
    and returns the process object.
    """
    print_info("Starting SeisHub Server...")

    proc = subprocess.Popen(os.path.join(BIN_DIR, "debug.sh"), shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    # Ping the server for up to ten seconds. This should assure it has started.
    t = time.time()
    while (time.time() - t) < 10.0:
        try:
            urllib2.urlopen(BASE_URL).read()
            break
        except Exception, e:
            if hasattr(e, "code"):
                break
            time.sleep(0.25)

    # Give some extra time, succesful pinging means just that the webservice
    # has started.
    time.sleep(0.25)
    print_info("SeisHub server started.")
    return proc


def stop_seishub_server(proc):
    """
    Terminates the passed process object.
    """
    proc.terminate()
    proc.kill()
    proc.wait()

    # Wait for a short time and then just kill it. Quite brute force, but the
    # only reliable way I could find.
    time.sleep(0.2)
    os.system('pkill -f "python -m seishub.core.daemon"')

    print_info("SeisHub Server terminated.")


def cleanup():
    """
    Simply removes the temporarily created SeisHub instance.
    """
    print_info("Cleaning up...")

    # Try deleting it for some seconds...
    t = time.time()
    while (time.time() - t) < 10.0:
        time.sleep(0.1)
        try:
            if os.path.exists(TEST_DIRECTORY):
                shutil.rmtree(TEST_DIRECTORY)
            return
        except:
            pass
    print_error("Cleanup failed.")


if __name__ == "__main__":
    print(
        "===================================================================\n"
        "Functional tests for SeisHub.\n\n"
        "A series of tests mainly to validate the REST interface of SeisHub.\n"
        "SeisHub is largely treated as a black box and only input, output\n"
        "and HTTP response codes are tested.\n"
        "===================================================================\n"
    )
    init_seishub_instance()

    print_info("Launching test case for initial setup...")
    # Run the basic setup test suite.
    test_case_initial_installation.run()

    proc = launch_seishub_server()

    print_info("Launching test case for vanilla SeisHub installation...")
    # Run the basic setup test suite.
    test_case_vanilla_seishub.run()

    stop_seishub_server(proc)

    cleanup()
