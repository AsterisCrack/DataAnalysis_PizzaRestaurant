FROM python:3.9

ADD pizzas.py .
ADD informe.py .

COPY data_files /data_files

RUN pip install pandas

CMD [ "python", "./pizzas.py" ]