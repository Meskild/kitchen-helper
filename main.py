import sqlite3

connection = sqlite3.connect('cookbook.db')

def add_recipe():
    Rec_name = input("Opskrifts Navn: ")
    Rec_description = input("Opskrifts Beskrivelse: ")
    Rec_total_time = int(input("Total tid i minutter: "))
    Rec_directions = input("Fremgangsmåde: ")
    Rec_category = input("Kategori: ")
    
    cursor.execute("""
    SELECT id FROM Recipe WHERE name = ?
    """, (Rec_category,))
    result = cursor.fetchone()
    if result:
        recipe_id = result[0]
    else:
        cursor.execute("""
        INSERT INTO Recipe (category) VALUES (?)
        """, (Rec_category,))
        recipe_id = cursor.lastrowid

    cursor.execute("INSERT INTO Recipe (name, description, total_time, directions, category) VALUES (?, ?, ?, ?, ?)",
                    (Rec_name, Rec_description, Rec_total_time, Rec_directions, Rec_category))
    return Rec_name, Rec_description, Rec_total_time, Rec_directions, Rec_category

def add_ingredient():
    cursor.execute("""
    SELECT id FROM Ingredients WHERE name = ?
    """, (Ing_name,))
    result = cursor.fetchone()
    if result:
        ingredient_id = result[0]
    else:
        cursor.execute("""
        INSERT INTO Ingredients (name) VALUES (?)
        """, (Ing_name,))
        ingredient_id = cursor.lastrowid

    amount = float (input("Mængde: "))
    unit = input("Enhed: ")
    cursor.execute("INSERT INTO RecIng (recipe_id, ingredient_id, amount, unit) VALUES (?, ?, ?, ?)", (recipe_id, ingredient_id, amount, unit))
    return ingredient_id, amount, unit

cursor = connection.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS Recipe (
               id INTEGER PRIMARY KEY NOT NULL, 
               name TEXT, 
               description TEXT, 
               total_time INTEGER,
               directions TEXT,
               category TEXT
               )
               """)

cursor.execute("""CREATE TABLE IF NOT EXISTS Ingredients (
               id INTEGER PRIMARY KEY NOT NULL, 
               name TEXT UNIQUE
               )
               """)

cursor.execute("""CREATE TABLE IF NOT EXISTS RecIng (
               id INTEGER PRIMARY KEY NOT NULL, 
               recipe_id INTEGER, 
               ingredient_id INTEGER,
               amount REAL,
               unit TEXT, 
               FOREIGN KEY(recipe_id) REFERENCES Recipe(id), 
               FOREIGN KEY(ingredient_id) REFERENCES Ingredients(id)
               )
               """)
done = False

while not done:
    choice = input("Vil du tilføje en opskrift? (ja/nej): ").strip().lower()
    if choice == 'ja':
        done = False
        add_recipe()
        recipe_id = cursor.lastrowid
        flere = False
        while not flere:
            more_ingredients = input("Vil du tilføje en ingrediens? (ja/nej): ").strip().lower()
            if more_ingredients == 'ja':
                flere = False
                Ing_name = input("Ingrediens Navn: ")
                add_ingredient()

            elif more_ingredients == 'nej':
                flere = True
            else:
                print("Ugyldigt valg, prøv igen.")

        connection.commit()
    elif choice == 'nej':
        done = True
        print("Afslutter programmet.")
    else:
        print("Ugyldigt valg, prøv igen.")

rows1 = cursor.execute("SELECT id, name, description, total_time, directions, category FROM Recipe").fetchall()
print(rows1)
rows2 = cursor.execute("SELECT id, name FROM Ingredients").fetchall()
print(rows2)
rows3 = cursor.execute("SELECT id, recipe_id, ingredient_id, amount, unit FROM RecIng").fetchall()
print(rows3)

cursor.execute("""
SELECT Recipe.name, Recipe.description, Recipe.total_time, Recipe.directions, Recipe.category, Ingredients.name, RecIng.amount, RecIng.unit
FROM Recipe, Ingredients, RecIng
WHERE Recipe.id = RecIng.recipe_id
AND Ingredients.id = RecIng.ingredient_id
""")
opskrifter = cursor.fetchall()
print("Alle opskrifter: ", opskrifter)

connection.close()
exit()

