from conans import ConanFile, CMake, tools
import os
import glob


class Slideio(ConanFile):
    name = "slideio"
    url = ""
    version = "2.7.0"
    description = "SlideIO library."
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    license = "BSD 3-Clause"
    _source_subfolder = "source_subfolder"

    def source(self):
        git = tools.Git()
        git.clone("https://github.com/Booritas/slideio.git", "refactoring", args="--recursive")

    def build(self):
        configuration = 'release'
        if self.settings.build_type == 'Debug':
            configuration = 'debug'
        self.run(f"python install.py -a install -c {configuration}")

    def package(self):
        os_name = str(self.settings.os)
        build_type = str(self.settings.build_type)
        install_folder = os.path.join("install", os_name)
        print(f"install_folder: {install_folder}")
        self.copy(pattern="*.hpp", dst="include", src=os.path.join(install_folder,"include"))
        lib_pattern = "*.lib"
        if self.settings.os == "Linux":
            lib_pattern = "*.so*"
        self.copy(pattern=lib_pattern, dst="lib", src=os.path.join(install_folder, "lib"))
        bin_pattern = "*.dll"
        if self.settings.os == "Linux":
            lib_pattern = "*.so*"
        self.copy(pattern=bin_pattern, dst="bin", src=os.path.join(install_folder, "bin"))

    def package_info(self):
        self.cpp_info.includedirs = ["include"]
        self.cpp_info.libdirs = ["lib"]
        self.cpp_info.bindirs = ["bin"]