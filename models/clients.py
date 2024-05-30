"""Модуль с классом Graphql клиента."""

import allure
import logging
import requests

from utils.helpers import Helper as h


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
        data['variables'] = variables if variables else None

        with allure.step(f'Выполнить query на {url}, data={data}, variables={variables}'):
            res = self.session.post(url=url, json=data)
            h.attach_response_to_log(self.logger, res)
            h.attach_response_to_allure(res)
            return res
