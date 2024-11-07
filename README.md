# Многоуровневая организация программных систем 2024
## Архитектура разрабатываемой IoT системы
![Архитектура системы](architecture.png)


### Сборка и/или запуск
```
docker compose up --watch
```
```
python -B -m iot_data_simulator.main
python -B -m iot_controller.main
```
```
docker build -t iot_data_simulator -f iot_data_simulator/Dockerfile .
docker build -t iot_controller -f iot_controller/Dockerfile .
docker run -d --entrypoint /bin/sh pyds:latest -c "while true; do sleep 1000; done"
docker run -it --entrypoint /bin/sh pcont
docker stop $(docker ps -aq) && docker rm $(docker ps -aq) && docker rmi $(docker images -q)
```
