import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy import stats

from modules.species_frecuency import SpeciesFrecuencyTable
from modules.excel_loader import load_excel

class ExcelAnalyzerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Análisis de Frecuencia desde Excel")
        self.geometry("900x1000")
        self.configure(padx=10, pady=10)

        self.df_resultado = None
        self.df_estadisticas = None
        self.canvas = None

        # Scroll canvas
        self.scroll_canvas = tk.Canvas(self)
        self.scroll_canvas.pack(fill="both", expand=True, side="left")

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.scroll_canvas.yview)
        scrollbar.pack(fill="y", side="right")

        self.scroll_canvas.configure(yscrollcommand=scrollbar.set)

        self.content_frame = ttk.Frame(self.scroll_canvas)
        # Aquí van los widgets
        ttk.Button(self.content_frame, text="Cargar archivo Excel", command=lambda: load_excel(self)).pack(pady=(0, 10))
        self.species_table = SpeciesFrecuencyTable(self, self.content_frame)
        self.scroll_canvas.create_window((0, 0), window=self.content_frame, anchor="nw")

        self.content_frame.bind(
            "<Configure>",
            lambda e: self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all"))
        )

        self.frame_grafico = ttk.Frame(self.content_frame)
        self.frame_grafico.pack(fill="both", expand=True)

        self.tree_stats = ttk.Treeview(self.frame_grafico, columns=('Proyecto', 'Media', 'Mediana', 'Moda', 'Desviación', 'Varianza'), show='headings')
        for col in ('Proyecto', 'Media', 'Mediana', 'Moda', 'Desviación', 'Varianza'):
            self.tree_stats.heading(col, text=col)
            self.tree_stats.column(col, width=120, anchor='center')

        ttk.Button(self.content_frame, text="Exportar Reporte Completo", command=self.exportar_reporte).pack(pady=(10, 0))

        self.frame_tendencia = ttk.Frame(self.content_frame)
        self.frame_tendencia.pack(fill="both", expand=True, pady=(20, 0))

    def exportar_reporte(self):
        if self.df_resultado is None or self.df_estadisticas is None:
            messagebox.showwarning("Aviso", "Primero debes cargar un archivo.")
            return

        filepath = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Archivo Excel", "*.xlsx")],
            title="Guardar Reporte"
        )

        if not filepath:
            return

        try:
            with pd.ExcelWriter(filepath, engine='xlsxwriter') as writer:
                self.df_resultado.to_excel(writer, sheet_name="Frecuencia", index=False)

                df_stats = pd.DataFrame(self.df_estadisticas, columns=['Proyecto', 'Media', 'Mediana', 'Moda', 'Desviación', 'Varianza'])
                df_stats.to_excel(writer, sheet_name="Estadísticas", index=False)

                workbook = writer.book
                worksheet = workbook.add_worksheet("Gráfico")
                writer.sheets["Gráfico"] = worksheet

                img_path = "grafico_temp.png"
                fig = self.canvas.figure
                fig.savefig(img_path)
                worksheet.insert_image('B2', img_path)

            if os.path.exists("grafico_temp.png"):
                os.remove("grafico_temp.png")

            messagebox.showinfo("Éxito", "Reporte exportado correctamente.")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar el reporte:\n{e}")

    def mostrar_tendencia_mensual(self):
        if self.df_original is None:
            return

        df = self.df_original.copy()

        if "Fecha" not in df.columns:
            return

        try:
            df["Fecha"] = pd.to_datetime(df["Fecha"], errors="coerce")
            df = df.dropna(subset=["Fecha"])
        except Exception:
            return

        df_2024 = df[df["Fecha"].dt.year == 2024].copy()
        if df_2024.empty:
            return

        df_2024["Mes"] = df_2024["Fecha"].dt.month
        df_grouped = df_2024.groupby(["Mes", "Especie"]).size().reset_index(name="Frecuencia")
        if df_grouped.empty:
            return

        for widget in self.frame_tendencia.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(8, 4))

        for especie in df_grouped["Especie"].unique():
            datos = df_grouped[df_grouped["Especie"] == especie]
            ax.plot(datos["Mes"], datos["Frecuencia"], marker='o', label=especie)

        ax.set_title("Tendencia Mensual de Pesca - Año 2024", fontsize=14)
        ax.set_xlabel("Mes")
        ax.set_ylabel("Frecuencia")
        ax.set_xticks(range(1, 13))
        ax.set_xticklabels(['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun',
                            'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'])
        ax.legend()
        ax.grid(True)
        plt.tight_layout()

        canvas_tendencia = FigureCanvasTkAgg(fig, master=self.frame_tendencia)
        canvas_tendencia.draw()
        canvas_tendencia.get_tk_widget().pack(fill="both", expand=True)

if __name__ == "__main__":
    app = ExcelAnalyzerApp()
    app.mainloop()