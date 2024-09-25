import random
from pymongo import MongoClient


def generate_genres():
    genre_list = ["Platformer", "Shooter", "Battle Royale", "Survival", "Horror", "RPG", "Defense"]
    genre_amount = random.randrange(1, 4)
    genres = set()
    for i in range(genre_amount):
        genres.add(random.choice(genre_list))
    genres.add(random.choice(["Multiplayer", "Singleplayer"]))
    return list(genres)


nouns = [
    "Adventure", "Quest", "Fantasy", "War", "Space", "Legend", "Mystery", "Magic", "Horror", "Kingdom",
    "Dungeon", "Blade", "Dragon", "World", "Chronicles", "Heroes", "Empires", "Pirates", "Titans", "Guardians",
    "Odyssey", "Legacy", "Prophecy", "Realm", "Saga", "Frontier", "Apocalypse", "Labyrinth", "Reckoning", "Phantoms",
    "Mysteries", "Requiem", "Destiny", "Conquest", "Titans", "Dawn", "Chronicles", "Eclipse", "Pioneers", "Legends",
    "Cataclysm", "Relics", "Ascension", "Exiles", "Armada", "Rune", "Wasteland", "Infinity"
]

adjectives = [
    "Epic", "Legendary", "Dark", "Mythical", "Infinite", "Lost", "Virtual", "Ancient", "Cosmic", "Eternal",
    "Mystic", "Forgotten", "Savage", "Mighty", "Mysterious", "Haunted", "Heroic", "Forged", "Shadow", "Fiery",
    "Astral", "Radiant", "Divine", "Surreal", "Cursed", "Ethereal", "Sorcerer's", "Fabled", "Chaos", "Legendary",
    "Enchanted", "Furious", "Steampunk", "Crystal", "Frosty", "Mechanical", "Fearsome", "Celestial", "Timeless",
    "Vengeful", "Raging", "Spectral", "Titanic", "Crimson", "Celestial", "Epic", "Ancient", "Uncharted", "Mythical"
]

client = MongoClient("localhost", 27017)
db = client.spiele

for i in range(100):
    name = f'{random.choice(adjectives)} {random.choice(nouns)}'
    year = random.randrange(1980, 2023)
    downloads = random.randrange(10, 100_000)
    rating = random.randrange(10, 100) / 10
    altersgrenze = random.choice([0, 6, 12, 16, 18])
    genres = generate_genres()
        
    db.pcgames.insert_one({
        "name": name,
        "genres": genres,
        "year": year,
        "downloads": downloads,
        "rating": rating,
        "min_age": altersgrenze
    })
