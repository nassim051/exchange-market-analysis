FROM python
WORKDIR /app
COPY . /app
RUN apt update && apt install -y sqlite3

RUN apt-get update --fix-missing \
    && apt-get install -y sqlite3 nodejs npm \
    && rm -rf /var/lib/apt/lists/* \
    && pip install pytest six pycoingecko date_time_event python-dateutil pycryptodome jsii
RUN pip install binance-connector==3.5.1 

ENV PYTHONPATH "${PYTHONPATH}:/app"
CMD ["python3","src/main.py"]