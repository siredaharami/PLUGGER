from config import OWNER_ID
from typing import Union, List, Pattern
from pyrogram import Client, filters as pyrofl
from pytgcalls import PyTgCalls, filters as pytgfl

def cdx(commands: Union[str, List[str]]):
    return pyrofl.command(commands, ["/", "!", "."])


def cdz(commands: Union[str, List[str]]):
    return pyrofl.command(commands, ["", "/", "!", "."])


def rgx(pattern: Union[str, Pattern]):
    return pyrofl.regex(pattern)


bot_owner_only = pyrofl.user(OWNER_ID)
