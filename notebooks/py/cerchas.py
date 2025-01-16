import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional
import networkx as nx

from mypackage import dir

# Environment variables
modality = 'p'
project = 'japan'
data = dir.make_dir_line(modality, project) 
processed = data('processed')
models = data('models')
outputs = data('outputs')

# Función para cargar datos
def cargar_datos(table_name: str) -> pd.DataFrame:
    df = pd.read_parquet(processed / f'{table_name}.parquet.gzip')
    print(f'Loaded table: {table_name}')
    return df

# Función para cargar los datos en la base de datos
def almacenar_outputs(df: pd.DataFrame, table_name: str) -> None:
    df.to_csv(outputs/f'{table_name}.csv', encoding = 'utf-8-sig', index = False)
    print(f'Saved table: {table_name}')

def get_photo(parentesco: int, sexo: int) -> Optional[str]:
    """
    Toma la columna parentesco y sexo de un dataframe y retorna una tupla de su transformacion

    Args:
        str: parentesco
        str: sexo

    Returns:
        Str
    """

    """
    Obtiene la etiqueta de la relación basada en el parentesco y sexo.

    Args:
        parentesco (int): Código que representa el parentesco de la persona.
        sexo (int): Código que representa el sexo de la persona (1: masculino, 2: femenino).

    Returns:
        Optional[str]: La etiqueta de la relación (e.g., 'Hijo_', 'Abuela', 'Yerno') o None si no se encuentra.
    """

    labels = {
        (1, 2): 'https://images.pexels.com/photos/755028/pexels-photo-755028.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2', 
        (3, 1): 'https://images.pexels.com/photos/3036405/pexels-photo-3036405.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2', 
        (3, 2): 'https://images.pexels.com/photos/1445704/pexels-photo-1445704.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2',
        (4, 1): 'https://images.pexels.com/photos/6973191/pexels-photo-6973191.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2', 
        (4, 2): 'https://images.pexels.com/photos/3768140/pexels-photo-3768140.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2',
        (5, 1): 'https://images.pexels.com/photos/3975266/pexels-photo-3975266.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2', 
        (5, 2): 'https://images.pexels.com/photos/1109238/pexels-photo-1109238.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2',#Padre, madre, padrastro, madrastra
        (6, 1): 'https://images.pexels.com/photos/18047314/pexels-photo-18047314/free-photo-of-pareja-gente-feliz-boda.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2', 
        (6, 2): 'https://images.pexels.com/photos/12371673/pexels-photo-12371673.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2',
        (7, 1): 'https://images.pexels.com/photos/3972178/pexels-photo-3972178.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2', 
        (7, 2): 'https://images.pexels.com/photos/4151482/pexels-photo-4151482.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2',
        (8, 1): 'https://images.pexels.com/photos/1320762/pexels-photo-1320762.jpeg', 
        (8, 2): 'https://images.pexels.com/photos/3854868/pexels-photo-3854868.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2',
        (9, 1): 'https://images.pexels.com/photos/39691/family-pier-man-woman-39691.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2', 
        (9, 2): 'https://images.pexels.com/photos/30194589/pexels-photo-30194589/free-photo-of-personas-disfrutando-de-la-diversion-con-burbujas-al-atardecer-en-el-parque-de-san-diego.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2',
        (10, 1): 'https://images.pexels.com/photos/6169135/pexels-photo-6169135.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2', 
        (10, 2): 'https://images.pexels.com/photos/9462618/pexels-photo-9462618.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2',
        (11, 1): 'https://images.pexels.com/photos/5415837/pexels-photo-5415837.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2', 
        (11, 2): 'https://images.pexels.com/photos/325265/pexels-photo-325265.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2',
        (12, 1): 'https://images.pexels.com/photos/6868463/pexels-photo-6868463.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2', 
        (12, 2): 'https://images.pexels.com/photos/7181189/pexels-photo-7181189.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2',
        (13, 1): 'https://images.pexels.com/photos/33786/hands-walking-stick-elderly-old-person.jpg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2', 
        (13, 2): 'https://images.pexels.com/photos/30150128/pexels-photo-30150128.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2',
        (14, 1): 'https://images.pexels.com/photos/1396122/pexels-photo-1396122.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2', 
        (14, 2): 'https://images.pexels.com/photos/106399/pexels-photo-106399.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2',
    }
    return labels.get((parentesco, sexo), None)


def get_label(parentesco: int, sexo: int) -> Optional[str]:
    """
    Toma la columna parentesco y sexo de un dataframe y retorna una tupla de su transformacion

    Args:
        str: parentesco
        str: sexo

    Returns:
        Str
    """

    """
    Obtiene la etiqueta de la relación basada en el parentesco y sexo.

    Args:
        parentesco (int): Código que representa el parentesco de la persona.
        sexo (int): Código que representa el sexo de la persona (1: masculino, 2: femenino).

    Returns:
        Optional[str]: La etiqueta de la relación (e.g., 'Hijo_', 'Abuela', 'Yerno') o None si no se encuentra.
    """

    labels = {
        (1, 2): 'Madre', 
        (3, 1): 'Hijo_', (3, 2): 'Hija_',
        (4, 1): 'Nieto_', (4, 2): 'Nieta_',
        (5, 1): 'Abuelo', (5, 2): 'Abuela',#Padre, madre, padrastro, madrastra
        (6, 1): 'Suegro', (6, 2): 'Suegra',
        (7, 1): 'Hermano_', (7, 2): 'Hermana_',
        (8, 1): 'Yerno', (8, 2): 'Nuera',
        (9, 1): 'Familiar', (9, 2): 'Familiar',
        (10, 1): 'Empleado', (10, 2): 'Empleada',
        (11, 1): 'Parientes', (11, 2): 'Parientes',
        (12, 1): 'Tabajador', (12, 2): 'Tabajadora',
        (13, 1): 'Pensionista', (13, 2): 'Pensionista',
        (14, 1): 'Otro', (14, 2): 'Otra',
    }
    return labels.get((parentesco, sexo), None)


def contador_integrantes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Añade un contador único por tipo de parentesco dentro de cada familia.

    Args:
        df (pd.DataFrame): DataFrame con las columnas 'id_familias' y 'parentesco'.

    Returns:
        pd.DataFrame: El DataFrame original con una nueva columna 'valor2'.
    """

    df['valor2'] = (
        df.groupby(['id_familias', 'parentesco'])
        .cumcount()
        .add(1)
        .astype(str)  # Convertir a string
        #.replace('1', '')  # Eliminar el sufijo '1'
    )

    return df


def familia_mejorada(df: pd.DataFrame) -> pd.DataFrame:
    """
    Genera un dataframe - grafo de relaciones familiares a partir de un DataFrame.

    Args:
        df (pd.DataFrame): DataFrame con columnas como 'SECUENCIA_P', 'id_familias', 'parentesco', y 'sexo'.

    Returns:
        pd.DataFrame: DataFrame con columnas 'from' y 'to', representando las relaciones familiares.
    """

    df = df.rename(columns={'SECUENCIA_P': 'Madre'})
    df = contador_integrantes(df)

    lista_from = []
    lista_to = []

    for index, row in df.iterrows():

        label = get_label(row['parentesco'], row['sexo'])

        if label in ['Hija_', 'Hijo_', 'Hermana_', 'Hermano_']:
            lista_from.append('Madre')
            lista_to.append(f"{label}{df.loc[index:, 'valor2'].iloc[0]}")
        elif label in ['Abuelo', 'Abuela', 'Suegro', 'Suegra']:
            # lista_from.append('Madre' if row['parentesco'] in [5, 6] else row['Madre'])
            lista_from.append('Madre')
            lista_to.append(f"{label}")
        elif label in ['Yerno', 'Nuera']:
            ultimo_hijo = next((x for x in reversed(lista_to) if isinstance(x, str) and x.startswith("H")), None)
            lista_from.append(ultimo_hijo if row['parentesco'] in [8] else row['Madre'])
            lista_to.append(f"{label}")
        elif label in ['Nieto_', 'Nieta_']:
            ultimo_hijo = next((x for x in reversed(lista_to) if isinstance(x, str) and x.startswith("H")), None)
            lista_from.append(ultimo_hijo if row['parentesco'] in [4] else row['Madre'])
            lista_to.append(f"{label}{df.loc[index:, 'valor2'].iloc[0]}")
        elif label in ['Familiar', 'Empleado', 'Empleada', 'Parientes', 'Tabajador', 'Tabajadora', 'Pensionista', 'Otro', 'Otra']:
            # lista_from.append('Madre' if row['parentesco'] in [9, 10, 11, 12, 13, 14] else row['Madre'])
            lista_from.append('Madre')
            lista_to.append(f"{label}")
        else:
            lista_from.append(row['Madre'])
            lista_to.append(row['parentesco'])

    df['source'] = lista_from
    df['target'] = lista_to
    df.drop(['Madre'], axis=1, inplace=True)
    df.drop(df[df['target'] == 1].index, inplace=True)

    # df.rename(columns={'edad':'source_edad', 'sexo':'source_sexo', 'photo_url':'source_photo_url'}, inplace=True)

    df.rename(columns={'edad':'target_edad', 'sexo':'target_sexo', 'photo_url':'target_photo_url'}, inplace=True)

    return df


if __name__ == '__main__':

    df = cargar_datos('familias')
    df = df.loc[:, [
        'id_familias', 'DIRECTORIO',
        'SECUENCIA_P', 'ORDEN', 
        'parentesco',
        'sexo', 'edad',
        'felicidad', 'tristeza',
        'satisfaccion_vida', 'satisfaccion_economica', 'satisfaccion_salud',
        'satisfaccion_seguridad', 'satisfaccion_trabajo', 'satisfaccion_tiempo_libre',
        'preocupacion', 'deseo_vivir', 'escalon_vida',
        ]]
    df['photo_url'] = df.apply(lambda row: get_photo(row['parentesco'], row['sexo']), axis=1)


    target_df = df.copy()
    target_df['label'] = target_df.apply(lambda row: get_label(row['parentesco'], row['sexo']), axis=1)
    target_df = contador_integrantes(target_df)
    target_df['id_orden'] = target_df['label'].astype(str) + target_df['valor2'].astype(str)
    target_df['id_orden'] = np.where(target_df['id_orden'].str.contains('_'), target_df['id_orden'], target_df['label'])
    target_df = target_df.loc[:,['id_familias', 'id_orden', 'edad', 'sexo', 'photo_url']]
    target_df.rename(columns={'edad':'source_edad', 'sexo':'source_sexo', 'photo_url':'source_photo_url'}, inplace=True)
    target_df.head()


    df = familia_mejorada(df)

    df = pd.merge(df, target_df, how='left', left_on=['id_familias', 'source'], right_on=['id_familias', 'id_orden']) 
    df = df.loc[:,[
        'DIRECTORIO', 'ORDEN', 'parentesco', 
        'source', 'source_sexo', 'source_edad', 'source_photo_url',
        'target', 'target_sexo', 'target_edad', 'target_photo_url',
        'felicidad', 'tristeza',
        'satisfaccion_vida', 'satisfaccion_economica', 'satisfaccion_salud',
        'satisfaccion_seguridad', 'satisfaccion_trabajo', 'satisfaccion_tiempo_libre',
        'preocupacion', 'deseo_vivir', 'escalon_vida',    
    ]]

    familias_con_faltantes = df[df['source_edad'].isnull()]['DIRECTORIO'].unique()

    fix_df = df.copy()
    fix_df = fix_df[fix_df['DIRECTORIO'].isin(familias_con_faltantes)]

    # # Función para reemplazar los valores por fila
    madres = fix_df[fix_df['source'] == 'Madre'].set_index('DIRECTORIO')

    # # Reemplazar valores en las columnas correspondientes
    for col in ['source', 'source_sexo', 'source_edad', 'source_photo_url']:
        fix_df[col] = fix_df['DIRECTORIO'].map(madres[col])

    df.drop(df[df['DIRECTORIO'].isin(familias_con_faltantes)].index, inplace = True)
    df = pd.concat([df,fix_df], ignore_index=True)

    df['source'] = df['source'].str.replace('_', ' ')
    df['target'] = df['target'].str.replace('_', ' ')
    df['satisfaccion_economica'] = np.where(df['satisfaccion_economica'] == 99, 0, df['satisfaccion_economica'])
    cols_to_convert = ['source_sexo', 'source_edad']
    df[cols_to_convert] = df[cols_to_convert].astype(int)

    df.columns = [
        'DIRECTORIO', 'ORDEN', 'Parentesco', 'Source', 'Source Sexo',
        'Source Edad', 'Source photo-url', 'Target', 'Target Sexo',
        'Target Edad', 'Target photo-url', 'Felicidad', 'Tristeza',
        'Satisfacción vida', 'Satisfacción Economica', 'Satisfacción Salud',
        'Satisfacción Seguridad', 'Satisfacción Trabajo', 'Satisfacción Tiempo Libre',
        'Preocupacion', 'Deseo Vivir', 'Escalon Vida'
    ]

    almacenar_outputs(df, 'cerchas')
