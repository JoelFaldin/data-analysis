from tkinter import ttk

from modules.save_excel import save_excel

class SpeciesFrecuencyTable:
  def __init__(self, app, parent):
    self.app = app

    self.tree = ttk.Treeview(parent, columns=("Especie", "Frecuencia"), show="headings")
    self.tree.heading("Especie", text="Especie")
    self.tree.heading("Frecuencia", text="Frecuencia")
    self.tree.pack(expand=True, fill="both")

    frame_botones = ttk.Frame(parent)
    frame_botones.pack(pady=10)
    ttk.Button(frame_botones, text="Guardar tabla como Excel", command=lambda: save_excel(self.app)).pack(side="left", padx=5)

  def populate(self, frecuencia_df):
    # Clear existing data
    for i in self.tree.get_children():
      self.tree.delete(i)
    # Insert new rows
    for _, row in frecuencia_df.iterrows():
      self.tree.insert("", "end", values=(row["Especie"], row["Frecuencia"]))