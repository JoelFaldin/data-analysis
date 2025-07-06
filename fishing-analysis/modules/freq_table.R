freqTableUI <- function(id) {
  ns <- NS(id)
  div(
    style = "display: flex; flex-direction: column; align-items: center;",
    uiOutput(ns("title")),
    tableOutput(ns("table"))
  )
}

freqTableServer <- function(id, data) {
  moduleServer(id, function(input, output, session) {
    output$title <- renderUI({
      req(data())
      h2("Tabla de frecuencias")
    })
    
    output$table <- renderTable({
      df <- data()
      freq <- table(df$Especie)
      freq_df <- as.data.frame(freq)
      colnames(freq_df) <- c("Especie", "Frecuencia")
      freq_df <- freq_df %>% arrange(desc(Frecuencia))
      freq_df
    })
  })
}
