import tkinter as tk

root = tk.Tk()
root.title("Eksempel med grid layout")
root.geometry("600x400")

# Ramme til "opskrift" felter (lodret)
frame_recipe = tk.LabelFrame(root, text="Opskrift")
frame_recipe.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

tk.Label(frame_recipe, text="Navn:").grid(row=0, column=0, sticky="w")
entry_name = tk.Entry(frame_recipe)
entry_name.grid(row=0, column=1, pady=5)

tk.Label(frame_recipe, text="Beskrivelse:").grid(row=1, column=0, sticky="w")
entry_desc = tk.Entry(frame_recipe)
entry_desc.grid(row=1, column=1, pady=5)

tk.Label(frame_recipe, text="Tid (min):").grid(row=2, column=0, sticky="w")
entry_time = tk.Entry(frame_recipe)
entry_time.grid(row=2, column=1, pady=5)

# Ramme til "ingredienser" (vandret)
frame_ingredients = tk.LabelFrame(root, text="Ingredienser")
frame_ingredients.grid(row=1, column=0, padx=10, pady=10, sticky="nw")

tk.Label(frame_ingredients, text="Ingrediens:").grid(row=0, column=0, padx=5)
entry_ing = tk.Entry(frame_ingredients, width=20)
entry_ing.grid(row=0, column=1, padx=5)

tk.Label(frame_ingredients, text="Mængde:").grid(row=0, column=2, padx=5)
entry_amount = tk.Entry(frame_ingredients, width=10)
entry_amount.grid(row=0, column=3, padx=5)

tk.Label(frame_ingredients, text="Enhed:").grid(row=0, column=4, padx=5)
entry_unit = tk.Entry(frame_ingredients, width=10)
entry_unit.grid(row=0, column=5, padx=5)

listbox = tk.Listbox(root)
listbox.grid(row=0, column=0, columnspan=2)

# En knap nederst
btn_save = tk.Button(root, text="Gem opskrift")
btn_save.grid(row=2, column=0, pady=20)

root.mainloop()
