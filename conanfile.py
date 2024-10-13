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
        self.run(f"python3 install.py -a install -c {configuration}")

    def package(self):
        os_name = str(self.settings.os)
        os_dir = os_name
        if os_name == "Macos":
            os_dir = "OSX"
        build_type = str(self.settings.build_type)
        install_folder = os.path.join("install", os_dir)
        print(f"install_folder: {install_folder}")
        self.copy(pattern="*.hpp", dst="include", src=os.path.join(install_folder,"include"))
        lib_pattern = "*.lib"
        bin_pattern = "*.dll"
        if self.settings.os == "Linux":
            lib_pattern = "*.so*"
            bin_pattern = "*.so*"
        elif self.settings.os == "Macos":
            lib_pattern = "*.dylib"
            bin_pattern = "*.dylib"
            
        self.copy(pattern=lib_pattern, dst="lib", src=os.path.join(install_folder, "lib"))
        self.copy(pattern=bin_pattern, dst="bin", src=os.path.join(install_folder, "bin"))
        libs = self.get_shared_libs()

        for lib in libs:
            # copy distributed shared libraries to lib folder
            self.copy(pattern=lib, dst="lib", src=os.path.join(install_folder, "bin"))

        # if self.settings.os == "Linux" or self.settings.os == "Macos":
        #     # copy shared libraries to bin folder
        #     for lib in libs:
        #         self.copy(pattern=lib, dst="bin", src=os.path.join(install_folder, "lib"))

    def get_shared_libs(self):
        lib_names = ["slideio", "slideio-converter", "slideio-transformer", "slideio-core"]
        lib_prefix = ""
        if self.settings.build_type == 'Debug':
            for i in range (len(lib_names)):
                lib_names[i] += "_d"
        lib_suffix = ".lib"
        if self.settings.os == "Linux":
            lib_suffix = ".so"
            lib_prefix = "lib"
        elif self.settings.os == "Macos":
            lib_suffix = ".dylib"
            lib_prefix = "lib"
        for i in range (len(lib_names)):
            lib_names[i] = lib_prefix + lib_names[i] + lib_suffix
        return lib_names

    def package_info(self):
        self.cpp_info.includedirs = ["include"]
        self.cpp_info.libdirs = ["lib"]
        self.cpp_info.bindirs = ["bin"]
        self.cpp_info.libs = self.get_shared_libs()
