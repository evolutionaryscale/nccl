import json
import os
import platform
import subprocess

from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class CustomBuildHook(BuildHookInterface):
    def initialize(self, version, build_data):
        try:
            conda_prefix = os.environ["CONDA_PREFIX"]
            subprocess.check_call(['make', 'all'], env={**os.environ, **{"CUDA_HOME": f"{conda_prefix}/targets/x86_64-linux", "CUDA_LIB": f"{conda_prefix}/lib"}})

            glibc_tag = "2_17"
            arch = platform.machine().lower()

            build_data['tag'] = f"cp310-abi3-manylinux_{glibc_tag}_{arch}"

            so_filename = "libnccl-profiler-inspector.so"
            build_data['force_include'][so_filename] = f"nccl_profiler_inspector_cu12/{so_filename}"

        except subprocess.CalledProcessError as e:
            print(f"Makefile failed: {e}")
            raise e
