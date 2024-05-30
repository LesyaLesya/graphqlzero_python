"""Модуль с тестами query запросов для Users."""


import allure
import pytest

from config.base_test import BaseTest
from utils.helpers import Helper as h


@pytest.mark.query_users
@allure.feature('Users')
@allure.story('Query')
class TestQueryUsers(BaseTest):
    """Тесты для query users."""

    @pytest.fixture
    def f_get_id_of_all_users(self):
        """Фикстура для теста test_get_id_of_all_users"""
        data = []
        for i in range(1, 11):
            data.append({'id': str(i)})
        return self.user_generator.users_data_dict(data)

    @pytest.fixture
    def f_get_id_name_uname_users_with_limit(self):
        """Фикстура для теста test_get_id_name_uname_users_with_limit"""
        user_1 = h.data_for_list(
            id='1', name=self.user_data.USER_1['name'],
            username=self.user_data.USER_1['username'])
        user_2 = h.data_for_list(
            id='2', name=self.user_data.USER_2['name'],
            username=self.user_data.USER_2['username'])
        limit_1 = self.user_generator.users_data_dict(datas=[user_1])
        limit_2 = self.user_generator.users_data_dict(datas=[user_1, user_2])
        return {'limit1': limit_1, 'limit2': limit_2}

    @allure.title('Получение id всех юзеров')
    def test_get_id_of_all_users(self, graphqlzero, f_get_id_of_all_users, check):
        """Тестовая функция для проверки получения id всех юзеров.

        :param graphqlzero: фикстура, создающая и возвращающая экземпляр класса GraphqlClient
        """
        query = """query {users {data {id}}}"""

        response = graphqlzero.query(query)
        users_data = response.json()

        check.check_response_status_code(response, 200)
        check.check_response_time(response)
        check.validate_json(users_data, self.get_users_schema)

        with allure.step(check.response_body_msg(users_data)):
            assert users_data == f_get_id_of_all_users, \
                f'ФР - {users_data}, ОР - {f_get_id_of_all_users}'

    @pytest.mark.parametrize('limit, res', [(1, 'limit1'), (2, 'limit2')])
    @allure.title('Получение id, name и username нескольких юзеров')
    def test_get_id_name_uname_users_with_limit(
            self, graphqlzero, limit, res, f_get_id_name_uname_users_with_limit, check):
        """Тестовая функция для проверки получения id, name и username нескольких юзеров.

        :param graphqlzero: фикстура, создающая и возвращающая экземпляр класса GraphqlClient
        :param limit: количество юзеров
        :param res: ожидаемый список юзеров
        """
        query = """query ($options: PageQueryOptions) {users (options: $options) {data {id name username}}}"""

        response = graphqlzero.query(query, variables=self.query_vars.vars_limit(limit))
        users_data = response.json()

        check.check_response_status_code(response, 200)
        check.check_response_time(response)
        check.validate_json(users_data, self.get_users_schema)

        with allure.step(check.response_body_msg(users_data)):
            expected_users = f_get_id_name_uname_users_with_limit[res]
            assert users_data == expected_users, f'ФР - {users_data}, ОР - {expected_users}'
