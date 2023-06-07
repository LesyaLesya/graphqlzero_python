"""Модуль с классом Graphql клиента."""

import allure
import json
import logging
import requests


class GraphqlClient:
    """Класс для выполнения запросов."""

    def __init__(self, host, schema):
        """Конструктор класса.

        :param host: адрес хоста
        :param schema: схема
        """
        self.host = host
        self.schema = schema
        self.session = requests.Session()
        self.logger = logging.getLogger('requests')

    def _get_url(self):
        return f'{self.schema}://{self.host}'

    def query(self, query, variables=None):
        """Возвращает вызов query запроса.

        :param query: тело запроса
        :param variables: переменные для запроса
        """
        url = self._get_url()
        data = {'query': query}
        if variables:
            data['variables'] = variables

        with allure.step(f'Выполнить query на {url}, data={data}'):
            res = self.session.post(url=url, json=data)
            self.logger.info(f'Метод и урл запроса: {res.request.method} {res.request.url}')
            self.logger.info(f'Тело запроса: {res.request.body}')
            try:
                self.logger.info(f'Тело ответа: {res.json()}')
            except json.decoder.JSONDecodeError as err:
                self.logger.error(f'Невалидный json в ответе. Error: {err}')
                self.logger.info(f'Тело ответа: {res.content}')
            return res
