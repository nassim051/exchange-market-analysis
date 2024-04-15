FROM python
WORKDIR /app
COPY . /app
RUN apt-get update \
    && apt-get install -y nodejs npm \
    && rm -rf /var/lib/apt/lists/*
RUN pip install pytest six pycoingecko  date_time_event python-dateutil pycryptodome jsii
RUN pip install binance-connector==3.5.1 

ENV PYTHONPATH "${PYTHONPATH}:/app"
CMD ["python3","src/main.py"]