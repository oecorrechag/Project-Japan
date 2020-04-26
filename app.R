# Load packages -----------------------------------------------------
library(shiny)
library(tree)
library(rpart)
library(dplyr)
library(networkD3)
library(igraph)

# Load data ---------------------------------------------------------

#data y para primer plot
data <- read.csv("data_modelo.csv", header = T, sep = ",", fileEncoding = "UTF-8")
data2 <- read.csv("Tabla_Nodos.csv", header = T, sep = ",", fileEncoding = "UTF-8")

# Define UI ---------------------------------------------------------

ui <- fluidPage(
    
    headerPanel(title = HTML("MADRES_APP"),
                windowTitle="Felicidad de las Madres Solteras"),
    
    mainPanel(
        tabsetPanel(type = "tabs",
                    
                    tabPanel("Información App", icon = icon("exclamation"),
                             h1("Bienvenido!", align = "center"),
                             p("Este trabajo presenta el análisis de La Encuesta Nacional de Calidad de Vida - ENCV 2019 
                               COLOMBIA, se pretende ajustar una serie de modelos que permitan entender mejor la satisfacción 
                               de las madres solteras con el objetivo de una adecuada toma de decisiones basados en los 
                               resultados obtenidos. La Encuesta Nacional de Calidad de Vida - ENCV 2019 COLOMBIA se compone 
                               de 15 tablas las cuales reúnen información surgen como respuesta a la necesidad de caracterizar 
                               la población en los diferentes aspectos involucrados en el bienestar de los hogares."),
                             strong("Se recomienda usar Google Chrome."),
                             br(),
                             p("Modelo:"),
                             p(strong("- Modelo: "),"En esta pestaña se podra calcular la felicidad."), 
                             p(strong("- Arbol Genealogico: "),"En esta pestaña se podra observar el arbol genealogico de las familias."), 
                             p(strong("- FAQ ")),
                             p(strong("- Actualizaciones")),
                             br(),
                             fluidRow(
                                 column(1,
                                        br()
                                 ),
                                 column(4,
                                        br()
                                 ),
                                 column(3,
                                        br(),br(),
                                        imageOutput("engrane1")
                                 )
                             )
                    ),
                    
                    
                    
                    
                    
                    
                    
                    
                    tabPanel("Modelo", icon = icon("sync"),
                             h1("Modelo para prediccion de la felicidad", align = "center"),
                             
                             
                             fluidRow(
                                 
                                 column(4,
                                        
                                        p(strong('Cual es su nivel de satisfaccion con los siguientes temas:')),
                                        
                                        radioButtons(inputId = "textEconomic",
                                                     label = "Con su ingreso economico:", 
                                                     choices = c("Muy satisfecho",
                                                                 "Satisfecho",
                                                                 "Neutral",
                                                                 "Insatisfecha",
                                                                 "Muy insatisfecha"),
                                                     selected = F),
                                        
                                    
                                        radioButtons(inputId = "textHealth",
                                                     label = "Con los servicios de salud:", 
                                                     choices = c("Muy satisfecho",
                                                                 "Satisfecho",
                                                                 "Neutral",
                                                                 "Insatisfecha",
                                                                 "Muy insatisfecha"),
                                                     selected = F),
                                        
                                        
                                        radioButtons(inputId = "textSecurity",
                                                     label = "Con la seguridad en donde reside:", 
                                                     choices = c("Muy satisfecho",
                                                                 "Satisfecho",
                                                                 "Neutral",
                                                                 "Insatisfecha",
                                                                 "Muy insatisfecha"),
                                                     selected = F)
                                        
                                        
                                        
                                        
                                 ),
                                 
                                 column(4,
                                        
                                        radioButtons(inputId = "textWork",
                                                     label = "Cual es su nivel de satisfaccion con su trabajo:", 
                                                     choices = c("Muy satisfecho",
                                                                 "Satisfecho",
                                                                 "Neutral",
                                                                 "Insatisfecha",
                                                                 "Muy insatisfecha"),
                                                     selected = F),
                                        
                                        
                                        radioButtons(inputId = "textPreocupacion",
                                                 label = "Que tan preocupada se sintio el dia de ayer", 
                                                     choices = c("Nada preocupada",
                                                                 "Poco preocupada",
                                                                 "Neutral",
                                                                 "Preocupada",
                                                                 "Muy preocupada"),
                                                     selected = F),
                                        
                                        
                                        radioButtons(inputId = "textstart",
                                                     label = "En que momento de la vida se siente:", 
                                                     choices = c("El mejor momento",
                                                                 "Cerca a mi mejor momento",
                                                                 "Neutral",
                                                                 "No estoy pasando por mi mejor momento",
                                                                 "Estoy pasando mi peor momento"),
                                                     selected = F)
                                        
                                        
                                        
                                 ),
                                 
                                 column(4,
                                        
                                        numericInput(inputId = "textmoney",
                                                     label = "¿Cual es su ingreso economico?:", 
                                                     value = 600000),
                                        
                                        p(strong('De 0 a 10, siendo 10 el mas alto, 0 el mas bajo, conteste: ')),
                                        
                                        sliderInput(inputId = "textLive",
                                                    label = "¿Que tan satisfecho se siente con su vida?:",
                                                    value = 10, min = 1, max = 10),
                                        
                                        sliderInput(inputId = "textSad",
                                                    label = "¿Que tan triste se sintio ayer?:",
                                                    value = 10, min = 1, max = 10),
                                        
                                        sliderInput(inputId = "textTranquility", 
                                                    label = "¿Cual es su deseo de seguir viviendo?:",
                                                    value = 10, min = 1, max = 10),
                                        
                                        
                                        
                                        
                                
                                        
                                        
                                        tags$head(
                                            tags$style
                                            (
                                                HTML
                                                (
                                                    '#run{background-color:#8BC5ED}'
                                                )
                                            ) 
                                        ),
                                        actionButton("run","Run Analysis"),
                                        p(strong('La felicidad es de :')),
                                        textOutput("resultPredicction")
                                 )
                            
                             )
                    ), 
                    
                    
                    
                    
                    
                    
                      tabPanel("Arbol Genealogico", icon = icon("stream"),
                             h1("Estructura de los hogares de las madres solteras", align = "center"),
                             
                             
                             fluidRow(
                                 # Cuadro de ingreso de numero
                                 numericInput("numero_hogar", h5("Ingrese el codigo pertinente:"),
                                              value = 1, min = 1, max = 15414),
                                 
                                 
                                 
                                 # Grafico generado
                                 simpleNetworkOutput(outputId="hogares_grafico")
                             )
                    ), 
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    tabPanel("FAQ", icon = icon("paperclip"),
                             h1("FAQ", align = "center"),
                             p(strong("- Fuente 1:"), "Datos tomados del Archivo Nacional de Datos pertenecientes a la encuesta de calidad de vida 2018", 
                               em("Tomado de: "), 
                               tags$a(href="http://microdatos.dane.gov.co/index.php/catalog/607/datafile", "ANDA.COM")),
                             
                             hr()
                    ),
                    
                    
                    
                    tabPanel("Updates", icon = icon("wrench"),
                             h1("Actualizaciones", align = "center"),
                             strong("October 9, 2018"),
                             p("Creacion de App."),
                             hr(),
                             strong("April 20, 2020"),
                             p("Actualizacion de modelo con los datos del 2019."),
                             hr(),
                             fluidRow(
                                 column(4,
                                        br(),br()
                                 ),
                                 column(4,
                                        imageOutput("gancho1")
                                 )
                             )
                    )
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
        )
    )
)

server <- function(input, output, ...) {
    
    
    #### Transformacion de variables --------------------------------------
    
    economiama <- reactive({
        switch(input$textEconomic,
               "Muy insatisfecha" = 10,
               "Insatisfecha" = 8,
               "Neutral" = 6,
               "Satisfecho" = 4,
               "Muy satisfecho" = 2
               
        )
    })
    
    
    saludma <- reactive({
        switch(input$textHealth,
               "Muy insatisfecha" = 2,
               "Insatisfecha" = 4,
               "Neutral" = 6,
               "Satisfecho" = 8,
               "Muy satisfecho" = 10
               
        )
    })
    
    
    seguridadma <- reactive({
        switch(input$textSecurity,
               "Muy insatisfecha" = 2,
               "Insatisfecha" = 4,
               "Neutral" = 6,
               "Satisfecho" = 8,
               "Muy satisfecho" = 10
               
        )
    })
    
    
    trabajoma <- reactive({
        switch(input$textWork,
               "Muy insatisfecha" = 2,
               "Insatisfecha" = 4,
               "Neutral" = 6,
               "Satisfecho" = 8,
               "Muy satisfecho" = 10
               
        )
    })
    
    
    preocupadama <- reactive({
        switch(input$textPreocupacion,
               "Muy preocupada" = 10,
               "Preocupada" = 8,
               "Neutral" = 6,
               "Poco preocupada" = 4,
               "Nada preocupada" = 2
               
        )
    })
    
    
    escalonma <- reactive({
        switch(input$textstart,
               "El mejor momento" = 10,
               "Cerca a mi mejor momento" = 8,
               "Neutral" = 6,
               "No estoy pasando por mi mejor momento" = 4,
               "Estoy pasando mi peor momento" = 2
        )
    })


    
    ##### Modelo ---------------------------------------------------
    
    
    modelo <- lm(Felicidad ~  Satisfaccion_economica + 
                                Satisfaccion_salud + 
                                Satisfaccion_seguridad +
                                Satisfaccion_trabajo +
                                Preocupacion +
                                Escalon_vida +
                                Ingreso_Hogares +
                                Satisfaccion_vida +
                                Tristeza +
                                Deseo_vivir,
                        data = data)
    
    
    
    
    observeEvent(input$run,{
        
        ##### Prediccion  ----------------------------------------------
        
        p <- predict(object = modelo,
                     newdata = data.frame(Satisfaccion_economica = economiama(),
                                          Satisfaccion_salud = saludma(),
                                          Satisfaccion_seguridad = seguridadma(),
                                          Satisfaccion_trabajo = trabajoma(),
                                          Preocupacion = preocupadama(),
                                          Escalon_vida = escalonma(),
                                          Ingreso_Hogares = input$textmoney,
                                          Satisfaccion_vida = input$textLive,
                                          Tristeza = (1 - (input$textSad)),
                                          Deseo_vivir = input$textTranquility
                                          ),
                     )
        
        output$resultPredicction <- renderText({ 
            
            print((p/13)*10)
            
            })
    })
    
    
    
    
    
    ##### Grafico ----------------------------------------------------------
    
    
    output$hogares_grafico <- renderSimpleNetwork({
        
        familia <- filter(data2, num_fam == input$numero_hogar)
        
        networkData <- data.frame(familia$from, familia$to)
        
        simpleNetwork(networkData, opacity = 10000, fontSize = familia$Edad,
                      zoom = T)
        
        
        
        
    })
    
     
    
}

shinyApp(ui, server)
