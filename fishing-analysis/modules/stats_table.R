library(dplyr)
library(modeest)

calcular_estadisticas <- function(data) {
  tryCatch({
    data <- data[, 1:3]

# Agrupar y contar cuántas veces se cazó cada especie por proyecto
    grouped <- data %>%
      group_by(Proyecto, Especie) %>%
      summarise(Unidades_Cazadas = n(), .groups = "drop")

# Luego, agrupamos por proyecto y calculamos estadísticas sobre esas cantidades
    estadisticas <- grouped %>%
      group_by(Proyecto) %>%
      summarise(
        Media = round(mean(Unidades_Cazadas), 2),
        Mediana = round(median(Unidades_Cazadas), 2),
        Moda = {
          m <- mfv(Unidades_Cazadas)
          if (length(m) > 0) m[1] else NA
        },
        `Desv. Estándar` = round(sd(Unidades_Cazadas), 2),
        Varianza = round(var(Unidades_Cazadas), 2),
        .groups = "drop"
      )

    return(estadisticas)

  }, error = function(e) {
    message(sprintf("No se pudieron generar estadísticas: %s", e$message))
    return(NULL)
  })
}

statsUI <- function(id) {
  ns <- NS(id)
  div(
    style = "display: flex; flex-direction: column; align-items: center; margin-top: 20px;",
    uiOutput(ns("title")),
    tableOutput(ns("table"))
  )
}

statsServer <- function(id, data) {
  moduleServer(id, function(input, output, session) {
    output$title <- renderUI({
      req(data())
      h2("Tabla de estadísticas por proyecto")
    })

    output$table <- renderTable({
      df <- data()
      req(all(c("Proyecto", "Especie") %in% colnames(df)))
      calcular_estadisticas(df)
    })
  })
}
