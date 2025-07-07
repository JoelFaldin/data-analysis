library(shiny)
library(dplyr)

source("modules/freq_table.R")
source("modules/histogram_graph.R")
source("modules/stats_table.R")
source("modules/monthly_tendency.R")
source("modules/export_report.R")

ui <- fluidPage(
  titlePanel(
    h1("Análisis de frecuencia desde Excel", align = "center")
  ),
  
  fluidRow(
    column(
      width = 6, offset = 3,
      fileInput("file", "Cargar archivo Excel", width = "100%"),
      
      downloadButton("download_report", "Exportar reporte completo", class = "btn btn-primary", style = "width: 100%; margin-bottom: 10px;"),
      
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
      conditionalPanel(
        condition = "input.view_choice == 'tendency'", 
        monthlyTendencyUI("trend")
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
  monthlyTendencyServer("trend", data)
  
  output$download_report <- downloadHandler(
    filename = function() {
      paste0("Reporte_Pesca_", Sys.Date(), ".xlsx")
    },
    content = function(file) {
      df <- data()
      req(df)
      
      tryCatch({
        generar_reporte(df, file)
      }, error = function(e) {
        showModal(modalDialog(
          title = "Error al generar el reporte",
          paste("Ocurrió un error:", e$message),
          easyClose = TRUE
        ))
      })
    }
  )
  
}

shinyApp(ui, server)