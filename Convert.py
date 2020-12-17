# Program to convert images and 2D scenarios into their 2D and 3D counterparts
# Thomas Roller
# Updated by Mohammed Al-Saeedi

import argparse
import sys
from DrawGrid import *

argParser = argparse.ArgumentParser(description="Convert 2D Drawing to 2D or 3D CO2 scenarios",
                                    allow_abbrev=False)
argParser.add_argument("config",
                       type=str,
                       action="store",
                       help="path to configuration file")

argParser.add_argument("--progress-msg",
                       "-p",
                       action="store_true",
                       help="turn on progress messages",
                       dest="prog_msg")

argParser.add_argument("--img-msg",
                       "-i",
                       action="store_true",
                       help="turn on image parsing error/information messages",
                       dest="img_msg")

argParser.add_argument("--no-crit-msg",
                       "-c",
                       action="store_true",
                       help="turn off critical messages",
                       dest="no_crit_msg")

args = argParser.parse_args()

try:
    GridApp.start(args)
except KeyboardInterrupt:
    if (not args.no_crit_msg): print("Caught interrupt")