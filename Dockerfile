FROM python:3.9

ADD pizzas.py .
ADD informe.py .
ADD limpiar.py .
ADD pizzas_2016.py .
ADD informe_2016.py .
ADD informe_2016_xml.py .
ADD informeXML.py .
ADD informe_final_XML.py .

COPY data_files /data_files
COPY data_files_2016 /data_files_2016

RUN pip intall -r requirements.txt

#Comment or uncomment the following line to run the script that you like
CMD [ "python", "./pizzas_2016.py" ]
#CMD [ "python", "./pizzas.py" ]