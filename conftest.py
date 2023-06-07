"""Модуль с фикстурами."""

import allure
import jsonschema
import logging
import pytest
import yaml
from jsonschema import validate

from helpers.clients import GraphqlClient


def pytest_addoption(parser):
    parser.addoption('--schema', action='store', default='https', choices=['https', 'http'])
    parser.addoption('--host', action='store', default='default')


@pytest.fixture(scope='session')
def parser_schema(request):
    return request.config.getoption('--schema')


@pytest.fixture(scope='session')
def parser_host(request):
    return request.config.getoption('--host')


@pytest.fixture(scope='session', autouse=True)
def logger_test():
    logger = logging.getLogger('testing')
    return logger


@pytest.fixture(autouse=True)
def log_test_description(request, logger_test):
    logger_test.info(f'___Test "{request.node.nodeid}" START')
    yield
    logger_test.info(f'___Test "{request.node.nodeid}" COMPLETE')


@pytest.fixture(scope='module', autouse=True)
def log_module_description(request, logger_test):
    logger_test.info(f'_____START testing module {request.node.name}')
    yield
    logger_test.info(f'_____STOP testing module {request.node.name}')


@pytest.fixture(scope='session')
def graphqlzero(get_host, get_schema, logger_test):
    """Фикстура, создающая и возвращающая экземпляр класса GraphqlClient."""
    host = get_host
    schema = get_schema
    logger_test.info(
        f'Инициализация экземпляра GraphqlClient: host {host}, schema {schema}')
    return GraphqlClient(host, schema)


@pytest.fixture(scope='session')
def cfg():
    with open('helpers/config.yml', 'r', encoding='utf-8') as file:
        config = yaml.load(file, yaml.SafeLoader)
    return config


@pytest.fixture(scope='session')
def get_host(cfg, parser_host):
    return cfg['host'][parser_host]


@pytest.fixture(scope='session')
def get_schema(cfg, parser_schema):
    return cfg['schema'][parser_schema]


@pytest.fixture
def validate_json(logger_test):
    """Фикстура валидации json схемы."""
    @allure.step('Провалидировать схему для тела ответа {json_data}')
    def _validate(json_data, base_schema):
        try:
            logger_test.info(f'Валидация схемы для тела {json_data}, схема: {base_schema}')
            validate(instance=json_data, schema=base_schema)
        except jsonschema.exceptions.ValidationError:
            assert False
        assert True
    return _validate


@pytest.fixture
def check_response_status_code(logger_test):
    """Фикстура проверки кода ответа."""
    @allure.step('Проверить, что код ответа {code}')
    def _check_response_status_code(response, code):
        assert response.status_code == code, f'Код ответа {response.status_code}, ОР {code}'
    return _check_response_status_code


@pytest.fixture
def response_body_msg(logger_test):
    def _response_body_msg(body):
        logger_test.info(f'Проверить тело ответа - {body}')
        return f'Проверить тело ответа - {body}'
    return _response_body_msg


@pytest.fixture
def check_response_time(logger_test):
    """Фикстура проверки времени ответа."""
    @allure.step('Проверить, что время ответа меньше {tims_ms} ms')
    def _check_response_time(response, tims_ms=1000):
        actual_time = response.elapsed.total_seconds() * 1000
        assert actual_time < tims_ms, f'Время ответа {actual_time}, ОР {tims_ms} ms'
    return _check_response_time


@pytest.fixture
def get_params(request):
    return request.param
