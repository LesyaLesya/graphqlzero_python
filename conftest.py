"""Модуль с фикстурами."""


import logging
import pytest
import yaml

from utils.assertions import Assertions
from models.clients import GraphqlClient


def pytest_addoption(parser):
    parser.addoption('--schema', action='store', default='https', choices=['https', 'http'])
    parser.addoption('--host', action='store', default='default')


@pytest.fixture(scope='session')
def cfg():
    with open('config.yml', 'r', encoding='utf-8') as file:
        config = yaml.load(file, yaml.SafeLoader)
    return config


@pytest.fixture(scope='session')
def get_host(cfg, request):
    r = request.config.getoption('--host')
    return cfg['host'][r]


@pytest.fixture(scope='session')
def get_schema(cfg, request):
    r = request.config.getoption('--schema')
    return cfg['schema'][r]


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


@pytest.fixture
def get_params(request):
    return request.param


@pytest.fixture(scope='session')
def graphqlzero(get_host, get_schema, logger_test):
    """Фикстура, создающая и возвращающая экземпляр класса GraphqlClient."""
    host = get_host
    schema = get_schema
    logger_test.info(
        f'Инициализация экземпляра GraphqlClient: host {host}, schema {schema}')
    return GraphqlClient(host, schema)


@pytest.fixture(scope='session')
def check():
    return Assertions()
