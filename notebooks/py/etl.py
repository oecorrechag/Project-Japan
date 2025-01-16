import pandas as pd
import numpy as np
from mypackage import dir


# Environment variables
modality = 'p'
project = 'japan'
data = dir.make_dir_line(modality, project) 
raw = data('raw')
processed = data('processed')


# Función para cargar datos
def cargar_datos(table_name: str) -> pd.DataFrame:
    df = pd.read_csv(raw / f'{table_name}.csv', sep = ';', decimal = '.', header = 0)
    print(f'Loaded table: {table_name}')
    return df


# Función para transformar los datos vivienda
def transformar_datos_vivienda(df: pd.DataFrame) -> pd.DataFrame:
    df = df.rename(columns={'P8520S1':'energia', 'P1070': 'tipo_de_vivienda', 'P8520S5': 'acueducto', 
                            'P8520S3': 'alcantarillado', 'P8520S4': 'recoleccion_Basura','P5661S3': 'basura', 
                            'P5661S4': 'aire', 'P5661S5': 'invaciones', 'P5661S9': 'contaminacion_rios', 
                            'P8520S1A1':'estrato'})
    df = df.loc[:, ['DIRECTORIO', 'SECUENCIA_ENCUESTA', 'ORDEN', 'P1_DEPARTAMENTO', 'P1_MUNICIPIO', 'REGION', 
                    'CANT_HOGARES_VIVIENDA', 'CLASE', 'tipo_de_vivienda', 'energia', 'estrato', 'acueducto',
                    'alcantarillado', 'recoleccion_Basura', 'basura', 'aire', 'contaminacion_rios', 'invaciones']]
    return df


# Función para transformar los datos servicios
def transformar_datos_servicios(df: pd.DataFrame) -> pd.DataFrame:
    df = df.rename(columns={'P5000':'num_cuartos', 
                            'P5010': 'num_duermen', 
                            'I_HOGAR':'ingreso_hogar', 
                            'CANT_PERSONAS_HOGAR':'cantidad_personas_hogar'})
    df = df.loc[:, ['DIRECTORIO', 'SECUENCIA_ENCUESTA', 'ORDEN', 'num_cuartos', 'num_duermen', 
                    'ingreso_hogar', 'cantidad_personas_hogar']]
    df.drop(df[df['num_cuartos'] == 99].index, inplace = True)
    df.drop(df[df['num_duermen'] == 99].index, inplace = True)
    return df


# Función para transformar los datos carateristicas
def transformar_datos_carateristicas(df: pd.DataFrame) -> pd.DataFrame:
    df = df.rename(columns={'P6020':'sexo', 'P6051':'parentesco', 'P6040':'edad', 'P5502':'estado_civil',
                            'P6081':'padre_vive', 'P6083': 'madre_vive', 'P6080':'cultura_pueblo', 
                            'P6087':'nivel_educativo_padre', 'P6088':'nivel_educativo_madre',
                            'P1895':'satisfaccion_vida', 'P1896': 'satisfaccion_economica', 'P1897': 'satisfaccion_salud', 
                            'P1898':'satisfaccion_seguridad', 'P1899': 'satisfaccion_trabajo', 'P1901': 'felicidad',
                            'P1903':'preocupacion', 'P1904': 'tristeza', 'P1905': 'deseo_vivir', 'P1927': 'escalon_vida',
                            'P2057':'campesino', 'P3175':'satisfaccion_tiempo_libre', 'P3038':'atraccion_sexual',
                            'P3039': 'se_reconoce_como', 'P6016':'generador_informacion',
                            })

    df = df.loc[:, ['DIRECTORIO', 'SECUENCIA_ENCUESTA', 'SECUENCIA_P', 'ORDEN', 'sexo', 'edad', 
                    'parentesco', 'generador_informacion', 'estado_civil', 'padre_vive', 
                    'nivel_educativo_padre', 'madre_vive',  'nivel_educativo_madre', 'cultura_pueblo', 
                    'campesino', 'satisfaccion_vida', 'satisfaccion_economica', 'satisfaccion_salud', 
                    'satisfaccion_seguridad', 'satisfaccion_trabajo', 'satisfaccion_tiempo_libre', 
                    'felicidad', 'preocupacion', 'tristeza', 'deseo_vivir', 'escalon_vida', 
                    'atraccion_sexual', 'se_reconoce_como']]
    
    df['campesino'] = np.where(df['campesino'] == 9, 2, df['campesino'])
    df['atraccion_sexual'] = np.where(df['atraccion_sexual'] == 9, 4, df['atraccion_sexual'])
    df['se_reconoce_como'] = np.where(df['se_reconoce_como'] == 9, 5, df['se_reconoce_como'])

    return df


def familias_madres_con_hijos(df: pd.DataFrame, estado_civil=[4, 5]) -> pd.DataFrame:
    """
    Identifica familias donde la mujer cabeza de familia es soltera (según los estados civiles
    proporcionados) y tiene al menos un hijo (según el criterio proporcionado).

    Args:
        df: DataFrame con los datos.
        estado_civil: Lista de códigos de estado civil considerados solteros.

    Returns:
        DataFrame con las familias que cumplen los criterios.
    """

    # Crear IDs y filtrar mujeres cabeza de familia
    df['id_familias'] = df['DIRECTORIO'].astype(str) + '-' + df['SECUENCIA_P'].astype(str)
    df['id_secuencia_parentesco'] = df['SECUENCIA_ENCUESTA'].astype(str) + '-' + df['parentesco'].astype(str)
    df_aux = df.copy()
    # df_errores = df_aux.loc[(df_aux['parentesco'] == 1) & (df_aux['felicidad'].notna())]

    # tomar las mujeres solteras cabeza de hogar
    df_mujeres_cabeza_solteras = df.loc[(df['SECUENCIA_P'] == 1) & (df['sexo'] == 2) & (df['parentesco'] == 1) & (df['estado_civil'].isin(estado_civil))]
    ## Eliminar registros no necesarios
    df_mujeres_cabeza_solteras = df_mujeres_cabeza_solteras[~(df_mujeres_cabeza_solteras['satisfaccion_economica'] == 99) & (df_mujeres_cabeza_solteras['id_secuencia_parentesco'] == '1-1')]


    conjunto_mujeres_solteras = set(df_mujeres_cabeza_solteras['id_familias'])
    # Eliminar problemas de encuesta
    df_errores = df.loc[df['id_secuencia_parentesco'] == '2-2']
    conjunto_errores = set(df_errores['id_familias'])
    # Esta es la lista de mujeres solteras (sin embargo aca no se sabe si tienen hijos o no)
    conjunto_mujeres_solteras_fix = list(conjunto_mujeres_solteras - conjunto_errores)


    # Se obtienen solo las familias donde sean mujeres cabeza de hogar, solteras y con almenos 1 hijo
    familias_con_hijos = df_aux[df_aux['id_familias'].isin(conjunto_mujeres_solteras_fix)].groupby('id_familias')\
                                    .filter(lambda x: (x['parentesco'] == 3).any())
    
    # Seleccionar variables necesarias
    familias_con_hijos = familias_con_hijos.loc[:,[
        'id_familias', 'id_secuencia_parentesco',
        'DIRECTORIO', 'SECUENCIA_ENCUESTA', 'SECUENCIA_P', 'ORDEN', 'sexo',
        'edad', 'parentesco', 'generador_informacion', 'estado_civil', 'padre_vive',
        'nivel_educativo_padre', 'madre_vive', 'nivel_educativo_madre',
        'cultura_pueblo', 'campesino', 'satisfaccion_vida',
        'satisfaccion_economica', 'satisfaccion_salud',
        'satisfaccion_seguridad', 'satisfaccion_trabajo',
        'satisfaccion_tiempo_libre', 'felicidad', 'preocupacion', 'tristeza',
        'deseo_vivir', 'escalon_vida', 'atraccion_sexual', 'se_reconoce_como',
       ]]
        
    return familias_con_hijos


# Función para cargar los datos en la base de datos
def cargar_en_db(df: pd.DataFrame, table_name: str) -> None:
    df.to_parquet(processed/f'{table_name}.parquet.gzip', compression='gzip')
    print(f'Saved table: {table_name}')


if __name__ == '__main__':

    # ETL Datos de la vivienda
    df_vivienda = cargar_datos('Datos de la vivienda')
    df_vivienda = transformar_datos_vivienda(df_vivienda)
    cargar_en_db(df_vivienda, 'vivienda')

    # ETL Servicios del hogar
    df_servicios = cargar_datos('Servicios del hogar')
    df_servicios = transformar_datos_servicios(df_servicios)
    cargar_en_db(df_servicios, 'servicios')

    # ETL Características y composición del hogar
    df_carateristicas = cargar_datos('Características y composición del hogar')
    df_carateristicas = transformar_datos_carateristicas(df_carateristicas)
    cargar_en_db(df_carateristicas, 'caracteristicas')

    # Create dataset
    familias_resultado = familias_madres_con_hijos(df_carateristicas)
    
    cargar_en_db(familias_resultado, 'familias')

    df = pd.merge(df_servicios, df_vivienda, how='left', on = ['DIRECTORIO', 'SECUENCIA_ENCUESTA', 'ORDEN'])
    df = pd.merge(familias_resultado, df, how='left', on = ['DIRECTORIO', 'SECUENCIA_ENCUESTA', 'ORDEN'])

    print(f'Numero de mujeres cabeza de hogar con almenos un hijo: {df['id_familias'].nunique()}')
    print(f'Registros de familias de mujeres cabeza de hogar con almenos un hijo: {df.shape[0]}')
    print(f'Promedio numero de integrantes: {df.shape[0]/df['id_familias'].nunique()}')

    cargar_en_db(df, 'dataset')
