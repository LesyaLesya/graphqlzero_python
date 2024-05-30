"""Модуль с общими вспомогательными функциями."""

import allure
import json
from mergedeep import merge

from allure_commons.types import AttachmentType


class Helper:

    @staticmethod
    def attach_response_to_allure(response):
        """Прикрепление тела ответа к allure отчету."""
        try:
            res = json.dumps(response.json(), indent=4)
            allure.attach(body=res, name='API Response', attachment_type=AttachmentType.JSON)
        except json.decoder.JSONDecodeError:
            allure.attach(body=response.content, name='API Response', attachment_type=AttachmentType.TEXT)

    @staticmethod
    def attach_response_to_log(logger, response):
        """Прикрепление тела ответа к лог файлу."""
        logger.info(f'Метод и урл запроса: {response.request.method} {response.request.url}')
        logger.info(f'Тело запроса: {response.request.body}')
        try:
            logger.info(f'Тело ответа: {response.json()}')
        except json.decoder.JSONDecodeError as err:
            logger.error(f'Невалидный json в ответе. Error: {err}')
            logger.info(f'Тело ответа: {response.content}')

    @staticmethod
    def common_dict(*args):
        """Функция мержа словарей."""
        return merge(*args)

    @staticmethod
    def data_for_list(**kwargs):
        return kwargs
