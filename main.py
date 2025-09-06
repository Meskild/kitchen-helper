import sqlite3
import tkinter as tk

connection = sqlite3.connect('cookbook.db')

cursor = connection.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS Recipe (
               id INTEGER PRIMARY KEY NOT NULL, 
               name TEXT, 
               description TEXT,
               total_time INTEGER,
               directions TEXT,
               category_id INTEGER,
               FOREIGN KEY(category_id) REFERENCES Category(id)
               )
               """)

cursor.execute("""CREATE TABLE IF NOT EXISTS Category (
               id INTEGER PRIMARY KEY NOT NULL, 
               category TEXT UNIQUE
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

# Midlertidig liste til ingredienser
current_ingridiens = []

# Tilføj opskriften til databasen
def add_recipe():
    rec_name = entry_rec_name.get()  # hent tekst fra tekstfelt
    rec_total_time = entry_rec_total_time.get() 
    rec_category = entry_rec_category.get()
    rec_description = text_rec_description.get("1.0", tk.END).strip()
    rec_directions = text_rec_directions.get("1.0", tk.END).strip()  
    label_output.config(text=f"Tilføjet {rec_name}, {rec_description}, {rec_total_time}, {rec_directions}, {rec_category}")  # skriv det i labelen
    
    cursor.execute("""
    SELECT id FROM Category WHERE category = ?
    """, (rec_category,))
    result = cursor.fetchone()
    if result:
        category_id = result[0]
    else:
        cursor.execute("""
        INSERT INTO Category (category) VALUES (?)
        """, (rec_category,))
        category_id = cursor.lastrowid

    cursor.execute("INSERT INTO Recipe (name, description, total_time, directions, category_id) VALUES (?, ?, ?, ?, ?)",
                    (rec_name, rec_description, rec_total_time, rec_directions, category_id))
    rec_id = cursor.lastrowid

    
    # Når vi trykker "Gem" tager vi hele listen
    for ing_name, ing_amount, ing_unit in current_ingridiens:
        # 1. Tjek om ingrediensen allerede findes
        cursor.execute("SELECT id FROM Ingredients WHERE name = ?", (ing_name,))
        result = cursor.fetchone()
        if result:
            ingredient_id = result[0]
        else:
            cursor.execute("INSERT INTO Ingredients (name) VALUES (?)", (ing_name,))
            ingredient_id = cursor.lastrowid

        # 2. Gem koblingen mellem opskrift og ingrediens
        cursor.execute(
            "INSERT INTO RecIng (recipe_id, ingredient_id, amount, unit) VALUES (?, ?, ?, ?)",
            (rec_id, ingredient_id, ing_amount, ing_unit)
        )
        
    connection.commit()
    entry_rec_name.delete(0, tk.END)
    text_rec_description.delete(1.0, tk.END)
    entry_rec_total_time.delete(0, tk.END)
    text_rec_directions.delete(1.0, tk.END)
    entry_rec_category.delete(0, tk.END)
    listbox.delete(0, tk.END)
    recipe_list.delete(0, tk.END)

    cursor.execute("SELECT name FROM Recipe")
    rows = cursor.fetchall()
    for row in rows:
        recipe_list.insert(tk.END, row[0])

def add_ingredient():
    ing_name = entry_ing_name.get()  # hent tekst fra tekstfelt
    ing_amount = entry_ing_amount.get() 
    ing_unit = entry_ing_unit.get()
    
    # Gem i listen
    current_ingridiens.append((ing_name, ing_amount, ing_unit))

    # Vis det i GUI (så vi kan se hvad der er i "hukommelsen")
    listbox.insert(tk.END, f"{ing_name} - {ing_amount} - {ing_unit}")

    entry_ing_name.delete(0, tk.END)
    entry_ing_amount.delete(0, tk.END)
    entry_ing_unit.delete(0, tk.END)

    current_ingridiens.clear()

    # return ingredient_id, ing_amount, ing_unit

# Lav hovedvinduet
root = tk.Tk()
root.title("Kitchen Helper")
root.geometry("1920x1080")  # bredde x højde

frame_recipe = tk.LabelFrame(root, text="Opskrift")
frame_recipe.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

# Et tekstfelt hvor man kan skrive
tk.Label(frame_recipe, text="Opskriftens Navn:").grid(row=0, column=0, sticky="w")
entry_rec_name = tk.Entry(frame_recipe, width=40)
entry_rec_name.grid(row=0, column=1, pady=5)

tk.Label(frame_recipe, text="Total Tid:").grid(row=1, column=0, sticky="w")
entry_rec_total_time = tk.Entry(frame_recipe, width=40)
entry_rec_total_time.grid(row=1, column=1, pady=5)

tk.Label(frame_recipe, text="Kategori:").grid(row=2, column=0, sticky="w")
entry_rec_category = tk.Entry(frame_recipe, width=40)
entry_rec_category.grid(row=2, column=1, pady=5)

tk.Label(frame_recipe, text="Beskrivelse:").grid(row=3, column=0, sticky="w")
text_rec_description = tk.Text(frame_recipe, height=10, width=40)
text_rec_description.grid(row=3, column=1, pady=5)

tk.Label(frame_recipe, text="Vejledning:").grid(row=4, column=0, sticky="w")
text_rec_directions = tk.Text(frame_recipe, height=10, width=40)
text_rec_directions.grid(row=4, column=1, pady=5)

# Ramme til "ingredienser" (vandret)
frame_ingredient = tk.LabelFrame(root, text="Ingredienser")
frame_ingredient.grid(row=0, column=1, padx=10, pady=10, sticky="nw")

tk.Label(frame_ingredient, text="Ingrediens:").grid(row=1, column=0, padx=5)
entry_ing_name = tk.Entry(frame_ingredient, width=40)
entry_ing_name.grid(row=1, column=1, pady=5)

tk.Label(frame_ingredient, text="mængde:").grid(row=2, column=0, padx=5)
entry_ing_amount = tk.Entry(frame_ingredient, width=40)
entry_ing_amount.grid(row=2, column=1, pady=5)

tk.Label(frame_ingredient, text="Enhed:").grid(row=3, column=0, padx=5)
entry_ing_unit = tk.Entry(frame_ingredient, width=40)
entry_ing_unit.grid(row=3, column=1, pady=5)

# Ramme til "Tilføjet ingredienser"
frame_ingredients = tk.LabelFrame(root, text="Tilføjet Ingredienser")
frame_ingredients.grid(row=0, column=2, padx=10, pady=10, sticky="nw")

listbox = tk.Listbox(frame_ingredients, width=40)
listbox.grid(row=0, column=0, columnspan=2)

# En knap der kalder funktionen add_recipe
button = tk.Button(root, text="Opret", command=add_recipe)
button.grid(row=2, column=0, pady=20)

# En knap der kalder funktionen add_ingredient
button = tk.Button(frame_ingredient, text="Tilføj", command=add_ingredient)
button.grid(row=7, column=0, pady=20)

# En label til at vise output
label_output = tk.Label(root, text="")
label_output.grid(row=3, column=0, pady=20)

# Ramme til "Tilføjet Opskrifter"
frame_recipes = tk.LabelFrame(root, text="Tilføjet Opskrifter")
frame_recipes.grid(row=0, column=3, padx=10, pady=10, sticky="nw")

recipe_list = tk.Listbox(frame_recipes, width=40)
recipe_list.grid(row=0, column=0, columnspan=2)

cursor.execute("SELECT name FROM Recipe")
rows = cursor.fetchall()
for row in rows:
    recipe_list.insert(tk.END, row[0])

# Start GUI'ens event-loop
root.mainloop()

connection.close()
exit()

