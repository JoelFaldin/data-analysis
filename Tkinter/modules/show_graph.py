from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def mostrar_grafico(app):
  if app.df_resultado is None:
    messagebox.showwarning("Aviso", "Primero debes cargar un archivo.")
    return

  df = app.df_resultado
  total = df["Frecuencia"].sum()
  porcentajes = (df["Frecuencia"] / total) * 100

  if app.canvas:
    app.canvas.get_tk_widget().destroy()

  fig, ax = plt.subplots(figsize=(6, 4))
  bars = ax.bar(df["Especie"], df["Frecuencia"], color="skyblue", edgecolor="black")

  ax.set_title("Frecuencia de pesca por especie", fontsize=14)
  ax.set_xlabel("Especie", fontsize=12)
  ax.set_ylabel("Frecuencia", fontsize=12)

  for bar, porcentaje in zip(bars, porcentajes):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, height + 0.5,
        f"{porcentaje:.1f}%", ha='center', va='bottom', fontsize=10)

  plt.xticks(rotation=45)
  plt.tight_layout()

  app.canvas = FigureCanvasTkAgg(fig, master=app.frame_grafico)
  app.canvas.draw()
  app.canvas.get_tk_widget().pack(fill="both", expand=True)

  for i in app.tree_stats.get_children():
    app.tree_stats.delete(i)
  for row in app.df_estadisticas:
    app.tree_stats.insert('', 'end', values=row)

  app.tree_stats.pack(fill='x', padx=10, pady=10)
