from tkinter import messagebox
from scipy import stats

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
