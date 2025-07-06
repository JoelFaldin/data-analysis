library(shiny)
library(dplyr)

source("modules/freq_table.R")
source("modules/histogram_graph.R")
source("modules/stats_table.R")

ui <- fluidPage(
  titlePanel(
    h1("Análisis de frecuencia desde Excel", align = "center")
  ),
  
  fluidRow(
    column(
      width = 6, offset = 3,
      fileInput("file", "Cargar archivo Excel", width = "100%"),
      selectInput(
        "view_choice",
        "Selecciona el gráfico",
        choices = c(
          "Tabla de frecuencia" = "frequency",
          "Histograma de frecuencia" = "histogram",
          "Tabla de estadísticas" = "stats",
          "Tendencia mensual" = "tendency"
        ),
        width = "100%"
      )
    )
  ),
  
  fluidRow(
    column(
      width = 10, offset = 1,
      conditionalPanel(
        condition = "input.view_choice == 'frequency'",
        freqTableUI("freq")
      ),
      conditionalPanel(
        condition = "input.view_choice == 'histogram'", 
        histogramUI("hist")
      ),
      conditionalPanel(
        condition = "input.view_choice == 'stats'", 
        statsUI("stats")
      ),
    )
  )
)

server <- function(input, output) {
  data <- reactive({
    req(input$file)
    readxl::read_excel(input$file$datapath)
  })
  
  freqTableServer("freq", data)
  histogramServer("hist", data)
  statsServer("stats", data)
}

shinyApp(ui, server)