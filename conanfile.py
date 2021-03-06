import os

from conans import ConanFile, tools


class PythonPipConan(ConanFile):
    name = "python-pip"
    version = tools.get_env("GIT_TAG", "19.2.3")
    license = "MIT"
    description = "High productivity build system"
    settings = "os", "compiler", "build_type", "arch"

    def source(self):
        tools.get("https://github.com/pypa/pip/archive/%s.tar.gz" % self.version)

    def build_requirements(self):
        self.build_requires("generators/1.0.0@camposs/stable")
        self.build_requires("python-setuptools/[>=41.2.0]@camposs/stable")

    def requirements(self):
        self.requires("python/[>=3.8.2]@camposs/stable")

    def build(self):
        with tools.chdir("pip-" + self.version):
            self.run('python setup.py install --optimize=1 --prefix= --root="%s"' % self.package_folder)

    def package_info(self):
        self.env_info.PYTHONPATH.append(os.path.join(self.package_folder, "lib", "python3.8", "site-packages"))
