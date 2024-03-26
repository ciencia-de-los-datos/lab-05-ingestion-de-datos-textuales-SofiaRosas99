import pandas as pd
import os
import zipfile
import glob


def descomprimir(archivo_zip, ruta_salida=None):
    if ruta_salida == None:
        ruta_salida = os.getcwd()
    if not os.path.exists(archivo_zip):
        raise Exception("No existe archivo zip")
    if not os.path.exists(ruta_salida):
        os.mkdir(ruta_salida)
    with zipfile.ZipFile(archivo_zip, "r") as zip:
        zip.extractall(ruta_salida)


def obtener_txt(ruta_archivos):
    archivos = glob.glob(ruta_archivos + "/*/*.txt")
    return archivos


"ejemplo/train\positive\0457.txt"


def consolidar(lista_rutas):
    lista_frases = []
    for ruta in lista_rutas:
        with open(ruta, "r", encoding="utf-8") as txt:
            lineas = txt.readlines()
        target = ruta.split("\\")[1]
        frase = lineas
        if len(lineas) > 1:
            max = 0
            for linea in lineas:
                long = len(linea)
                if long > max:
                    max = long
                    frase = [linea]
        lista_frases.append([frase[0], target])
    return lista_frases


def crear_df(datos, nombre_columnas):
    df = pd.DataFrame(datos, columns=nombre_columnas)
    return df


def guardar_csv(df, nombre_csv, folder=None, index=False):
    if folder != None:
        if not os.path.exists(folder):
            os.mkdir(folder)
        nombre_csv = os.path.join(folder, nombre_csv)
    df.to_csv(nombre_csv, index=index)


def main(archivo_zip, ruta_salida):
    descomprimir(archivo_zip, ruta_salida)
    archivos_test = obtener_txt(ruta_salida + "/test")
    archivos_train = obtener_txt(ruta_salida + "/train")
    data_test = consolidar(archivos_test)
    data_train = consolidar(archivos_train)
    nombre_columnas = ["phrase", "sentiment"]
    df_test = crear_df(data_test, nombre_columnas)
    df_train = crear_df(data_train, nombre_columnas)
    nombre_test = "test_dataset.csv"
    nombre_train = "train_dataset.csv"
    guardar_csv(df_test, nombre_test)
    guardar_csv(df_train, nombre_train)


if __name__ == "__main__":
    archivo_zip = "data.zip"
    ruta_salida = "data"
    main(archivo_zip, ruta_salida)
