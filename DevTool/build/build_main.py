import logging
import os
import shutil
import subprocess

BUILD_NAME = "DM-Bot"

def build_main():
    logging.info("Start build main file")
    cur_path = os.path.dirname(os.path.abspath(__file__))

    if os.path.exists(os.path.join(cur_path, BUILD_NAME)):
        shutil.rmtree(cur_path)
    
    nuitka_command = (
        f"python -m nuitka "
        f"--remove-output "
        f"--jobs=4 "
        f"--standalone "
        f"--no-pyi-file "
        f"--windows-icon-from-ico=../Sprites.DM-Bot/icons/exe-main-icon.png "
        f"../Code.DM-Bot/main.py"
    )
    subprocess.run(nuitka_command, shell=True)

    os.rename("main.dist", BUILD_NAME)
