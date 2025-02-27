#!/usr/bin/env python

# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# This script is used to execute pylint within a tox environment. Depending on which package is being executed against,
# a failure may be suppressed.

from subprocess import check_call, CalledProcessError
import argparse
import os
import logging
import sys

from ci_tools.environment_exclusions import PYLINT_OPT_OUT
from ci_tools.parsing import ParsedSetup

logging.getLogger().setLevel(logging.INFO)

root_dir = os.path.abspath(os.path.join(os.path.abspath(__file__), "..", "..", ".."))
rcFileLocation = os.path.join(root_dir, "pylintrc")
lint_plugin_path = os.path.join(root_dir, "scripts/pylint_custom_plugin")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run pylint against target folder. Add a local custom plugin to the path prior to execution. "
    )

    parser.add_argument(
        "-t",
        "--target",
        dest="target_package",
        help="The target package directory on disk. The target module passed to pylint will be <target_package>/azure.",
        required=True,
    )

    args = parser.parse_args()

    pkg_dir = os.path.abspath(args.target_package)
    pkg_details = ParsedSetup.from_path(pkg_dir)

    top_level_module = pkg_details.namespace.split('.')[0]

    if pkg_details.name not in PYLINT_OPT_OUT:
        try:
            check_call(
                [
                    sys.executable,
                    "-m",
                    "pylint",
                    "--rcfile={}".format(rcFileLocation),
                    "--output-format=parseable",
                    os.path.join(args.target_package, top_level_module),
                ]
            )
        except CalledProcessError as e:
            logging.error(
                "{} exited with linting error {}".format(pkg_details.name, e.returncode)
            )
            exit(1)
