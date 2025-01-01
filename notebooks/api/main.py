import uvicorn
import pickle
import pandas as pd
import numpy as np
from fastapi import FastAPI
from inputs_data import inputs

numeric_features = ['edad', 'ingreso_hogar',
                    'satisfaccion_vida', 'satisfaccion_economica', 'satisfaccion_salud',
                    'satisfaccion_seguridad', 'satisfaccion_trabajo', 'satisfaccion_tiempo_libre', 
                    'preocupacion', 'tristeza', 'deseo_vivir', 'escalon_vida', 'num_cuartos', 
                    'cantidad_personas_hogar']
categorical_features = ['campesino', 'P1_DEPARTAMENTO', 'se_reconoce_como', 'atraccion_sexual']

with open('clf.pkl', 'rb') as f:
    clf = pickle.load(f)

with open('encoder.pkl', 'rb') as f:
    encoder = pickle.load(f)

with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

with open('scaler2.pkl', 'rb') as f:
    scaler2 = pickle.load(f)

app = FastAPI()

@app.post("/predict")
def predict(data:inputs):
    data = data.dict()
    edad = data[ 'edad']
    ingreso_hogar = data[ 'ingreso_hogar']
    satisfaccion_vida = data[ 'satisfaccion_vida']
    satisfaccion_economica = data[ 'satisfaccion_economica']
    satisfaccion_salud = data[ 'satisfaccion_salud']
    satisfaccion_seguridad = data[ 'satisfaccion_seguridad']
    satisfaccion_trabajo = data[ 'satisfaccion_trabajo']
    satisfaccion_tiempo_libre = data[ 'satisfaccion_tiempo_libre']
    preocupacion = data[ 'preocupacion']
    tristeza = data[ 'tristeza']
    deseo_vivir = data[ 'deseo_vivir']
    escalon_vida = data[ 'escalon_vida']
    num_cuartos = data[ 'num_cuartos']
    cantidad_personas_hogar = data[ 'cantidad_personas_hogar']
    campesino = data[ 'campesino']
    P1_DEPARTAMENTO = data[ 'P1_DEPARTAMENTO']
    se_reconoce_como = data[ 'se_reconoce_como']
    atraccion_sexual = data[ 'atraccion_sexual']

    new_data = {'edad': [edad], 
                'ingreso_hogar': [ingreso_hogar],
                'satisfaccion_vida': [satisfaccion_vida],
                'satisfaccion_economica': [satisfaccion_economica],
                'satisfaccion_salud': [satisfaccion_salud],
                'satisfaccion_seguridad': [satisfaccion_seguridad],
                'satisfaccion_trabajo': [satisfaccion_trabajo],
                'satisfaccion_tiempo_libre': [satisfaccion_tiempo_libre], 
                'preocupacion': [preocupacion], 
                'tristeza': [tristeza],
                'deseo_vivir': [deseo_vivir], 
                'escalon_vida': [escalon_vida],
                'num_cuartos': [num_cuartos], 
                'cantidad_personas_hogar': [cantidad_personas_hogar],
                'campesino': [campesino], 
                'P1_DEPARTAMENTO': [P1_DEPARTAMENTO], 
                'se_reconoce_como': [se_reconoce_como], 
                'atraccion_sexual': [atraccion_sexual]
                }
    new_data = pd.DataFrame(new_data)

    new_data['campesino'] = new_data['campesino'].astype(str)
    new_data['P1_DEPARTAMENTO'] = new_data['P1_DEPARTAMENTO'].astype(str)
    new_data['se_reconoce_como'] = new_data['se_reconoce_como'].astype(str)
    new_data['atraccion_sexual'] = new_data['atraccion_sexual'].astype(str)

    X_scaled = scaler.transform(new_data[numeric_features])
    X_scaled = scaler2.transform(X_scaled)
    X_categorical = encoder.transform(new_data[categorical_features])
    X = np.hstack([X_categorical.toarray(), X_scaled])

    out_model = clf.predict(X)[0]

    return {"prediction": out_model}

# 5. Run the API with uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
