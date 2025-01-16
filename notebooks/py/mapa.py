import pandas as pd
import geopandas as gpd 
import numpy as np
from mypackage import dir


# Environment variables
modality = 'p'
project = 'japan'
data = dir.make_dir_line(modality, project) 
raw = data('raw')
processed = data('processed')
models = data('models')
outputs = data('outputs')


regiones = {
        'Amazónica': ['Amazonas', 'Caquetá', 'Putumayo', 'Guainía', 'Guaviare', 'Vaupés', 'Vichada'],
        'Andina': ['Antioquia', 'Bogotá, D.C.', 'Boyacá', 'Caldas', 'Cundinamarca', 'Huila', 'Quindío', 'Risaralda', 'Santander', 'Tolima', 'Norte de Santander'],
        'Caribe': ['Atlántico', 'Bolívar', 'Cesar', 'Córdoba', 'La Guajira', 'Magdalena', 'Sucre', 'Archipiélago de San Andrés, Providencia y Santa Catalina'],
        'Orinoquía': ['Arauca', 'Casanare', 'Meta'],
        'Pacífica': ['Cauca', 'Nariño', 'Valle del Cauca', 'Chocó'],
    }


# Función para cargar datos
def cargar_datos(table_name: str) -> pd.DataFrame:
    df = pd.read_parquet(processed / f'{table_name}.parquet.gzip')
    print(f'Loaded table: {table_name}')
    return df


# Función para cargar los datos en la base de datos
def almacenar_outputs(df: pd.DataFrame, table_name: str) -> None:
    df.to_csv(outputs/f'{table_name}.csv', encoding = 'utf-8-sig', index = False)
    print(f'Saved table: {table_name}')


# Función para obtener la región de un departamento
def obtener_region(departamento):
    for region, departamentos_region in regiones.items():
        if departamento in departamentos_region:
            return region
    return 'Otra'  # Para departamentos no encontrados


if __name__ == '__main__':

    poligonos = gpd.read_file(raw / "departamentos_col.geojson")    
    poligonos.rename(columns={'DeNombre':'departamento'}, inplace=True)
    poligonos['COD_DPTO'] = poligonos['COD_DPTO'].astype(np.int8)
    poligonos.geometry = poligonos.geometry.to_crs(epsg = 4326)
    poligonos = poligonos[poligonos['COD_DPTO'] != 0]
    poligonos['departamento'] = np.where(poligonos['departamento'] == 'Bogota', 'Bogotá, D.C.', poligonos['departamento'])
    poligonos['departamento'] = np.where(poligonos['departamento'] == 'San Andrés Providencia y Santa Catalina', 'Archipiélago de San Andrés, Providencia y Santa Catalina', poligonos['departamento'])
    poligonos['geometry'] = poligonos['geometry'].simplify(tolerance=0.001, preserve_topology=True)

    poligonos2 = poligonos.copy()
    poligonos2 = poligonos2.loc[:,['COD_DPTO', 'geometry']]
    poligonos2.to_file(processed/'dashboard_poligonos_departamentos.geojson', driver='GeoJSON') 

    poligonos3 = poligonos.copy()
    poligonos3 = poligonos3.loc[:,['departamento', 'COD_DPTO']]

    df = cargar_datos('dataset')
    df = df.loc[df['id_secuencia_parentesco'] == '1-1']
    cols_to_convert = ['P1_DEPARTAMENTO', 'P1_MUNICIPIO', 'REGION']
    df[cols_to_convert] = df[cols_to_convert].astype(float).astype(int)
    df = df.loc[:,[
        # 'DIRECTORIO', 'id_familias', 'id_secuencia_parentesco', 
        'P1_DEPARTAMENTO', 'REGION', #'P1_MUNICIPIO', 
        'felicidad', 'tristeza',
        'satisfaccion_vida', 'satisfaccion_economica', 'satisfaccion_salud',
        'satisfaccion_seguridad', 'satisfaccion_trabajo', 'satisfaccion_tiempo_libre',
        'preocupacion', 'deseo_vivir', 'escalon_vida',
        ]]
    df.rename(columns={'P1_DEPARTAMENTO':'COD_DPTO'}, inplace=True)
    df = df.groupby(['COD_DPTO', 'REGION'], as_index=False).mean()

    df = pd.merge(df, poligonos3, how='left', on=['COD_DPTO'])

    # Aplicar la función a cada fila del DataFrame
    df['nombre_region'] = df['departamento'].apply(obtener_region)

    df = df.loc[:,[
        'COD_DPTO', 'REGION', 'nombre_region', 'departamento', 'felicidad', 
        'satisfaccion_vida', 'satisfaccion_economica', 'satisfaccion_salud',
        'satisfaccion_seguridad', 'satisfaccion_trabajo', 'satisfaccion_tiempo_libre', 
        'preocupacion', 'tristeza', 'deseo_vivir', 'escalon_vida', 
        ]]

    df.columns = [
        'COD_DPTO', 'Región', 'Region politica', 'Departamento', 'Felicidad',
        'Satisfacción vida', 'Satisfacción Economica', 'Satisfacción Salud',
        'Satisfacción Seguridad', 'Satisfacción Trabajo', 'Satisfacción Tiempo Libre',
        'Preocupacion', 'Tristeza', 'Deseo Vivir', 'Escalon Vida'
    ]

    almacenar_outputs(df, 'mapa')


    df_melted = df.melt(id_vars=['Departamento', 'Region politica'], 
                        value_vars=['Felicidad',
                                    'Satisfacción vida', 'Satisfacción Economica', 'Satisfacción Salud',
                                    'Satisfacción Seguridad', 'Satisfacción Trabajo', 'Satisfacción Tiempo Libre',
                                    'Preocupacion', 'Tristeza', 'Deseo Vivir', 'Escalon Vida'],
                        var_name='Variable', 
                        value_name='Valor')

    almacenar_outputs(df_melted, 'parallel')
