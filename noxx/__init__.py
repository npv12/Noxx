from sys import version_info

__version__ = "1.0"

if version_info[:2] < (3, 6):
    print("Pyrogram needs version 3.6 or more")
    quit()
