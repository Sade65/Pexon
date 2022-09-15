FROM python:alpine3.6
WORKDIR /app
COPY ./ /app
RUN pip install flask
RUN pip install pysqlite3
CMD ["python", "main.py"]