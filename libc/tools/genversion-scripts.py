#!/usr/bin/python

# This tool is used to generate the version scripts for libc and libm
# for every architecture.

import atexit
import os.path
import shutil
import tempfile


all_arches = ["arm", "arm64", "mips", "mips64", "x86", "x86_64"]
bionic_libc_root = os.path.join(os.environ["ANDROID_BUILD_TOP"], "bionic/libc")
bionic_libm_root = os.path.join(os.environ["ANDROID_BUILD_TOP"], "bionic/libm")
bionic_libdl_root = os.path.join(os.environ["ANDROID_BUILD_TOP"], "bionic/libdl")
libc_script = os.path.join(bionic_libc_root, "libc.map.txt")
libm_script = os.path.join(bionic_libm_root, "libm.map.txt")
libdl_script = os.path.join(bionic_libdl_root, "libdl.map.txt")

# TODO (dimity): generate architecture-specific version scripts as part of build

# temp directory where we store all intermediate files
bionic_temp = tempfile.mkdtemp(prefix="bionic_genversionscripts")
# Make sure the directory is deleted when the script exits.
atexit.register(shutil.rmtree, bionic_temp)

bionic_libc_root = os.path.join(os.environ["ANDROID_BUILD_TOP"], "bionic/libc")

warning = "Generated by genversionscripts.py. Do not edit."


class VersionScriptGenerator(object):

  def run(self):
    for script in [libc_script, libm_script, libdl_script]:
      basename = os.path.basename(script)
      dirname = os.path.dirname(script)
      for arch in all_arches:
        name = basename.split(".")[0] + "." + arch + ".map"
        tmp_path = os.path.join(bionic_temp, name)
        dest_path = os.path.join(dirname, name)
        with open(tmp_path, "w") as fout:
          with open(script, "r") as fin:
            fout.write("# %s\n" % warning)
            for line in fin:
              index = line.find("#")
              if index != -1:
                arches = line[index+1:].split()
                if arch not in arches:
                  continue
              fout.write(line)
        shutil.copyfile(tmp_path, dest_path)


generator = VersionScriptGenerator()
generator.run()
