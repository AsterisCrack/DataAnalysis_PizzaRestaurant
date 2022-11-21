
import pandas as pd
import xml.etree.ElementTree as ET

def pretty(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            pretty(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def createXML(df, f):
    #Tengo un df de la forma del de next_week_supplies.csv
    #Creo un XML con el formato de next_week_supplies.xml
    root = ET.Element("root")
    for i in df.index:
        row = ET.SubElement(root, "row")
        row.set("id", str(i))
        for j in df.columns:
            ET.SubElement(row, j).text = str(df.loc[i,j])
    pretty(root)
    #Creando el archivo XML
    tree = ET.ElementTree(root)
    tree.write(f)

        
