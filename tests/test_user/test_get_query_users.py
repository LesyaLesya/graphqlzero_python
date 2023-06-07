"""Модуль с тестами query запросов для Users."""


import allure
import pytest

from helpers.base_functions import data_for_list, vars_limit
from helpers.data import User as u
from helpers.schemas.user_schemas import GET_USERS_SCHEMA


@pytest.fixture
def f_get_id_of_all_users(users_data_dict):
    """Фикстура для теста test_get_id_of_all_users"""
    data = []
    for i in range(1, 11):
        data.append({'id': str(i)})
    return users_data_dict(data)


@pytest.fixture
def f_get_id_name_uname_users_with_limit(users_data_dict):
    """Фикстура для теста test_get_id_name_uname_users_with_limit"""
    user_1 = data_for_list(id='1', name=u.USER_1['name'], username=u.USER_1['username'])
    user_2 = data_for_list(id='2', name=u.USER_2['name'], username=u.USER_2['username'])
    limit_1 = users_data_dict(datas=[user_1])
    limit_2 = users_data_dict(datas=[user_1, user_2])
    return {'limit1': limit_1, 'limit2': limit_2}


@pytest.mark.query_users
@allure.feature('Users')
@allure.story('Query')
class TestQueryUsers:
    """Тесты для query users."""

    @allure.title('Получение id всех юзеров')
    def test_get_id_of_all_users(
            self, graphqlzero,  validate_json, check_response_status_code,
            response_body_msg, check_response_time, f_get_id_of_all_users):
        """Тестовая функция для проверки получения id всех юзеров.

        :param graphqlzero: фикстура, создающая и возвращающая экземпляр класса GraphqlClient
        :param validate_json: фикстура для валидации JSON схемы
        :param check_response_status_code: фикстура, проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param check_response_time: фикстура проверки времени ответа
        """
        query = """query {users {data {id}}}"""

        response = graphqlzero.query(query)
        users_data = response.json()

        check_response_status_code(response, 200)
        check_response_time(response)
        validate_json(users_data, GET_USERS_SCHEMA)

        with allure.step(response_body_msg(users_data)):
            assert users_data == f_get_id_of_all_users, \
                f'ФР - {users_data}, ОР - {f_get_id_of_all_users}'

    @pytest.mark.parametrize('limit, res', [(1, 'limit1'), (2, 'limit2')])
    @allure.title('Получение id, name и username нескольких юзеров')
    def test_get_id_name_uname_users_with_limit(
            self, graphqlzero, validate_json, check_response_status_code,
            response_body_msg, check_response_time, limit, res, f_get_id_name_uname_users_with_limit):
        """Тестовая функция для проверки получения id, name и username нескольких юзеров.

        :param graphqlzero: фикстура, создающая и возвращающая экземпляр класса GraphqlClient
        :param validate_json: фикстура для валидации JSON схемы
        :param check_response_status_code: фикстура, проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param check_response_time: фикстура проверки времени ответа
        :param limit: количество юзеров
        :param res: ожидаемый список юзеров
        """
        query = """query ($options: PageQueryOptions) {users (options: $options) {data {id name username}}}"""

        response = graphqlzero.query(query, variables=vars_limit(limit))
        users_data = response.json()

        check_response_status_code(response, 200)
        check_response_time(response)
        validate_json(users_data, GET_USERS_SCHEMA)

        with allure.step(response_body_msg(users_data)):
            expected_users = f_get_id_name_uname_users_with_limit[res]
            assert users_data == expected_users, f'ФР - {users_data}, ОР - {expected_users}'
