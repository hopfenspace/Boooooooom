#!/usr/bin/env python

import os
import argparse
import json
from distutils.dir_util import copy_tree


def main(args):
    pwd = os.path.join(os.path.dirname(os.path.abspath(__file__)), "modules", args.name)
    lib_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib")
    req_file = os.path.join(pwd, "requirements.json")
    if not os.path.isdir(pwd):
        print(args.name, "is no directory in modules")
        exit(1)
    if not os.path.isfile(req_file):
        print("requirements.json could not be found, generating new one ...")
        with open(req_file, "w") as fh:
            json.dump({"libs": []}, fh, indent=2)
    else:
        with open(req_file) as fh:
            try:
                json_decoded = json.load(fh)
                if "libs" not in json_decoded:
                    print("Invalid json, exiting")
                    exit(1)
                if not os.path.isdir(os.path.join(pwd, "lib")):
                    print("lib dir could not be found in module, generating one")
                    os.mkdir(os.path.join(pwd, "lib"))
                for module in json_decoded["libs"]:
                    if not os.path.isdir(os.path.join(lib_path, module)):
                        print(f"Module {module} could not be found in cpp libs")
                        continue
                    if not os.path.isdir(os.path.join(pwd, "lib", module)):
                        os.mkdir(os.path.join(pwd, "lib", module))
                    copy_tree(os.path.join(lib_path, module), os.path.join(pwd, "lib", module), update=True)

            except json.JSONDecodeError:
                print("Error decoding requirements.json")
                exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "name",
        action="store",
        help="The name of the module"
    )
    arguments = parser.parse_args()

    main(arguments)

