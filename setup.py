import os
import subprocess

from setuptools import setup
from setuptools.command.install import install


class CustomInstallCommand(install):
    def run(self):
        print("[INFO]: Building with GGML_METAL=on")
        os.environ["CMAKE_ARGS"] = "-DGGML_METAL=on"
        subprocess.check_call(
            ["pip", "install", "-U", "llama-cpp-python", "--no-cache-dir"]
        )
        install.run(self)


setup(
    version=os.environ.get("BUILD_VERSION"),
    cmdclass={
        "install": CustomInstallCommand,
    },
)
