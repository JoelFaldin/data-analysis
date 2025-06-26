from tkinter import messagebox, filedialog

def save_excel(app):
  if app.df_resultado is None:
    messagebox.showwarning("Aviso", "Primero debes cargar un archivo.")
    return

  filepath = filedialog.asksaveasfilename(
    defaultextension=".xlsx",
    filetypes=[("Archivo Excel", "*.xlsx")],
    title="Guardar como"
  )

  if filepath:
    try:
      app.df_resultado.to_excel(filepath, index=False)
      messagebox.showinfo("Éxito", "Archivo guardado correctamente.")
    except Exception as e:
      messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{e}")