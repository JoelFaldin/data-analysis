library(ggplot2)
library(dplyr)

crear_histograma <- function(data, columna_especie) {
  if (missing(data) || missing(columna_especie)) {
    stop("Debes proporcionar un dataframe y el nombre de la columna de especie.")
  }
  
  tabla_frecuencia <- data %>%
    count(.data[[columna_especie]]) %>%
    rename(Especie = 1, Frecuencia = 2) %>%
    arrange(desc(Frecuencia)) %>%
    mutate(Porcentaje = round(100 * Frecuencia / sum(Frecuencia), 1))
  
  grafico <- ggplot(tabla_frecuencia, aes(x = reorder(Especie, -Frecuencia), y = Frecuencia)) +
    geom_bar(stat = "identity", fill = "#2c7fb8") +
    geom_text(aes(label = paste0(Porcentaje, "%")), vjust = -0.5, size = 4) +
    labs(x = "Especie",
         y = "Frecuencia") +
    theme_minimal() +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))
  
  return(grafico)
}

histogramUI <- function(id) {
  ns <- NS(id)
  div(
    style = "display: flex; flex-direction: column; align-items: center; margin-top: 20px;",
    uiOutput(ns("title")),
    plotOutput(ns("plot"), height = "500px", width = "80%")
  )
}

histogramServer <- function(id, data) {
  moduleServer(id, function(input, output, session) {
    output$title <- renderUI({
      req(data())
      h2("Histograma de frecuencia")
    })
    
    output$plot <- renderPlot({
      df <- data()
      req("Especie" %in% colnames(df))
      crear_histograma(df, "Especie")
    })
  })
}