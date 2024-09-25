import os

from rich.pretty import pprint
from rich import print
from rich.console import Console
from utils import clear, to_table


# Show
def anzeigen(db):
    print('[b]Welche Einträge wollen Sie anzeigen lassen?[/b]')
    print('[r] 1 [/r] Alle       [r] 2 [/r] Zufälliger')
    print('[red][r] X [/r] Schliessen[/red]')

    eingabe = input()
    if eingabe.lower() == 'x':
        exit()

    print('[b]Wie sollen die Einträge formattiert werden?[/b]')
    print('[r] 1 [/r] JSON [r] 2 [/r] Tabelle')

    format = input()
    clear(db, Console())

    match eingabe.lower():
        case '1':
            if format == '1':
                for entry in db.pcgames.find():
                    pprint(entry)
            else:
                statement = db.pcgames.find()
                print(to_table(statement))

        case '2':
            if format == '1':
                for entry in db.pcgames.aggregate([{"$sample": {"size": 1}}]):
                    pprint(entry)
            else:
                statement = db.pcgames.aggregate([{"$sample": {"size": 1}}])
                print(to_table(statement))


# Update
def veraendern(db):
    print('[b]Wie wollen Sie Ihre/n Eintrag/e aussuchen?[/b]')
    print('[r] 1 [/r] Titel           [r] 2 [/r] Genre')
    print('[r] 3 [/r] Entstehungsjahr [red][r] X [/r] Schliessen[/red]')

    eingabe = input()
    if eingabe.lower() == 'x':
        os.system('cls')
        return

    clear(db, Console())

    search = {}

    match eingabe.lower():
        case '1':
            # Titel
            while True:
                print("[dim]Geben Sie [r]exit[/r] ein, um diesen Dialog zu verlassen.[/dim]")
                title = input("Nach welchem Titel wollen Sie suchen? ").strip()
                if title.lower() == "exit":
                    os.system('cls')
                    return
                if db.pcgames.count_documents({'name': title}, limit=1):
                    clear(db, Console())
                    print(to_table(db.pcgames.find({'name': title})))
                    search = {'name': title}
                    break

                clear(db, Console())
                print(f"[red]Es existiert kein Spiel namens [r]{title}[/r] in dieser Datenbank...[/red]")

        case '2':
            # Genre
            while True:
                print("[dim]Geben Sie [r]exit[/r] ein, um diesen Dialog zu verlassen.[/dim]")
                genre = input("Nach welchem/n Genre/s wollen Sie suchen? ").strip()
                if genre.lower() == "exit":
                    os.system('cls')
                    return
                genre = [x.strip() for x in genre.split(',')]
                if db.pcgames.count_documents({'genres': {'$all': genre}}, limit=1):
                    clear(db, Console())
                    print(to_table(db.pcgames.find({'genres': {'$all': genre}})))
                    search = {'genres': {'$all': genre}}
                    break

                clear(db, Console())
                print(f"[red]Es existiert kein Spiel mit dem Genre [r]{genre}[/r] in dieser Datenbank...[/red]")

        case '3':
            # Entstehungsjahr
            while True:
                print("[dim]Geben Sie [r]exit[/r] ein, um diesen Dialog zu verlassen.[/dim]")
                year = input("Nach welchem Entstehungsjahr wollen Sie suchen? ").strip()
                if year.lower() == "exit":
                    os.system('cls')
                    return
                year = int(year)
                if db.pcgames.count_documents({'year': year}, limit=1):
                    clear(db, Console())
                    print(to_table(db.pcgames.find({'year': year})))
                    search = {'year': year}
                    break

                clear(db, Console())
                print(f"[red]Es existiert kein Spiel aus dem Jahr [r]{year}[/r] in dieser Datenbank...[/red]")

    print('Geben Sie die Daten an, mit welchen die aktuellen ersetzt werden sollen.')
    print('Lassen Sie sie frei, um sie beizubehalten.\n')

    name_new = input('Name: ').strip()
    genres_new = input('Genres (mit ", " getrennt): ')
    entstehung_new = input('Entstehungsjahr: ')
    downloads_new = input('Downloads: ')
    bewertung_new = input('Bewertung: ')
    mindestalter_new = input('Mindestalter: ')

    print('[r] 1 [/r] So übernehmen [red][r] X [/r] Schliessen[/red]')
    if input().lower() == 'x':
        os.system('cls')
        return

    update = {}
    if not name_new == '':
        update.update({'name': name_new})
    if not genres_new == '':
        update.update({'genres': genres_new.split(', ')})
    if not entstehung_new == '':
        update.update({'year': int(entstehung_new)})
    if not downloads_new == '':
        update.update({'downloads': int(downloads_new)})
    if not bewertung_new == '':
        update.update({'rating': float(bewertung_new)})
    if not mindestalter_new == '':
        update.update({'min_age': int(mindestalter_new)})

    db.pcgames.update_many(search, {"$set": update})


# Insert
def einfuegen(db):
    print('Geben Sie die Daten an, welche Sie einfügen wollen.')
    print('Lassen Sie sie frei, um sie nicht zu setzen.\n')

    name_new = input('Name: ').strip()
    genres_new = input('Genres (mit ", " getrennt): ')
    entstehung_new = input('Entstehungsjahr: ')
    downloads_new = input('Downloads: ')
    bewertung_new = input('Bewertung: ')
    mindestalter_new = input('Mindestalter: ')

    print('[r] 1 [/r] So übernehmen [red][r] X [/r] Schliessen[/red]')
    if input().lower() == 'x':
        os.system('cls')
        return

    values = {}
    if not name_new == '':
        values.update({'name': name_new})
    if not genres_new == '':
        values.update({'genres': genres_new.split(', ')})
    if not entstehung_new == '':
        values.update({'year': int(entstehung_new)})
    if not downloads_new == '':
        values.update({'downloads': int(downloads_new)})
    if not bewertung_new == '':
        values.update({'rating': float(bewertung_new)})
    if not mindestalter_new == '':
        values.update({'min_age': int(mindestalter_new)})

    db.pcgames.insert_one(values)


# Delete
def loeschen(db):
    print('[b]Wie wollen Sie Ihre/n Eintrag/e aussuchen?[/b]')
    print('[r] 1 [/r] Titel           [r] 2 [/r] Genre')
    print('[r] 3 [/r] Entstehungsjahr [red][r] X [/r] Schliessen[/red]')

    eingabe = input()
    if eingabe.lower() == 'x':
        os.system('cls')
        return

    clear(db, Console())

    search = {}

    match eingabe.lower():
        case '1':
            # Titel
            while True:
                print("[dim]Geben Sie [r]exit[/r] ein, um diesen Dialog zu verlassen.[/dim]")
                title = input("Nach welchem Titel wollen Sie suchen? ").strip()
                if title.lower() == "exit":
                    os.system('cls')
                    return
                if db.pcgames.count_documents({'name': title}, limit=1):
                    clear(db, Console())
                    print(to_table(db.pcgames.find({'name': title})))
                    search = {'name': title}
                    break

                clear(db, Console())
                print(f"[red]Es existiert kein Spiel namens [r]{title}[/r] in dieser Datenbank...[/red]")

        case '2':
            # Genre
            while True:
                print("[dim]Geben Sie [r]exit[/r] ein, um diesen Dialog zu verlassen.[/dim]")
                genre = input("Nach welchem/n Genre/s wollen Sie suchen? ").strip()
                if genre.lower() == "exit":
                    os.system('cls')
                    return
                genre = [x.strip() for x in genre.split(',')]
                if db.pcgames.count_documents({'genres': {'$all': genre}}, limit=1):
                    clear(db, Console())
                    print(to_table(db.pcgames.find({'genres': {'$all': genre}})))
                    search = {'genres': {'$all': genre}}
                    break

                clear(db, Console())
                print(f"[red]Es existiert kein Spiel mit dem Genre [r]{genre}[/r] in dieser Datenbank...[/red]")

        case '3':
            # Entstehungsjahr
            while True:
                print("[dim]Geben Sie [r]exit[/r] ein, um diesen Dialog zu verlassen.[/dim]")
                year = input("Nach welchem Entstehungsjahr wollen Sie suchen? ").strip()
                if year.lower() == "exit":
                    os.system('cls')
                    return
                year = int(year)
                if db.pcgames.count_documents({'year': year}, limit=1):
                    clear(db, Console())
                    print(to_table(db.pcgames.find({'year': year})))
                    search = {'year': year}
                    break

                clear(db, Console())
                print(f"[red]Es existiert kein Spiel aus dem Jahr [r]{year}[/r] in dieser Datenbank...[/red]")

    print('[r] 1 [/r] Diesen Eintrag löschen [red][r] X [/r] Schliessen[/red]')
    if input().lower() == 'x':
        os.system('cls')
        return

    db.pcgames.delete_many(search)
