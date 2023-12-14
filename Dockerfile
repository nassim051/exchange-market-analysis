FROM python
WORKDIR /app
COPY . /app
RUN pip install pytest six
ENV PYTHONPATH "${PYTHONPATH}:/app"
CMD ["python3","src/main.py"]