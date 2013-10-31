from cx_Freeze import setup, Executable
import sys

includefiles = ["assets"]
includes = ["numbers"]
excludes = []
packages = []
path = sys.path

base = "Console"
if sys.platform == "win32":
    base = "Win32GUI"

setup(name = "Hivemind Demo 1",
    version = "0.0.1",
    description = "Controls demo. Kinda clunky!",
    options = {"build_exe": {"includes": includes,
                             "excludes": excludes,
                             "packages": packages,
                             "path": path,
                             "optimize": 2,
                             "include_files":includefiles}
               },
    executables = [Executable("player_test.py", base=base)])