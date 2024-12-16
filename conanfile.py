import os

from conan import ConanFile
from conan.tools.files import copy, get, chdir, download
from conan.tools.layout import basic_layout
from conan.tools.env import Environment

required_conan_version = ">=1.52.0"


class PythonPipConan(ConanFile):
    python_requires = "camp_common/0.5@camposs/stable"
    python_requires_extend = "camp_common.CampPythonBase"

    package_type = 'application'

    name = "python-pip"
    version = "24.3.1"
    license = "MIT"
    description = "High productivity build system"

    settings = "os", "arch"

    def build_requirements(self):
        if self._use_custom_python:
            self.requires("cpython/[~{}]@camposs/stable".format(self._python_version))

    def layout(self):
        basic_layout(self, src_folder="src")

    def generate(self):
        env1 = Environment()
        env1.define("PYTHONPATH", os.path.join(self.package_folder, "lib", f"python{self._python_version}", "site-packages"))
        envvars = env1.vars(self)
        envvars.save_script("py_env_file")

    def package_id(self):
        self.info.clear()

    def source(self):
        download(self, "https://bootstrap.pypa.io/get-pip.py", "get-pip.py")

    def build(self):
        self.run('{0} {1} --prefix={2}'.format(self._python_exec, os.path.join(self.source_folder, "get-pip.py"), self.package_folder), env=["py_env_file"])

    def package_info(self):
        self.runenv_info.append_path("PYTHONPATH", os.path.join(self.package_folder, "lib", f"python{self._python_version}", "site-packages"))
        self.buildenv_info.append_path("PYTHONPATH", os.path.join(self.package_folder, "lib", f"python{self._python_version}", "site-packages"))


