
#This file does the same as informe.py but writes the results in an XML file istead of txt
import pandas as pd
import xml.etree.ElementTree as ET
from xml.dom import minidom

def prettify(elem):
    #Return a pretty-printed XML string for the Element.
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def analyze(df, f):
    #Necesito indentar el XML para que sea mas legible
    ET.SubElement(f, "NaN_totales").text = str(df.isna().sum().sum())
    ET.SubElement(f, "NaN_por_columna").text = str(df.isna().sum())
    ET.SubElement(f, "Nulls_totales").text = str(df.isnull().sum().sum())
    ET.SubElement(f, "Nulls_por_columna").text = str(df.isnull().sum())
    ET.SubElement(f, "Cada_columna_representa_el_siguiente_tipo_de_dato").text = str(df.dtypes)
    
def crear_informe():
    FILE = "GeneratedResults/xml_files/informe_calidad.xml"
    DATA = ('data_files/data_dictionary.csv','data_files/order_details.csv','data_files/orders.csv','data_files/pizza_types.csv','data_files/pizzas.csv')
    root = ET.Element("root")
    for i in DATA:
        tabla = ET.SubElement(root, "tabla")
        tabla.set("nombre", i)
        analyze(pd.read_csv(i, sep=",", encoding="LATIN_1"), tabla)
        
    with open(FILE, "w") as f:
        f.write(prettify(root))
    print("Análisis finalizado")
    print(f"Guardado en el archivo {FILE}")

