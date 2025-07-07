library(ggplot2)
library(dplyr)
library(lubridate)

crear_tendencia <- function(data) {
  if (!"Fecha" %in% colnames(data) || !"Especie" %in% colnames(data)) {
    stop("El archivo no contiene datos!")
  }
  
  data <- data %>%
    mutate(Fecha = suppressWarnings(lubridate::ymd(Fecha))) %>%
    filter(!is.na(Fecha)) %>%
    filter(year(Fecha) == 2024) %>%
    mutate(Mes = month(Fecha))
  
  if (nrow(data) == 0) {
    stop("No hay datos que mostrar!")
  }
  
  df_grouped <- data %>%
    group_by(Mes, Especie) %>%
    summarise(Frecuencia = n(), .groups = "drop")
  
  if (nrow(df_grouped) == 0) {
    stop("No hay grupos!")
  }
  
  meses <- c("Ene", "Feb", "Mar", "Abr", "May", "Jun",
             "Jul", "Ago", "Sep", "Oct", "Nov", "Dic")
  
  ggplot(df_grouped, aes(x = Mes, y = Frecuencia, color = Especie)) +
    geom_line(size = 1.2) +
    geom_point(size = 2) +
    scale_x_continuous(breaks = 1:12, labels = meses) +
    labs(x = "Mes", y = "Frecuencia", color = "Especie") +
    theme_minimal() +
    theme(
      text = element_text(size = 12),
      axis.text.x = element_text(angle = 0),
      plot.title = element_text(hjust = 0.5)
    )
}

monthlyTendencyUI <- function(id) {
  ns <- NS(id)
  div(
    style = "display: flex; flex-direction: column; align-items: center; margin-top: 20px;",
    uiOutput(ns("title")),
    plotOutput(ns("tendencyPlot"), height = "500px", width = "90%")
  )
}

monthlyTendencyServer <- function(id, data) {
  moduleServer(id, function(input, output, session) {
    output$title <- renderUI({
      req(data())
      h2("Tendencia mensual por especie (2024)")
    })
    
    output$tendencyPlot <- renderPlot({
      df <- data()
      crear_tendencia(df)
    })
  })
}
