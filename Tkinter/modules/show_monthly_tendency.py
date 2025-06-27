import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

def mostrar_tendencia_mensual(app):
    if app.df_original is None:
        return

    df = app.df_original.copy()

    if "Fecha" not in df.columns:
        return

    try:
        df["Fecha"] = pd.to_datetime(df["Fecha"], errors="coerce")
        df = df.dropna(subset=["Fecha"])
    except Exception as e:
        return

    df_2024 = df[df["Fecha"].dt.year == 2024].copy()
    if df_2024.empty:
        return

    df_2024["Mes"] = df_2024["Fecha"].dt.month
    df_grouped = df_2024.groupby(["Mes", "Especie"]).size().reset_index(name="Frecuencia")
    if df_grouped.empty:
        return

    # Clean the frame
    for widget in app.frame_tendencia.winfo_children():
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

    canvas_tendencia = FigureCanvasTkAgg(fig, master=app.frame_tendencia)
    canvas_tendencia.draw()
    canvas_tendencia.get_tk_widget().pack(fill="both", expand=True)