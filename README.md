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
docker stop $(docker ps -aq) && docker rm $(docker ps -aq) && docker rmi $(docker images -q) && docker volume rm $(docker volume ls -q)


docker stop $(docker ps -aq) && docker rm $(docker ps -aq) && docker rmi $(docker images -q) - снести всё кроме volumes !


    develop:
      watch:
        - action: sync+restart
          path: .
          target: .
```


Некоторые правила: 

controller:
если
  alpha < 30 -> пакет не принимается
иначе
  пакет добавляется в БД в коллекцию data и отправляется в rabbitmq очередь


rule engine: 
  если 
  beta > 75, то срабатывает instant rule
  
  если beta < 75, то копим стек правила ongoing rule