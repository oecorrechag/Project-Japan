library(shiny)
library(tree)
library(rpart)
library(dplyr)
library(networkD3)
library(igraph)

data <- read.csv("dataset.csv",
                 header = T,
                 sep = ",",
                 fileEncoding = "UTF-8"
)

data_normalized <- data %>%
  mutate(
    satisfaccion_economica = (satisfaccion_economica - min(satisfaccion_economica)) / (max(satisfaccion_economica) - min(satisfaccion_economica)),
    satisfaccion_salud = (satisfaccion_salud - min(satisfaccion_salud)) / (max(satisfaccion_salud) - min(satisfaccion_salud)),
    satisfaccion_seguridad = (satisfaccion_seguridad - min(satisfaccion_seguridad)) / (max(satisfaccion_seguridad) - min(satisfaccion_seguridad)),
    satisfaccion_trabajo = (satisfaccion_trabajo - min(satisfaccion_trabajo)) / (max(satisfaccion_trabajo) - min(satisfaccion_trabajo)),
    satisfaccion_tiempo_libre = (satisfaccion_tiempo_libre - min(satisfaccion_tiempo_libre)) / (max(satisfaccion_tiempo_libre) - min(satisfaccion_tiempo_libre)),
    preocupacion = (preocupacion - min(preocupacion)) / (max(preocupacion) - min(preocupacion)),
    tristeza = (tristeza - min(tristeza)) / (max(tristeza) - min(tristeza)),
    deseo_vivir = (deseo_vivir - min(deseo_vivir)) / (max(deseo_vivir) - min(deseo_vivir)),
    escalon_vida = (escalon_vida - min(escalon_vida)) / (max(escalon_vida) - min(escalon_vida)),
    ingreso_hogar = (ingreso_hogar - min(ingreso_hogar)) / (max(ingreso_hogar) - min(ingreso_hogar)),
  )

modelo <- lm(
  felicidad ~ satisfaccion_economica +
    satisfaccion_salud +
    satisfaccion_seguridad +
    satisfaccion_trabajo +
    satisfaccion_tiempo_libre +
    preocupacion +
    tristeza +
    deseo_vivir +
    escalon_vida +
    ingreso_hogar,
  data = data_normalized
)

saveRDS(modelo, file = "model.rds")
modelo <- readRDS("model.rds")

input_data <- data.frame(
  satisfaccion_economica = c(10),
  satisfaccion_salud = c(10),
  satisfaccion_seguridad = c(10),
  satisfaccion_trabajo = c(10),
  satisfaccion_tiempo_libre = c(10),
  preocupacion = c(10),
  tristeza = c(10),
  deseo_vivir = c(10),
  escalon_vida = c(10),
  ingreso_hogar = c(1500000)
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

predict(object = modelo, newdata = input_data)
