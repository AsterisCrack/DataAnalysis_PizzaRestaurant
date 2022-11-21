FROM python:3.9

ADD pizzas.py .
ADD informe.py .
ADD limpiar.py .
ADD pizzas_2016.py .
ADD informe_2016.py .


COPY data_files /data_files
COPY data_files_2016 /data_files_2016

RUN pip intall -r requirements.txt

CMD [ "python", "./pizzas.py" ]