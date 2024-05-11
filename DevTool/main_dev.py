import logging
import os
import subprocess
import sys

from build import build_main, pack
from colorlog import ColoredFormatter

if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)        
    
    console_handler = logging.StreamHandler()
    formatter = ColoredFormatter(
        "[%(asctime)s] [%(log_color)s%(levelname)s%(reset)s] - %(message)s",
        datefmt=None,
        reset=True,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'purple',
        },
        secondary_log_colors={},
        style='%'
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    build_main()
    pack(folder_to_add=["templates", "static", "../Prototype.DM-Bot", "../Loc.DM-Bot", "../Sprites.DM-Bot"], use_password=False)
