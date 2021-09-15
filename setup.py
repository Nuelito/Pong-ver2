import sys
from cx_Freeze import setup, Executable

options = {
    "build_exe": {
        "packages": ["pygame"],
        "include_files": ["src/"],
        "excludes": ["tkinter", "email", "json", "numpy", "PyInstaller", "test",
                    "multiprocessing", "asyncio", "lib2to3", "pkg_resources",
                    "http", "html", "distutils"]
    }
}

executables = [Executable("main.py", targetName="Pong", base = "Win32GUI")]

setup(
    name = "Pong",
    version = "1.0",
    description = "Description",
    options = options,
    executables=executables
)