import tkinter as tk
from tkinter import ttk

from modules.species_frecuency import SpeciesFrecuencyTable
from modules.excel_loader import load_excel
from modules.export_report import exportar_reporte

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

        ttk.Button(self.content_frame, text="Exportar Reporte Completo", command=lambda: exportar_reporte(self)).pack(pady=(10, 0))

        self.frame_tendencia = ttk.Frame(self.content_frame)
        self.frame_tendencia.pack(fill="both", expand=True, pady=(20, 0))

if __name__ == "__main__":
    app = ExcelAnalyzerApp()
    app.mainloop()