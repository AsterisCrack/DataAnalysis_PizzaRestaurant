
#Voy a crear un reporte ejecutivo de la empresa
#Usare matplotlib para graficar
#Guardare todo en un archivo pdf
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
import os
import sys
import fpdf

def createReport(df, df_results, price_df, df_amplio, is2016=False):
    #df tiene datos de los ingredientes usados por semana
    #df_results tiene datos de los ingredientes usados en total por semana
    #price_df tiene datos de los beneficios totales por semana
    #df_amplio tiene datos de cada orden, que incluye la fecha, cantidad, tipo de pizza, tamaño, precio y ingredientes
    create_graphs(df, df_results, price_df, df_amplio)
    create_pdf(price_df, is2016)

def create_graphs(df, df_results, price_df, df_amplio):
    #If folder doesn't exist, create it
    if not os.path.exists("graphs"):
        os.makedirs("graphs")
    #Grafico de beneficios por semana con seaborn
    #Grafico de lineas
    sns.set_style("darkgrid")
    ax = sns.lineplot(x="date", y="price", data=price_df)
    ax.set(xlabel='Fecha', ylabel='Dólares')
    plt.title("Total recaudado por semana")
    plt.savefig("graphs/price.png")
    plt.clf()

    #Grafico de ingredientes usados por semana con seaborn
    #Cada ingrediente es una linea
    #Creo df_Aux que es df pero solo los datos de las filas cuyos ingredientes sean: Pepperonni y Tomatoes
    df_aux = df.iloc[df.index[df['ingredients'].isin(["Mozzarella Cheese", "Tomatoes", "Eggplant", "Thyme"])]]

    sns.set_style("darkgrid")
    ax = sns.lineplot(x="date", y="size", hue="ingredients", data=df_aux)
    ax.set(xlabel='Fecha', ylabel='Cantidad')
    plt.title("Ingredientes usados por semana")
    plt.savefig("graphs/ingredients.png")
    plt.clf()

    #Me aseguro de que todas las filas de size sean float
    df_amplio['size'] = df_amplio['size'].astype(float)
    #Grafico de pizzas más populares en general
    #guardo un df aux con sólo la columna de el tipo de pizza y el size
    df_aux = df_amplio[["pizza_type_id", "size"]]
    #Agrupo por tipo de pizza y sumo los tamaños
    df_aux = df_aux.groupby("pizza_type_id").sum()
    df_aux = df_aux.sort_values(by="size", ascending=False)
    #Grafico de pie con las 10 pizzas más populares
    #Sin leyenda, indicando el valor de size como valor real, no porcentual
    #Guarda el df
    def absolute_value(val):
        a  = np.round(val/100.*df_aux[:10]["size"].sum(), 0)
        return a
    #Uso colores de seaborn
    colors = sns.color_palette("YlOrRd")

    df_aux[:10].plot.pie(y="size", legend=False, colors=colors, autopct=absolute_value, ylabel="")
    plt.title("Pizzas más populares")
    plt.savefig("graphs/pizza_popular.png")
    plt.clf()

    #Lo mismo para las 10 pizzas menos populares
    df_aux = df_aux.sort_values(by="size", ascending=True)
    df_aux[:10].plot.pie(y="size", legend=False, colors=colors, autopct=absolute_value, ylabel="")
    plt.title("Pizzas menos populares")
    plt.savefig("graphs/pizza_no_popular.png")
    plt.clf()

    #Agrego una tabla con los datos de los ingredientes usados en total
    df = df_results
    alternating_colors = [['white'] * 2, ['whitesmoke'] * 2] * len(df)
    alternating_colors = alternating_colors[:len(df)]
    fig, ax = plt.subplots(figsize=(13,20))
    ax.axis('tight')
    ax.axis('off')
    the_table = ax.table(cellText=df[["ingredient", "to_buy"]].values,
                        colLabels="Ingredientes Cantidad".split(), #Column names:
                        colColours=['tomato']*2,
                        cellColours=alternating_colors,
                        loc='center',
                        cellLoc='center')
    #To make the text bigger
    the_table.auto_set_font_size(False)
    the_table.set_fontsize(12)
    #To make the table fill the page
    the_table.scale(1, 1.5)
    #Guardo la tabla como una imagen
    plt.axis("off")
    plt.savefig("graphs/table.png")

def create_pdf(price_df, is2016):
    #Si no existe el folder, lo creo
    if not os.path.exists("GeneratedResults/pdf_files"):
        os.makedirs("GeneratedResults/pdf_files")
    if not is2016:
        FILE = "GeneratedResults/pdf_files/ReporteEjecutivo.pdf"
    else:
        FILE = "GeneratedResults/pdf_files/ReporteEjecutivo2016.pdf"
    #Creo el pdf
    pdf = fpdf.FPDF()
    pdf.add_page()
    
    #Agrego el titulo, con la fuente mas grande y en bold y underline
    pdf.set_font("Arial", size=20, style="BU")
    if not is2016:
        pdf.cell(200, 10, txt="Reporte para Maven Pizzas en 2015", ln=1, align="C")
    else:
        pdf.cell(200, 10, txt="Reporte para Maven Pizzas en 2016", ln=1, align="C")

    pdf.set_font("Arial", size=16, style="B")
    pdf.cell(200, 10, txt=" ", ln=1, align="C")
    #Agrego explicacion para el grafico de ingredientes
    pdf.cell(200, 10, txt="Análisis de ganancias por semana:", ln=1, align="C")
    #Agrego las imagenes
    pdf.image("graphs/price.png", x=45, y=40, w=130)
    pdf.set_font("Arial", size=14)
    for i in range(10):
        pdf.cell(200, 10, txt=" ", ln=1, align="C")
    text = "En total se han recaudado {:.2f} dólares este año.".format(price_df['price'].sum())
    pdf.cell(200, 10, txt=text, ln=1, align="C")

    pdf.cell(200, 10, txt=" ", ln=1, align="C")
    pdf.set_font("Arial", size=14, style="B")
    pdf.cell(200, 10, txt="Análisis uso de algunos ingredientes importantes y otros poco utilizados:", ln=1, align="C")
    pdf.image("graphs/ingredients.png", x=45, y=175, w=130)

    pdf.add_page()
    pdf.set_font("Arial", size=16, style="B")
    pdf.cell(200, 10, txt="Análisis de popularidad de las pizzas:", ln=1, align="C")
    pdf.image("graphs/pizza_popular.png", x=30, y=30, w=150)
    pdf.image("graphs/pizza_no_popular.png", x=30, y=130, w=150)
    for i in range(24):
        pdf.cell(200, 10, txt=" ", ln=1, align="C")
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt="En la siguiente página se muestran los ingredientes a comprar cada semana.", ln=1, align="C")
    
    pdf.add_page()
    
    #Agrego la imagen de la tabla al pdf
    pdf.image("graphs/table.png", x=-15, y=-30, w=230)

    #Guardo el pdf
    pdf.output(FILE)
    
    #Elimino las imagenes
    os.remove("graphs/price.png")
    os.remove("graphs/ingredients.png")
    os.remove("graphs/pizza_popular.png")
    os.remove("graphs/pizza_no_popular.png")
    os.remove("graphs/table.png")
    #Elimino el folder
    os.rmdir("graphs")
