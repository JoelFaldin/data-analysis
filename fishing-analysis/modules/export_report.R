library(dplyr)
library(ggplot2)
library(openxlsx)
library(modeest)

generar_reporte <- function(data, path = "Reporte_Pesca.xlsx") {
  stopifnot(!is.null(data), nrow(data) > 0)
  
  # Frecuencia por especie
  frecuencia <- data %>%
    count(Especie, name = "Frecuencia") %>%
    arrange(desc(Frecuencia))
  
  # Gráfico
  img <- tempfile(fileext = ".png")
  g <- ggplot(frecuencia, aes(x = reorder(Especie, -Frecuencia), y = Frecuencia)) +
    geom_col(fill = "steelblue") +
    geom_text(aes(label = paste0(round(100 * Frecuencia / sum(Frecuencia), 1), "%")), vjust = -0.5) +
    labs(title = "Frecuencia por especie", x = "Especie", y = "Frecuencia") +
    theme_minimal() + theme(axis.text.x = element_text(angle = 45, hjust = 1))
  ggsave(img, g, width = 6, height = 4)
  
  # Estadísticas por proyecto
  resumen <- data %>%
    count(Proyecto, Especie, name = "Unidades") %>%
    group_by(Proyecto) %>%
    summarise(
      Media = mean(Unidades),
      Mediana = median(Unidades),
      Moda = mfv(Unidades)[1],
      `Desv.Estandar` = sd(Unidades),
      Varianza = var(Unidades),
      .groups = "drop"
    )
  
  # Crear workbook y hojas
  wb <- createWorkbook()
  addWorksheet(wb, "Frecuencia")
  addWorksheet(wb, "Estadisticas")
  addWorksheet(wb, "Grafico")
  
  # Escribir datos y agregar imagen
  writeData(wb, "Frecuencia", frecuencia)
  writeData(wb, "Estadisticas", resumen)
  insertImage(wb, "Grafico", img, startRow = 2, startCol = 2, width = 6, height = 4)
  
  # Guardar archivo
  saveWorkbook(wb, path, overwrite = TRUE)
}