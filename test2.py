import tkinter as tk

def hent_data():
    # Henter fra Entry
    navn = entry_navn.get()
    
    # Henter fra Text (fra linje 1, tegn 0 til slut)
    beskrivelse = text_beskrivelse.get("1.0", tk.END).strip()
    
    label_output.config(text=f"Navn: {navn}\nBeskrivelse:\n{beskrivelse}")

root = tk.Tk()
root.title("Entry vs Text")

# Entry (en linje)
tk.Label(root, text="Navn (Entry):").pack()
entry_navn = tk.Entry(root, width=40)
entry_navn.pack(pady=5)

# Text (flere linjer)
tk.Label(root, text="Beskrivelse (Text):").pack()
text_beskrivelse = tk.Text(root, width=40, height=5)
text_beskrivelse.pack(pady=5)

# Knap til at hente data
btn = tk.Button(root, text="Hent data", command=hent_data)
btn.pack(pady=10)

# Output label
label_output = tk.Label(root, text="", anchor="w", justify="left")
label_output.pack(pady=10, fill="x")

root.mainloop()
