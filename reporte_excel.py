
import pandas as pd
import numpy as np
import os

def createReport(df, df_results, price_df, df_amplio, is2016=False):
    #df tiene datos de los ingredientes usados por semana
    #df_results tiene datos de los ingredientes usados en total por semana
    #price_df tiene datos de los beneficios totales por semana
    #df_amplio tiene datos de cada orden, que incluye la fecha, cantidad, tipo de pizza, tamaño, precio y ingredientes
    #Esta vez lo haremos todo en la misma función
    if not os.path.exists("GeneratedResults/xlsx_files"):
        os.makedirs("GeneratedResults/xlsx_files")
    if not is2016:
        FILE = "GeneratedResults/xlsx_files/ReporteEjecutivo.xlsx"
    else:
        FILE = "GeneratedResults/xlsx_files/ReporteEjecutivo2016.xlsx"

    xlsxwriter = pd.ExcelWriter(FILE, engine='xlsxwriter', date_format="dd/mm/yyyy")
    workbook = xlsxwriter.book
    hoja_reporteEjecutivo(xlsxwriter, workbook, price_df)
    hoja_ingredientes(xlsxwriter, workbook, df, df_results)
    hoja_pedidos(xlsxwriter, workbook, df_amplio)
    xlsxwriter.save()

def hoja_reporteEjecutivo(xlsxwriter, workbook, price_df):
    
    #Grafico de Reporte Ejecutivo
    price_df.to_excel(xlsxwriter, sheet_name="Reporte Ejecutivo")
    worksheet = xlsxwriter.sheets["Reporte Ejecutivo"]
    #Date column is in format dd/mm/yyyy
    #Read it correctly
    #Format date column
    bold = workbook.add_format({'bold': True})
    date_format = workbook.add_format({'num_format': 'dd/mm/yyyy'})
    worksheet.set_column('B:B', 15, date_format)

    chart = workbook.add_chart({'type': 'line'})
    chart.add_series({
        'name':       ['Reporte Ejecutivo', 0, 1],
        'categories': ['Reporte Ejecutivo', 1, 1, len(price_df), 1],
        'values':     ['Reporte Ejecutivo', 1, 2, len(price_df), 2],
    })
    chart.set_title({'name': 'Total recaudado por semana'})
    chart.set_x_axis({'name': 'Fecha'})
    chart.set_y_axis({'name': 'Beneficios'})
    #A big chart
    chart.set_size({'width': 720, 'height': 576})
    chart.set_style(11)
    worksheet.insert_chart('F8', chart)
    #Añadir texto de "En total se vendieron..."
    text = "En total se han recaudado {:.2f} dólares este año.".format(price_df['price'].sum())
    worksheet.write('G2', text, bold)

def hoja_ingredientes(xlsxwriter, workbook, df, df_results):
    #Grafico de ingredientes usados por semana
    df_aux = df.iloc[df.index[df['ingredients'].isin(["Mozzarella Cheese", "Tomatoes", "Eggplant", "Thyme"])]]
    #Cada ingrediente en una columna
    new_cols = ["date", "Mozzarella Cheese", "Tomatoes", "Eggplant", "Thyme"]
    df_new = pd.DataFrame(columns=new_cols)
    df_new["date"] = df_aux["date"]
    for ing in new_cols[1:]:
        df_new[ing] = df_aux[df_aux["ingredients"] == ing]["size"]
    df_new = df_new.fillna(0)
    #Sumar ingredientes por semana
    df_new = df_new.groupby("date").sum()
    df_new = df_new.reset_index()
    df_new.to_excel(xlsxwriter, sheet_name="Ingredientes")
    worksheet = xlsxwriter.sheets["Ingredientes"]
    #Format date column
    date_format = workbook.add_format({'num_format': 'dd/mm/yyyy'})
    worksheet.set_column('B:B', 15, date_format)

    #Añadir texto explicativo
    bold = workbook.add_format({'bold': True})
    text = "Muestra del uso de dos igredientes muy usados y dos poco usados en las pizzas."
    worksheet.write('J2', text, bold)

    chart = workbook.add_chart({'type': 'line'})
    for i in range(len(new_cols)-1):
        chart.add_series({
            'name':       ['Ingredientes', 0, i+2],
            'categories': ['Ingredientes', 1, 1, len(df_new), 1],
            'values':     ['Ingredientes', 1, i+2, len(df_new), i+2],
        })
    chart.set_title({'name': 'Ingredientes usados por semana'})
    chart.set_x_axis({'name': 'Fecha'})
    chart.set_y_axis({'name': 'Cantidad de ingredientes'})
    #A big chart
    chart.set_size({'width': 720, 'height': 576})
    chart.set_style(12)
    worksheet.insert_chart('H4', chart)

    df_results.to_excel(xlsxwriter, sheet_name="Ingredientes", startrow=3, startcol=19, index=False)
    
    #Hago que la tabla se vea bien ensanchando las columnas necesarias
    #Con border=1 se ve bien
    w_border = workbook.add_format({'border': 1})
    worksheet.set_column('T:T', 25, w_border)
    worksheet.set_column('U:U', 10, w_border)
    #Aplico estilo al header de la tabla
    header_format = workbook.add_format({
        'bold': True,
        'text_wrap': False,
        'valign': 'top',
        'fg_color': '#fa3232',
        'color': 'white',
        'font_size': 16,
        'align': 'center',
        'border': 1})
    for col_num, value in enumerate(df_results.columns.values):
        worksheet.write(3, col_num + 19, value, header_format)
    Bold_grande = workbook.add_format({'bold': True, 'font_size': 15})
    texto = "INGREDIENTES A COMPRAR LA SEMANA QUE VIENE"
    worksheet.write('S2', texto, Bold_grande)

def hoja_pedidos(xlsxwriter, workbook, df_amplio):
    #Me aseguro de que todas las filas de size sean float
    df_amplio['size'] = df_amplio['size'].astype(float)
    #Grafico de pizzas más populares en general
    #guardo un df aux con sólo la columna de el tipo de pizza y el size
    df_aux = df_amplio[["pizza_type_id", "size"]]
    #Agrupo por tipo de pizza y sumo los tamaños
    df_aux = df_aux.groupby("pizza_type_id").sum()
    df_aux = df_aux.sort_values(by="size", ascending=False)
    df_aux = df_aux.reset_index()

    #Df aux 2 cantidad de pedidos por día
    df_aux2 = df_amplio[["date", "price"]]
    #Nueva columna con 1 para contar
    df_aux2.insert(1, "count", 1)
    df_aux2 = df_aux2.groupby("date").sum()
    #Hay que dividir price entre count
    df_aux2["price"] = df_aux2["price"] / df_aux2["count"]
    df_aux2 = df_aux2.sort_values(by="price", ascending=False)
    df_aux2 = df_aux2.reset_index()

    #Df aux 3 cantidad de pedidos por día de la semana
    df_aux3 = df_aux2[["date", "count", "price"]]
    #Make sure date is datetime
    try:
        df_aux3["date"] = pd.to_datetime(df_aux3["date"], format="%d/%m/%Y")
    except:
        df_aux3["date"] = pd.to_datetime(df_aux3["date"], format="%Y-%m-%d")
    df_aux3["day"] = df_aux3["date"].dt.day_name()
    #Delete date column
    df_aux3 = df_aux3.drop(columns=["date"])
    df_aux3 = df_aux3.groupby("day").sum()
    df_aux3 = df_aux3.sort_values(by="count", ascending=False)
    df_aux3 = df_aux3.reset_index()

    #Ambos a excel
    df_aux.to_excel(xlsxwriter, sheet_name="Pedidos", startrow=0, startcol=0, index=False)
    df_aux3.to_excel(xlsxwriter, sheet_name="Pedidos", startrow=0, startcol=3, index=False)
    worksheet = xlsxwriter.sheets["Pedidos"]

    def make_pie_chart(row_ini, row_fin):
        chart = workbook.add_chart({'type': 'pie'})
        chart.add_series({
            'name':       'Pedidos',
            'categories': ['Pedidos', row_ini, 0, row_fin, 0],
            'values':     ['Pedidos', row_ini, 1, row_fin, 1],
            #Data labels: Mostrar el valor y el nombre de la pizza, sin leyenda a la derecha
            'data_labels': {'value': True, 'category': True, 'percentage': False, 'separator': '\n', 'legend': False},
        })

        return chart
    #Grafico de pie con las 10 pizzas más populares
    chart = make_pie_chart(1, 11)
    chart.set_title({'name': 'Pizzas más populares'})
    #Use monochromatic pallette 5, green gradient
    chart.set_style(5)
    chart.set_size({'width': 500, 'height': 400})
    worksheet.insert_chart('H1', chart)

    #Grafico de pie con las 10 pizzas menos populares
    chart = make_pie_chart(len(df_aux)-10, len(df_aux))
    chart.set_title({'name': 'Pizzas menos populares'})
    #Use monochromatic pallette 4, red gradient
    chart.set_style(4)
    chart.set_size({'width': 500, 'height': 400})
    worksheet.insert_chart('H21', chart)

    #Grafico de barras qué días de la semana se venden más pizzas
    def barras(col):
        chart = workbook.add_chart({'type': 'column'})
        chart.add_series({
            'name':       'Pedidos',
            'categories': ['Pedidos', 1, 3, 6, 3],
            'values':     ['Pedidos', 1, col, 6, col],
        })
        return chart
    chart = barras(4)
    chart.set_title({'name': 'Pedidos por día de la semana'})
    chart.set_y_axis({'name': 'Cantidad de pedidos'})
    chart.set_x_axis({'name': 'Día de la semana'})
    chart.set_style(11)
    chart.set_size({'width': 500, 'height': 400})
    worksheet.insert_chart('P1', chart)

    #Grafico de barras qué días de la semana se gasta más por pedido
    chart = barras(5)
    chart.set_title({'name': 'Gasto por pedido por día de la semana'})
    chart.set_y_axis({'name': 'Gasto por pedido'})
    chart.set_x_axis({'name': 'Día de la semana'})
    chart.set_style(11)
    chart.set_size({'width': 500, 'height': 400})
    worksheet.insert_chart('P21', chart)
