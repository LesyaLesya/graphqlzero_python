"""Модуль с тестами query запросов для User."""


import allure
import pytest

from config.base_test import BaseTest
from utils.helpers import Helper as h


@pytest.mark.query_user
@allure.feature('User')
@allure.story('Query')
class TestQueryUser(BaseTest):
    """Тесты для query user."""

    @pytest.fixture
    def f_get_user_id_uname_name_email_phone_web_addr(self):
        """Фикстура для теста test_get_user_id_uname_name_email_phone_web_addr"""
        data_user_1 = self.user_generator.user_data_dict(
            id='1', username=self.user_data.USER_1['username'], name=self.user_data.USER_1['name'],
            email=self.user_data.USER_1['email'], phone=self.user_data.USER_1['phone'],
            website=self.user_data.USER_1['website'])
        address_user_1 = self.user_generator.address_data_dict(
            lat=self.user_data.USER_1['address']['geo']['lat'],
            lng=self.user_data.USER_1['address']['geo']['lng'])
        expected_user_1 = h.common_dict(data_user_1, address_user_1)
        data_user_2 = self.user_generator.user_data_dict(
            id='2', username=self.user_data.USER_2['username'], name=self.user_data.USER_2['name'],
            email=self.user_data.USER_2['email'], phone=self.user_data.USER_2['phone'],
            website=self.user_data.USER_2['website'])
        address_user_2 = self.user_generator.address_data_dict(
            lat=self.user_data.USER_2['address']['geo']['lat'],
            lng=self.user_data.USER_2['address']['geo']['lng'])
        expected_user_2 = h.common_dict(data_user_2, address_user_2)
        return {'user1': expected_user_1, 'user2': expected_user_2}

    @pytest.fixture
    def f_get_user_name_phone(self):
        """Фикстура для теста test_get_user_name_phone"""
        expected_user_1 = self.user_generator.user_data_dict(
            name=self.user_data.USER_1['name'], phone=self.user_data.USER_1['phone'])
        expected_user_2 = self.user_generator.user_data_dict(
            name=self.user_data.USER_2['name'], phone=self.user_data.USER_2['phone'])
        return {'user1': expected_user_1, 'user2': expected_user_2}

    @pytest.fixture
    def f_get_user_id_uname_name_email_phone_web_addr_by_unexist_id(self):
        """Фикстура для теста test_get_user_id_uname_name_email_phone_web_addr_by_unexist_id"""
        return self.user_generator.user_data_dict(
            id=None, username=None, name=None, email=None, phone=None, website=None, address=None)

    @pytest.fixture
    def f_get_user_all_id_posts(self):
        """Фикстура для теста test_get_user_all_id_posts"""
        data = []
        for i in range(1, 11):
            data.append({'id': str(i)})
        return self.user_generator.user_posts_data_dict(data)

    @pytest.mark.parametrize('idx, res', [(1, 'user1'), (2, 'user2')])
    @allure.title('Получение id, username, name, email, phone, web, addr юзера по существующему id')
    def test_get_user_id_uname_name_email_phone_web_addr(
            self, graphqlzero, idx, f_get_user_id_uname_name_email_phone_web_addr, res, check):
        """Тестовая функция для проверки получения id, username, name,
        email, phone, web, addr юзера по существующему id.

        :param graphqlzero: фикстура, создающая и возвращающая экземпляр класса GraphqlClient
        :param idx: id юзера
        :param res: ожидаемый юзер
        """
        query = """query ($id: ID!){user(id: $id){id username name 
        email phone website address {geo {lat lng}}}}"""

        response = graphqlzero.query(query, variables=self.query_vars.vars_id(idx))
        user_data = response.json()

        check.check_response_status_code(response, 200)
        check.check_response_time(response)
        check.validate_json(user_data, self.get_user_schema)

        with allure.step(check.response_body_msg(user_data)):
            expected_user = f_get_user_id_uname_name_email_phone_web_addr[res]
            assert user_data == expected_user, f'ФР - {user_data}, ОР - {expected_user}'

    @pytest.mark.parametrize('idx, res', [(1, 'user1'), (2, 'user2')])
    @allure.title('Получение name, phone юзера по существующему id')
    def test_get_user_name_phone(
            self, graphqlzero, idx, res, f_get_user_name_phone, check):
        """Тестовая функция для проверки получения name, phone юзера по существующему id.

        :param graphqlzero: фикстура, создающая и возвращающая экземпляр класса GraphqlClient
        :param idx: id юзера
        :param res: ожидаемый юзер
        """
        query = """query ($id: ID!){user(id: $id){name phone}}"""

        response = graphqlzero.query(query, variables=self.query_vars.vars_id(idx))
        user_data = response.json()

        check.check_response_status_code(response, 200)
        check.check_response_time(response)
        check.validate_json(user_data, self.get_user_schema)

        with allure.step(check.response_body_msg(user_data)):
            expected_user = f_get_user_name_phone[res]
            assert user_data == expected_user, f'ФР - {user_data}, ОР - {expected_user}'

    @allure.title('Получение id, username, name, email, phone, web, addr юзера по несуществующему id')
    def test_get_user_id_uname_name_email_phone_web_addr_by_unexist_id(
            self, graphqlzero, f_get_user_id_uname_name_email_phone_web_addr_by_unexist_id, check):
        """Тестовая функция для проверки получения id, username, name,
        email, phone, web, addr юзера по несуществующему id.

        :param graphqlzero: фикстура, создающая и возвращающая экземпляр класса GraphqlClient
        """
        query = """query {user(id: 101){id username name email phone website address {geo {lat lng}}}}"""

        response = graphqlzero.query(query)
        user_data = response.json()

        check.check_response_status_code(response, 200)
        check.check_response_time(response)
        check.validate_json(user_data, self.get_user_schema)

        with allure.step(check.response_body_msg(user_data)):
            assert user_data == f_get_user_id_uname_name_email_phone_web_addr_by_unexist_id, \
                f'ОР - {f_get_user_id_uname_name_email_phone_web_addr_by_unexist_id}, ФР - {user_data}'

    @allure.title('Получение id всех постов юзера')
    def test_get_user_all_id_posts(self, graphqlzero, f_get_user_all_id_posts, check):
        """Тестовая функция для проверки получения id всех постов юзера.

        :param graphqlzero: фикстура, создающая и возвращающая экземпляр класса GraphqlClient
        """
        query = """query {user(id: 1){posts {data {id}}}}"""

        response = graphqlzero.query(query)
        user_data = response.json()
        post_data = user_data['data']['user']['posts']

        check.check_response_status_code(response, 200)
        check.check_response_time(response)
        check.validate_json(user_data, self.get_user_schema)
        check.validate_json(post_data, self.posts_schema)

        with allure.step(check.response_body_msg(user_data)):
            assert user_data == f_get_user_all_id_posts, \
                f'ОР - {f_get_user_all_id_posts}, ФР - {user_data}'
