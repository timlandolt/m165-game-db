import os

from rich.markdown import Markdown
from rich.table import Table
from rich import print, box


def clear(db, console):
    os.system('cls')
    os.system('title Spiele-Datenbank')
    print(Markdown('# Wilkommen zum Spiele-Datenbank CLI'))
    console.print(f"[dim]{db.pcgames.count_documents({})} Einträge in der Datenbank[/dim]", justify='right')


def to_table(statement):
    table = Table(box=box.ROUNDED)

    table.add_column("Name")
    table.add_column("Genres")
    table.add_column("Entstehung", justify='center')
    table.add_column("Downloads", justify='right')
    table.add_column("Bewertung", justify='right')
    table.add_column("Mindestalter", justify='right')

    for entry in statement:
        table.add_row(
            entry["name"],
            str(entry["genres"])
            .replace('[', '')
            .replace(']', '')
            .replace("'", ''),
            str(entry["year"]),
            str(entry["downloads"]),
            str(entry["rating"]),
            str(entry["min_age"])
        )

    return table
