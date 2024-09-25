import os

import rich
from rich import print
from rich.markdown import Markdown
from rich.console import Console

from crud_operations import *

from pymongo import MongoClient

from utils import clear

client = MongoClient("localhost", 27017)
db = client.spiele

console = Console()

running = True

while running:
    clear(db, console)
    print('[b]Was möchten Sie unternehmen?[/b]')

    print('[r] 1 [/r] Anzeigen [r] 2 [/r] Verändern')
    print('[r] 3 [/r] Einfügen [r] 4 [/r] Löschen')
    print('[red][r] X [/r] Schliessen[/red]')
    eingabe = input()
    if eingabe.lower() == 'x':
        os.system('cls')
        exit()

    clear(db, console)
    match eingabe:
        case '1': anzeigen(db),
        case '2': veraendern(db),
        case '3': einfuegen(db),
        case '4': loeschen(db)

    os.system('pause')

os.system('cls')
