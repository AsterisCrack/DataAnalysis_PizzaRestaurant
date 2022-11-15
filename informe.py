import pandas as pd

def analyze(df, f):
    f.write(f'NaN totales: {df.isna().sum().sum()}\n')
    f.write(f'NaN por columna: \n{df.isna().sum()}\n\n') 
    f.write(f'Nulls totales: {df.isnull().sum().sum()}\n')
    f.write(f'Nulls por columna:\n{df.isnull().sum()}\n\n')
    f.write(f"Cada columna representa el siguiente tipo de dato:\n{df.dtypes}\n")

def crear_informe():
    FILE = "informe_calidad.txt"
    DATA = ('data_files/data_dictionary.csv','data_files/order_details.csv','data_files/orders.csv','data_files/pizza_types.csv','data_files/pizzas.csv')
    with open(FILE, "w") as f:
        for i in DATA:
            f.write(f"Analisis de la tabla {i}\n")
            analyze(pd.read_csv(i, sep=",", encoding="LATIN_1"), f)
            f.write("\n")
            f.write("---------------------------------------------------------------")
            f.write("\n")
    print("Análisis finalizado")
    print(f"Guardado en el archivo {FILE}")