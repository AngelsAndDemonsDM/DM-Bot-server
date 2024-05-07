import logging
import os
import subprocess
import sys

from colorlog import ColoredFormatter

from build import build_main, build_updater, pack


def clear_consol() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')

def print_menu() -> None:
    print("1. build_main & pack")
    print("2. build_updater")
    print("0. exit")

def main() -> None:
    while True:
        clear_consol()
        print_menu()
        menu = input("> ")
        
        match int(menu):
            case 1:
                build_main()
                pack(folder_to_add=["templates", "static", "../Prototype.DM-Bot", "../Loc.DM-Bot", "../Sprites.DM-Bot"])
                
            case 2:
                build_updater()

            case 0:
                sys.exit(0)
            
            case _:
                print("number error")
                input("Enter...")


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

    main()