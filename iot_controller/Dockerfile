FROM python:3.12
WORKDIR /itmo-mops-2024

COPY ./iot_proto_message ./iot_proto_message/
COPY ./iot_controller/main.py ./iot_controller/

COPY ./iot_controller/requirements.txt ./iot_controller/
RUN pip install --no-cache-dir -r ./iot_controller/requirements.txt

EXPOSE 5000

CMD ["python", "-B", "-m", "iot_controller.main"]