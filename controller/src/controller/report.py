import redis
import asyncio
from statistics import mean
import logging

logger = logging.getLogger()

r = redis.Redis(host='redis', port=6379, db=0)

class RedisMetricsReporter:
    def __init__(self, host='redis', port=6379, db=0):
        print("RedisMetricsReporter __init__(...)")
        self.r = redis.Redis(host=host, port=port, db=db)
        self.total_requests_by_segment = 0
        self.accepted_requests_by_segment = 0
        self.declined_requests_by_segment = 0
        self.segment_alpha_values = []
        self.segment_beta_values = []

    def connect_to_redis(self):
        try:
            response = self.r.ping()
            if response:
                print("Подключение к Redis успешно!")
            else:
                print("Ошибка подключения к Redis.")
        except Exception as e:
            print(f"Ошибка подключения к Redis: {e}")

    async def send_metrics_to_redis(self):
        while True:
            await asyncio.sleep(30)
            if self.segment_alpha_values and self.segment_beta_values:
                avg_alpha = mean(self.segment_alpha_values)
                avg_beta = mean(self.segment_beta_values)
            else:
                avg_alpha = avg_beta = 0

            self.r.set("accepted_segment_requests", self.accepted_requests_by_segment)
            self.r.set("declined_segment_requests", self.declined_requests_by_segment)
            self.r.set("avg_segment_alpha", avg_alpha)
            self.r.set("avg_segment_beta", avg_beta)

            print(f"Отчет в Redis обновлен. Принятых запросов: {self.accepted_requests_by_segment}, "
                  f"Отклоненных: {self.declined_requests_by_segment}, "
                  f"Среднее alpha: {avg_alpha}, Среднее beta: {avg_beta}")

            self.reset_metrics()

    async def start_background_tasks(self):
        asyncio.create_task(self.send_metrics_to_redis())

    def increment_accepted_requests(self):
        self.accepted_requests_by_segment += 1

    def increment_declined_requests(self):
        self.declined_requests_by_segment += 1

    def add_fields_data(self, alpha, beta):
        self.segment_alpha_values.append(alpha)
        self.segment_beta_values.append(beta)

    def reset_metrics(self):
        self.segment_alpha_values = []
        self.segment_beta_values = []
        self.total_requests_by_segment = 0
        self.accepted_requests_by_segment = 0
        self.declined_requests_by_segment = 0
        print("Данные сброшены. Кэш-метрики очищены.")


metrics_reporter = RedisMetricsReporter()


