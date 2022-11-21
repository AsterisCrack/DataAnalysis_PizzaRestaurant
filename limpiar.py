
#Necesito limpiar el archivo csv para poder trabajar con el
import pandas as pd
import re
import datetime

def clean_details_file(file):
    #Cosas a tener en cuenta:
    #1. Hay líneas a las que les falta algún dato. Estas las elimino por completo
    #2. Hay líneas que tienen espacios en blanco donde debería haber ;. Estas son en las que detrás del espacio hay un número
    #3. Hay líneas que tienen espacios en blanco donde debería haber _. Estas son en las que detrás del espacio hay una letra
    #4. Hay líneas en las que hay que cambiar el nombre de la pizza. Por ejemplo: 3 por e, @ por a, etc.
    #Leo el archivo
    clean_file_name = file[:-4] + "_clean.csv"
    with open(file, 'r') as f:
        lines = f.readlines()
        with open(clean_file_name, 'w') as f2:
            for line in lines:
                line.strip()
                #Si la línea tiene un espacio en blanco y detrás hay un número, lo cambio por ;
                if ' ' in line and line[line.index(' ')+1].isdigit():
                    line = line.replace(' ', ';')
                #Si la línea tiene un espacio en blanco y detrás hay una letra, lo cambio por _
                elif ' ' in line: # and line[line.index(' ')+1].isalpha()
                    line = line.replace(' ', '_')
                if "-" in line:
                    line = line.replace("-", "_")
                #Si la linea no tiene dos ; seguidos, la añado al archivo
                if ';;' not in line and ';\n' not in line:
                    f2.write(line)

    df = pd.read_csv(clean_file_name, sep=';')
    #En la columna quantity, cambio los numeros escritos en letra por números
    num_letra = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
    num = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    for i in range(len(num_letra)):
        #Da igual si es mayuscula o minuscula
        df['quantity'] = df['quantity'].str.replace(num_letra[i], str(num[i]), case=False)


    #Arreglo columna pizza_id
    #En la columna pizza_id, cambio los caracteres como @ por a, 3 por e, etc.
    caracteres = ["@", "3", "4", "5", "6", "7", "8", "9", "0"]
    caracteres_cambio = ["a", "e", "f", "s", "g", "t", "b", "g", "o"]
    for i in range(len(caracteres)):
        df['pizza_id'] = df['pizza_id'].str.replace(caracteres[i], caracteres_cambio[i])

    #guardo el archivo
    df.to_csv(clean_file_name, sep=';', index=False)

def clean_orders_file(file):
    #Cosas a tener en cuenta:
    #1. Hay líneas a las que les falta algún dato. Estas las elimino por completo
    #2. Si después de un espacio hay algo de la forma 20:04:41, lo cambio por ;
    #3. Nos da igual la hora, así que la elimino. Elimino todo lo que haya detrás del último ;
    
    #Leo el archivo
    clean_file_name = file[:-4] + "_clean.csv"
    with open(file, 'r') as f:
        lines = f.readlines()
        with open(clean_file_name, 'w') as f2:
            for line in lines:
                line.strip()
                #Si después de un espacio hay algo de la forma 20:04:41, lo cambio por ;
                hora = re.search(r' \d{2}:\d{2}:\d{2}', line)
                if hora:
                    line = line.replace(hora.group(), ';')
                #No necesito la hora y no quiero que me de problemas, así que la elimino
                #elimino todo lo que haya detrás del último ;
                line = line[:line.rindex(';')]
                line = line+'\n'
                #Si la linea no tiene dos ; seguidos, la añado al archivo
                if ';;' not in line and ';\n' not in line:
                    f2.write(line)

    df = pd.read_csv(clean_file_name, sep=';')


    #If the value in df['date'] is a float, it is a date in python timestamp format
    #I will convert it to a date in the format YYYY-MM-DD
    for i in range(len(df['date'])):
        try:
            df.loc[i, 'date'] = float(df['date'][i])
            df.loc[i, 'date'] = datetime.datetime.fromtimestamp(df.loc[i, 'date']).strftime('%Y-%m-%d')
        except:
            pass
    df["date"] = pd.to_datetime(df["date"])

    #guardo el archivo
    df.to_csv(clean_file_name, sep=';', index=False)

def limpiar():
    clean_orders_file("data_files_2016/orders.csv")
    clean_details_file("data_files_2016/order_details.csv")
    return ("data_files_2016/order_details_clean.csv", "data_files_2016/orders_clean.csv")


