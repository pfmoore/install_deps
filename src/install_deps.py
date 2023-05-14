import argparse
import subprocess
import sys
import tomllib


def install_deps_from(filename):
    # Warning: code has only been lightly tested!
    with open(filename, "rb") as f:
        data = tomllib.load(f)

    if "project" not in data:
        raise ValueError(f"No PEP 621 metadata in {filename}")
    if "dependencies" in data["project"].get("dynamic", []):
        raise ValueError("Dependencies cannot be dynamic")

    deps = data["project"].get("dependencies")

    if not deps:
        print(f"No dependencies specified in {filename}")
        return

    cmd = [sys.executable, "-m", "pip", "install", *deps]
    subprocess.run(cmd)


def parse_args(args=None):
    parser = argparse.ArgumentParser(
        prog="install-deps",
        description="Install a project's dependencies from pyproject.toml",
    )
    parser.add_argument(
        "filename",
        help="The pyproject.toml file to read dependencies from",
    )
    return parser.parse_args(args)


def main():
    args = parse_args()
    try:
        install_deps_from(args.filename)
    except ValueError as e:
        print(f"Error: {e.args[0]}")
        sys.exit(1)
