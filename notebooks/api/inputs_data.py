# 1. Library imports
from pydantic import BaseModel

# 2. Class for models.
class inputs(BaseModel):
    edad:int=58
    ingreso_hogar:float=2501667
    satisfaccion_vida:int=6
    satisfaccion_economica:int=3
    satisfaccion_salud:int=6
    satisfaccion_seguridad:int=3
    satisfaccion_trabajo:int=4
    satisfaccion_tiempo_libre:int=7
    preocupacion:int=3
    tristeza:int=3
    deseo_vivir:int=7
    escalon_vida:int=7
    num_cuartos:int=3
    cantidad_personas_hogar:int=3
    campesino:int=2
    P1_DEPARTAMENTO:int=18
    se_reconoce_como:int=2
    atraccion_sexual:int=1
    