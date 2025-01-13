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

def preprocess_data(data):
    # Crear DataFrame de forma más concisa
    df = pd.DataFrame({k: [v] for k, v in data.items()})

    # Convertir columnas categóricas a string directamente en el DataFrame
    df[categorical_features] = df[categorical_features].astype(str)

    # Escalado y codificación (función auxiliar)
    X_scaled = scaler.transform(df[numeric_features])
    X_scaled = scaler2.transform(X_scaled)
    X_categorical = encoder.transform(df[categorical_features])
    X = np.hstack([X_categorical.toarray(), X_scaled])
    return X

app = FastAPI()

@app.post("/predict")
def predict(data: inputs):
    try:
        X = preprocess_data(data.dict())
        out_model = clf.predict(X)[0]
        return {"prediction": out_model}
    except Exception as e:
        # Manejar la excepción (por ejemplo, registrar un error)
        return {"error": str(e)}

# 5. Run the API with uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
