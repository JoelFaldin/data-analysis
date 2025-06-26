from tkinter import filedialog, messagebox
import pandas as pd
import os

def exportar_reporte(app):
    if app.df_resultado is None or app.df_estadisticas is None:
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
            app.df_resultado.to_excel(writer, sheet_name="Frecuencia", index=False)

            df_stats = pd.DataFrame(app.df_estadisticas, columns=['Proyecto', 'Media', 'Mediana', 'Moda', 'Desviación', 'Varianza'])
            df_stats.to_excel(writer, sheet_name="Estadísticas", index=False)

            workbook = writer.book
            worksheet = workbook.add_worksheet("Gráfico")
            writer.sheets["Gráfico"] = worksheet

            img_path = "grafico_temp.png"
            fig = app.canvas.figure
            fig.savefig(img_path)
            worksheet.insert_image('B2', img_path)

        if os.path.exists("grafico_temp.png"):
            os.remove("grafico_temp.png")

        messagebox.showinfo("Éxito", "Reporte exportado correctamente.")

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo exportar el reporte:\n{e}")
