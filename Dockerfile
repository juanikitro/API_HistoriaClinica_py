FROM python:3.10

ENV PYTHONUNBUFFERED 1

WORKDIR /code

RUN apt-get update && apt-get install -y gcc g++ unixodbc-dev

# Instalar el controlador ODBC para SQL Server
RUN apt-get install -y curl
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql17

RUN pip install --upgrade pip

COPY ./requirements.txt /code/requirements.txt

RUN pip install -r /code/requirements.txt

COPY ./app/src /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
