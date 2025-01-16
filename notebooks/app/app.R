# Load packages -----------------------------------------------------
library(shiny)
library(tree)
library(rpart)
library(dplyr)
library(networkD3)
library(igraph)

# Load data ---------------------------------------------------------

# data y para primer plot
cerchas <- read.csv("cerchas.csv",
    header = T,
    sep = ",",
    fileEncoding = "UTF-8"
)
directorio_vector <- cerchas$DIRECTORIO
directorio_lista <- unique(directorio_vector)

# Define UI ---------------------------------------------------------

ui <- fluidPage(
    headerPanel(
        title = HTML("Análisis de la Felicidad"),
        windowTitle = "Análisis de la Felicidad"
    ),
    mainPanel(
        tabsetPanel(
            type = "tabs",
            tabPanel("Información App",
                icon = icon("exclamation"),
                h1("Bienvenido!", align = "center"),
                p("La felicidad es un concepto subjetivo que abarca diversos aspectos de la vida, como la satisfacción personal, 
                el bienestar emocional y la calidad de las relaciones interpersonales. En el caso de las madres solteras, 
                este tema adquiere una relevancia especial debido a los desafíos únicos que enfrentan, como la responsabilidad de 
                criar a sus hijos en solitario, equilibrar trabajo y familia, y manejar factores económicos y sociales que pueden 
                influir en su bienestar general. Este proyecto tiene como objetivo explorar y analizar los factores que contribuyen 
                a la felicidad de las madres solteras, utilizando técnicas de ciencia de datos para identificar patrones, 
                correlaciones y posibles intervenciones que promuevan su bienestar."),
                strong("Se recomienda usar Google Chrome."),
                br(),
                p("Modelo:"),
                p(strong("- Modelo: "), "En esta pestaña se podra calcular la felicidad."),
                p(strong("- Arbol Genealogico: "), "En esta pestaña se podra observar el arbol genealogico de las familias."),
                p(strong("- FAQ ")),
                p(strong("- Actualizaciones")),
                br(),
                fluidRow(
                    column(
                        1,
                        br()
                    ),
                    column(
                        4,
                        br()
                    ),
                    column(
                        3,
                        br(), br(),
                        imageOutput("engrane1")
                    )
                )
            ),
            tabPanel("Modelo",
                icon = icon("sync"),
                h1("Factores Determinantes en Madres Solteras", align = "center"),
                fluidRow(
                    column(
                        4,
                        p(strong("Cual es su nivel de satisfaccion con los siguientes temas:")),
                        radioButtons(
                            inputId = "textEconomic",
                            label = "Con su ingreso economico:",
                            choices = c(
                                "Muy satisfecho",
                                "Satisfecho",
                                "Neutral",
                                "Insatisfecha",
                                "Muy insatisfecha"
                            ),
                            selected = F
                        ),
                        radioButtons(
                            inputId = "textHealth",
                            label = "Con los servicios de salud:",
                            choices = c(
                                "Muy satisfecho",
                                "Satisfecho",
                                "Neutral",
                                "Insatisfecha",
                                "Muy insatisfecha"
                            ),
                            selected = F
                        ),
                        radioButtons(
                            inputId = "textSecurity",
                            label = "Con la seguridad en donde reside:",
                            choices = c(
                                "Muy satisfecho",
                                "Satisfecho",
                                "Neutral",
                                "Insatisfecha",
                                "Muy insatisfecha"
                            ),
                            selected = F
                        )
                    ),
                    column(
                        4,
                        radioButtons(
                            inputId = "textWork",
                            label = "Cual es su nivel de satisfaccion con su trabajo:",
                            choices = c(
                                "Muy satisfecho",
                                "Satisfecho",
                                "Neutral",
                                "Insatisfecha",
                                "Muy insatisfecha"
                            ),
                            selected = F
                        ),
                        radioButtons(
                            inputId = "textPreocupacion",
                            label = "Que tan preocupada se sintio el dia de ayer",
                            choices = c(
                                "Nada preocupada",
                                "Poco preocupada",
                                "Neutral",
                                "Preocupada",
                                "Muy preocupada"
                            ),
                            selected = F
                        ),
                        radioButtons(
                            inputId = "textstart",
                            label = "En que momento de la vida se siente:",
                            choices = c(
                                "El mejor momento",
                                "Cerca a mi mejor momento",
                                "Neutral",
                                "No estoy pasando por mi mejor momento",
                                "Estoy pasando mi peor momento"
                            ),
                            selected = F
                        )
                    ),
                    column(
                        4,
                        numericInput(
                            inputId = "textmoney",
                            label = "¿Cual es su ingreso economico?:",
                            value = 600000,
                            step = 20000
                        ),
                        p(strong("De 0 a 10, siendo 10 el mas alto, 0 el mas bajo, conteste: ")),
                        sliderInput(
                            inputId = "textLive",
                            label = "¿Que tan satisfecho se siente con su vida?:",
                            value = 10, min = 1, max = 10
                        ),
                        sliderInput(
                            inputId = "textSad",
                            label = "¿Que tan triste se sintio ayer?:",
                            value = 10, min = 1, max = 10
                        ),
                        sliderInput(
                            inputId = "textTranquility",
                            label = "¿Cual es su deseo de seguir viviendo?:",
                            value = 10, min = 1, max = 10
                        ),
                        sliderInput(
                            inputId = "tiempoma",
                            label = "¿Cual es su tiempo libre?:",
                            value = 10, min = 1, max = 10
                        ),
                        tags$head(
                            tags$style
                            (
                                HTML
                                (
                                    "#run{background-color:#8BC5ED}"
                                )
                            )
                        ),
                        actionButton("run", "Run Analysis"),
                        p(strong("La felicidad es de :")),
                        textOutput("resultPredicction")
                    )
                )
            ),
            tabPanel("Arbol Genealogico",
                icon = icon("stream"),
                h1("Estructura de los hogares de las madres solteras", align = "center"),
                fluidRow(
                    selectizeInput("numero_hogar", "Seleccione los directorios:",
                       choices = directorio_lista, multiple = FALSE),
                    # Grafico generado
                    simpleNetworkOutput(outputId = "hogares_grafico")
                )
            ),
            tabPanel("FAQ",
                icon = icon("paperclip"),
                h1("FAQ", align = "center"),
                p(
                    strong("- Fuente 1:"), "Datos tomados del Archivo Nacional de Datos pertenecientes a la encuesta de calidad de vida 2018",
                    em("Tomado de: "),
                    tags$a(href = "http://microdatos.dane.gov.co/index.php/catalog/607/datafile", "ANDA.COM")
                ),
                hr()
            ),
            tabPanel("Updates",
                icon = icon("wrench"),
                h1("Actualizaciones", align = "center"),
                strong("October 9, 2018"),
                p("Creacion de App."),
                hr(),
                strong("April 20, 2020"),
                p("Actualizacion de modelo con los datos del 2019."),
                hr(),
                strong("January 15, 2025"),
                p("Actualizacion de modelo con los datos del 2023."),
                hr(),
                fluidRow(
                    column(
                        4,
                        br(), br()
                    ),
                    column(
                        4,
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

    model <- readRDS("model.rds")

    observeEvent(input$run, {

    ##### Prediccion  ----------------------------------------------

    input_data <- data.frame(
        satisfaccion_economica = economiama(),
        satisfaccion_salud = saludma(),
        satisfaccion_seguridad = seguridadma(),
        satisfaccion_trabajo = trabajoma(),
        satisfaccion_tiempo_libre = input$tiempoma,
        preocupacion = preocupadama(),
        tristeza = input$textSad,
        deseo_vivir = input$textLive,
        escalon_vida = escalonma(),
        ingreso_hogar = input$textmoney
    )

    input_data <- input_data %>%
        mutate(
            satisfaccion_economica = satisfaccion_economica / 10,
            satisfaccion_salud = satisfaccion_salud / 10,
            satisfaccion_seguridad = satisfaccion_seguridad / 10,
            satisfaccion_trabajo = satisfaccion_trabajo / 10,
            satisfaccion_tiempo_libre = satisfaccion_tiempo_libre / 10,
            preocupacion = preocupacion / 10,
            tristeza = tristeza / 10,
            deseo_vivir = deseo_vivir / 10,
            escalon_vida = escalon_vida / 10,
            ingreso_hogar = ingreso_hogar / 255787500,
            )

        output$resultPredicction <- renderText({
            predict(object = model, newdata = input_data)
        })
    })

    ##### Grafico ----------------------------------------------------------

    output$hogares_grafico <- renderSimpleNetwork({
        familia <- filter(cerchas, DIRECTORIO == input$numero_hogar)
        networkData <- data.frame(familia$Source, familia$Target)

        simpleNetwork(networkData,
            opacity = 10000, fontSize = familia$"Target Edad",
            zoom = T
        )
    })
}

shinyApp(ui, server)
