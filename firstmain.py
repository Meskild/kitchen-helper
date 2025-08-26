import sqlite3

connection = sqlite3.connect('recipe.db')

cursor = connection.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS Recipe (
               id INTEGER PRIMARY KEY NOT NULL, 
               name TEXT, 
               description TEXT, 
               total_time INTEGER
               )
               """)

cursor.execute("""CREATE TABLE IF NOT EXISTS Ingredients (
               id INTEGER PRIMARY KEY NOT NULL, 
               name TEXT UNIQUE
               )"""
               )

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

cursor.execute("INSERT INTO Recipe VALUES (1,'Boller', 'Blød og dejlig', 90)")
cursor.execute("INSERT INTO Recipe VALUES (2,'Pasta Kødsovs', 'Mættende', 45)")

cursor.execute("INSERT INTO Ingredients VALUES (1, 'Pasta')")
cursor.execute("INSERT INTO Ingredients VALUES (2, 'Hakket oksekød')")
cursor.execute("INSERT INTO Ingredients VALUES (3, 'Champinjoner')")
cursor.execute("INSERT INTO Ingredients VALUES (4, 'Tomatpuré')")
cursor.execute("INSERT INTO Ingredients VALUES (5, 'Løg')")
cursor.execute("INSERT INTO Ingredients VALUES (6, 'Pepper')")
cursor.execute("INSERT INTO Ingredients VALUES (7, 'Gær')")
cursor.execute("INSERT INTO Ingredients VALUES (8, 'Mel')")
cursor.execute("INSERT INTO Ingredients VALUES (9, 'Æg')")
cursor.execute("INSERT INTO Ingredients VALUES (10, 'Olie')")
cursor.execute("INSERT INTO Ingredients VALUES (11, 'Salt')")

cursor.execute("INSERT INTO RecIng (recipe_id, ingredient_id, amount, unit) VALUES (1, 7, 50, 'gram')")
cursor.execute("INSERT INTO RecIng (recipe_id, ingredient_id, amount, unit) VALUES (1, 8, 500, 'gram')")
cursor.execute("INSERT INTO RecIng (recipe_id, ingredient_id, amount, unit) VALUES (1, 9, 2, 'stk')")
cursor.execute("INSERT INTO RecIng (recipe_id, ingredient_id, amount, unit) VALUES (1, 10, 100, 'ml')")
cursor.execute("INSERT INTO RecIng (recipe_id, ingredient_id, amount, unit) VALUES (1, 11, 1, 'tsk')")

cursor.execute("INSERT INTO RecIng (recipe_id, ingredient_id, amount, unit) VALUES (2, 11, 2, 'tsk')")
cursor.execute("INSERT INTO RecIng (recipe_id, ingredient_id, amount, unit) VALUES (2, 1, 500, 'gram')")
cursor.execute("INSERT INTO RecIng (recipe_id, ingredient_id, amount, unit) VALUES (2, 2, 400, 'gram')")
cursor.execute("INSERT INTO RecIng (recipe_id, ingredient_id, amount, unit) VALUES (2, 3, 200, 'gram')")
cursor.execute("INSERT INTO RecIng (recipe_id, ingredient_id, amount, unit) VALUES (2, 4, 100, 'gram')")
cursor.execute("INSERT INTO RecIng (recipe_id, ingredient_id, amount, unit) VALUES (2, 5, 1, 'stk')")
cursor.execute("INSERT INTO RecIng (recipe_id, ingredient_id, amount, unit) VALUES (2, 6, 1, 'tsk')")

connection.commit()

rows1 = cursor.execute("SELECT id, name, description, total_time FROM Recipe").fetchall()
print(rows1)
rows2 = cursor.execute("SELECT id, name FROM Ingredients").fetchall()
print(rows2)

cursor.execute("""
SELECT Ingredients.name 
FROM Ingredients
JOIN RecIng ON Ingredients.id = RecIng.ingredient_id
WHERE RecIng.recipe_id = 1
""")
Recipe = cursor.fetchall()
print("Igredienser til Boller:", Recipe)

cursor.execute("""
SELECT Recipe.name 
FROM Recipe
JOIN RecIng ON Recipe.id = RecIng.recipe_id
WHERE RecIng.ingredient_id = 11
""")
Ingredients = cursor.fetchall()
print("?", Ingredients)

cursor.execute("""
SELECT Recipe.name 
FROM Recipe
JOIN RecIng ON Recipe.id = RecIng.recipe_id
JOIN Ingredients ON RecIng.ingredient_id = Ingredients.id
WHERE Ingredients.name = 'Salt' 
""")
Ingredients = cursor.fetchall()
print("??", Ingredients)

cursor.execute("""
SELECT Recipe.name, Ingredients.name, RecIng.amount, RecIng.unit
FROM Recipe, Ingredients, RecIng
WHERE Recipe.id = RecIng.recipe_id 
AND Ingredients.id = RecIng.ingredient_id
AND Ingredients.name = 'Salt' 
""")
Ingredients = cursor.fetchall()
print("???", Ingredients)

connection.close()
print("Database operations completed successfully.")