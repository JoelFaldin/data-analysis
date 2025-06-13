import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt

class ExcelAnalyzerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Análisis de Frecuencia desde Excel")
        self.geometry("600x400")
        self.configure(padx=10, pady=10)

        self.df_resultado = None  # Guardar resultados

        self.create_widgets()

    def create_widgets(self):
        # Botón para cargar archivo
        ttk.Button(self, text="Cargar archivo Excel", command=self.load_excel).pack(pady=(0, 10))

        # Treeview para mostrar la tabla
        self.tree = ttk.Treeview(self, columns=("Especie", "Frecuencia"), show="headings")
        self.tree.heading("Especie", text="Especie")
        self.tree.heading("Frecuencia", text="Frecuencia")
        self.tree.pack(expand=True, fill="both")

        # Botones para guardar y graficar
        frame_botones = ttk.Frame(self)
        frame_botones.pack(pady=10)

        ttk.Button(frame_botones, text="Guardar tabla como Excel", command=self.save_excel).pack(side="left", padx=5)
        ttk.Button(frame_botones, text="Mostrar gráfico", command=self.mostrar_grafico).pack(side="left", padx=5)

    def load_excel(self, filepath=None):
        if not filepath:
            filepath = filedialog.askopenfilename(
                title="Selecciona un archivo Excel",
                filetypes=[("Archivos Excel", "*.xlsx *.xls *.csv")]
            )
        
        if filepath:
            try:
                df = pd.read_excel(filepath)

                if "Especie" not in df.columns:
                    raise ValueError("El archivo debe contener una columna llamada 'Especie'.")

                frecuencia = df["Especie"].value_counts().reset_index()
                frecuencia.columns = ["Especie", "Frecuencia"]
                self.df_resultado = frecuencia

                # Limpiar Treeview
                for i in self.tree.get_children():
                    self.tree.delete(i)

                # Insertar datos
                for _, row in frecuencia.iterrows():
                    self.tree.insert("", "end", values=(row["Especie"], row["Frecuencia"]))

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo leer el archivo:\n{e}")

    def save_excel(self):
        if self.df_resultado is None:
            messagebox.showwarning("Aviso", "Primero debes cargar un archivo.")
            return

        filepath = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Archivo Excel", "*.xlsx")],
            title="Guardar como"
        )

        if filepath:
            try:
                self.df_resultado.to_excel(filepath, index=False)
                messagebox.showinfo("Éxito", "Archivo guardado correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{e}")

    def mostrar_grafico(self):
        if self.df_resultado is None:
            messagebox.showwarning("Aviso", "Primero debes cargar un archivo.")
            return

        df = self.df_resultado
        total = df["Frecuencia"].sum()
        porcentajes = (df["Frecuencia"] / total) * 100

        fig, ax = plt.subplots(figsize=(12, 8))
        bars = ax.bar(df["Especie"], df["Frecuencia"], color="skyblue", edgecolor="black")

        # Etiquetas
        ax.set_title("Frecuencia de pesca por especie", fontsize=14)
        ax.set_xlabel("Especie", fontsize=12)
        ax.set_ylabel("Frecuencia", fontsize=12)

        # Mostrar porcentaje sobre cada barra
        for bar, porcentaje in zip(bars, porcentajes):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, height + 0.5,
                    f"{porcentaje:.1f}%", ha='center', va='bottom', fontsize=10)

        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    app = ExcelAnalyzerApp()
    app.mainloop()
