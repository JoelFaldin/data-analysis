import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy import stats

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
        self.scroll_canvas.create_window((0, 0), window=self.content_frame, anchor="nw")

        self.content_frame.bind(
            "<Configure>",
            lambda e: self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all"))
        )

        # Aquí van los widgets
        ttk.Button(self.content_frame, text="Cargar archivo Excel", command=self.load_excel).pack(pady=(0, 10))

        self.tree = ttk.Treeview(self.content_frame, columns=("Especie", "Frecuencia"), show="headings")
        self.tree.heading("Especie", text="Especie")
        self.tree.heading("Frecuencia", text="Frecuencia")
        self.tree.pack(expand=True, fill="both")

        frame_botones = ttk.Frame(self.content_frame)
        frame_botones.pack(pady=10)
        ttk.Button(frame_botones, text="Guardar tabla como Excel", command=self.save_excel).pack(side="left", padx=5)

        self.frame_grafico = ttk.Frame(self.content_frame)
        self.frame_grafico.pack(fill="both", expand=True)

        self.tree_stats = ttk.Treeview(self.frame_grafico, columns=('Proyecto', 'Media', 'Mediana', 'Moda', 'Desviación', 'Varianza'), show='headings')
        for col in ('Proyecto', 'Media', 'Mediana', 'Moda', 'Desviación', 'Varianza'):
            self.tree_stats.heading(col, text=col)
            self.tree_stats.column(col, width=120, anchor='center')

        ttk.Button(self.content_frame, text="Exportar Reporte Completo", command=self.exportar_reporte).pack(pady=(10, 0))

        self.frame_tendencia = ttk.Frame(self.content_frame)
        self.frame_tendencia.pack(fill="both", expand=True, pady=(20, 0))

    def load_excel(self, filepath=None):
        if not filepath:
            filepath = filedialog.askopenfilename(
                title="Selecciona un archivo Excel o CSV",
                filetypes=[("Archivos Excel y CSV", "*.xlsx *.xls *.csv")]
            )

        if filepath:
            try:
                ext = os.path.splitext(filepath)[1].lower()
                df = pd.read_csv(filepath) if ext == ".csv" else pd.read_excel(filepath)

                if "Especie" not in df.columns or "Fecha" not in df.columns:
                    raise ValueError("El archivo debe contener columnas 'Fecha' y 'Especie'.")

                self.df_original = df.copy()

                frecuencia = df["Especie"].value_counts().reset_index()
                frecuencia.columns = ["Especie", "Frecuencia"]
                self.df_resultado = frecuencia

                for i in self.tree.get_children():
                    self.tree.delete(i)
                for _, row in frecuencia.iterrows():
                    self.tree.insert("", "end", values=(row["Especie"], row["Frecuencia"]))

                self.generar_estadisticas(df)
                self.mostrar_grafico()
                self.mostrar_tendencia_mensual()

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo leer el archivo:\n{e}")

    def generar_estadisticas(self, df):
        try:
            df = df.iloc[:, :3]
            grouped = df.groupby(['Proyecto', 'Especie']).size().reset_index(name='Unidades_Cazadas')

            stats_list = []
            for proyecto, grupo in grouped.groupby('Proyecto'):
                cantidades = grupo['Unidades_Cazadas']
                media = cantidades.mean()
                mediana = cantidades.median()
                try:
                    moda = stats.mode(cantidades, keepdims=True).mode[0]
                except:
                    moda = "No definida"
                desviacion = cantidades.std()
                varianza = cantidades.var()

                stats_list.append([proyecto, round(media, 2), round(mediana, 2), moda, round(desviacion, 2), round(varianza, 2)])

            self.df_estadisticas = stats_list

        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron generar estadísticas:\n{e}")

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

        if self.canvas:
            self.canvas.get_tk_widget().destroy()

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

        self.canvas = FigureCanvasTkAgg(fig, master=self.frame_grafico)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        for i in self.tree_stats.get_children():
            self.tree_stats.delete(i)
        for row in self.df_estadisticas:
            self.tree_stats.insert('', 'end', values=row)

        self.tree_stats.pack(fill='x', padx=10, pady=10)

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