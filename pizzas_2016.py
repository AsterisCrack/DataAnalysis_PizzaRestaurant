
import pandas as pd
import informe_2016 as informe
import informe_2016_xml as informeXML
import informe_final_XML
import reporte_ejecutivo
import reporte_excel
import signal
import sys
import os

def handler_signal(signal, frame):
    print("\n\n Exiting program...")
    sys.exit(1)

# Señal de control por si el usuario introduce Ctrl + C para parar el programa
signal.signal(signal.SIGINT, handler_signal)

def extract():
    #Obtenemos los datos de las tablas que necestiamos
    pizzas = pd.read_csv("data_files_2016/pizzas.csv", encoding="latin-1")
    pizza_types = pd.read_csv("data_files_2016/pizza_types.csv", encoding="latin-1")
    orders = pd.read_csv("data_files_2016/orders_clean.csv", sep=";", encoding="latin-1")
    order_details = pd.read_csv("data_files_2016/order_details_clean.csv", sep=";", encoding="latin-1")
    return pizzas, pizza_types, orders, order_details

def transform(pizzas, pizza_types, orders, order_details):
    #Quito caracter extraño Glyph 145 (\x91) de la columna ingredients
    pizza_types["ingredients"] = pizza_types["ingredients"].str.replace("\x91", "")
    
    #Unimos las tablas que nos interesan
    pizzas = pizzas.merge(pizza_types, on="pizza_type_id")
    orders = orders.merge(order_details, on="order_id")
    orders = orders.merge(pizzas, on="pizza_id")
    
    #Nos quedamos con las columnas que nos interesan
    orders = orders[['date', 'quantity', 'pizza_type_id', 'size', 'price', 'ingredients']]
    #Assume size is S:1, M:1,5, L:2, XL:2,5, XXL:3
    orders["size"] = orders["size"].replace({"S":1, "M":1.5, "L":2, "XL":2.5, "XXL":3})
    #Copio a un nuevo df para no modificar el original
    df_amplio = orders.copy()
    #Group by date and pizza_type_id, adding the values of size and price, ingredientts is the same, date and pizza_type_id must be conserved as columns
    orders = orders.groupby(["date", "pizza_type_id"]).agg({"size":"sum", "price":"sum", "ingredients":"first"})
    #Reset index to make date and pizza_type_id columns again
    orders = orders.reset_index()

    ingredients = list()
    for i in pizza_types["ingredients"]:
        pizza_ingredients = i.split(",")
        for j in pizza_ingredients:
            if j not in ingredients:
                ingredients.append(j)
    #Strip all ingredients
    for i in range(len(ingredients)):
        ingredients[i] = ingredients[i].strip()
    #delete repeated ingredients
    ingredients = list(set(ingredients))

    orders['date'] = pd.to_datetime(orders['date'], format="%Y-%m-%d") - pd.to_timedelta(7, unit='d')
    orders = orders.groupby(['pizza_type_id', pd.Grouper(key='date', freq='W-MON')]).agg({"size":"sum", "price":"sum", "ingredients":"first"}).reset_index()
    orders = orders.sort_values(by=['date'])
    #drop column pizza_type_id
    df = orders.drop(columns=["pizza_type_id", "price"])
    #Separate ingredients by comma
    df["ingredients"] = df["ingredients"].str.split(",")
    df = df.explode("ingredients")
    df["ingredients"] = df["ingredients"].str.strip()
    #Sum size and price by date and ingredients
    df = df.groupby(["date", "ingredients"]).agg({"size":"sum"}).reset_index()

    #A new df named price_df is based on orders, but only with the columns date, price; grouped by date and adding the values of price
    price_df = orders[["date", "price"]].groupby(["date"]).agg({"price":"sum"}).reset_index()

    #Calculate mean, mode and median of size by ingredients, making a new df
    #Initialize new df with columns: ingredient, mean, mode, median
    df_results = pd.DataFrame(columns=["ingredient", "mean", "mode", "median"])
    #Iterate over ingredients
    for i in ingredients:
        #Create a new df with the rows of df that have the ingredient i
        df_aux = df[df["ingredients"] == i]
        #Calculate mean, mode and median of size
        mean = df_aux["size"].mean()
        mode = df_aux["size"].mode()
        median = df_aux["size"].median()
        #Append the values to df_results
        df_results = pd.concat([df_results, pd.DataFrame({"ingredient":i, "mean":mean, "mode":mode, "median":median}, index=[0])], ignore_index=True)
    #Delete spaces from ingredients column
    df_results["ingredient"] = df_results["ingredient"].str.strip()
    df_results = df_results.sort_values(by=["ingredient"])

    return df, df_results, price_df, df_amplio

def load(df, df_results, price_df, df_amplio):
    #From df results save another df with the columns ingredient and mode
    df_final = df_results[["ingredient", "mode"]]
    #Rename mode column to "To buy"
    df_final = df_final.rename(columns={"mode":"to_buy"}).reset_index(drop=True)
    #Save df_final to csv
    df_final.to_csv("GeneratedResults/csv_files/next_week_supplies_2016.csv", index=False)
    #Save df_final to xml
    informe_final_XML.createXML(df_final, "GeneratedResults/xml_files/next_week_supplies_2016.xml")
    #Create reporte ejecutivo
    reporte_ejecutivo.createReport(df, df_final, price_df, df_amplio, True)
    reporte_excel.createReport(df, df_final, price_df, df_amplio, True)
    #Print "You need to buy {mode} of {ingredient} for the next week"
    for i in df_results["ingredient"]:
        print(f"You need to buy {df_results[df_results['ingredient'] == i]['mode'].values[0]} of {i} for the next week")
    print()
    print("All data saved in GeneratedResults/csv_files/next_week_supplies_2016.csv")

if __name__ == "__main__":
    #Create new folder named GeneratedResults and subfolders needed
    if not os.path.exists("GeneratedResults/csv_files"):
        os.makedirs("GeneratedResults/csv_files")
    if not os.path.exists("GeneratedResults/xml_files"):
        os.makedirs("GeneratedResults/xml_files")
    if not os.path.exists("GeneratedResults/text_files"):
        os.makedirs("GeneratedResults/text_files")
    if not os.path.exists("GeneratedResults/text_files"):
        os.makedirs("GeneratedResults/pdf_files")
    informe.crear_informe()
    informeXML.crear_informe()
    pizzas, pizza_types, orders, order_details = extract()
    week_data, results, weekly_price, df_amplio = transform(pizzas, pizza_types, orders, order_details)
    load(week_data, results, weekly_price, df_amplio)