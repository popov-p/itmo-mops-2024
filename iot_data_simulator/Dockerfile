FROM python:3.12
WORKDIR /itmo-mops-2024

COPY ./iot_proto_message ./iot_proto_message
COPY ./iot_data_simulator/data_simulator.py ./iot_data_simulator/
COPY ./iot_data_simulator/main.py ./iot_data_simulator/

COPY ./iot_data_simulator/requirements.txt ./iot_data_simulator/
RUN pip install --no-cache-dir -r ./iot_data_simulator/requirements.txt

EXPOSE 5000

CMD ["python", "-B", "-m", "iot_data_simulator.main"]