"""Модуль с тестами query запросов для User."""


import allure
import pytest

from helpers.base_functions import common_dict, vars_id
from helpers.data import User as u
from helpers.schemas.post_schemas import POSTS_SCHEMA
from helpers.schemas.user_schemas import GET_USER_SCHEMA


@pytest.fixture
def f_get_user_id_uname_name_email_phone_web_addr(user_data_dict, address_data_dict):
    """Фикстура для теста test_get_user_id_uname_name_email_phone_web_addr"""
    data_user_1 = user_data_dict(
        id='1', username=u.USER_1['username'], name=u.USER_1['name'],
        email=u.USER_1['email'], phone=u.USER_1['phone'], website=u.USER_1['website'])
    address_user_1 = address_data_dict(lat=u.USER_1['address']['geo']['lat'],
                                       lng=u.USER_1['address']['geo']['lng'])
    expected_user_1 = common_dict(data_user_1, address_user_1)
    data_user_2 = user_data_dict(
        id='2', username=u.USER_2['username'], name=u.USER_2['name'],
        email=u.USER_2['email'], phone=u.USER_2['phone'], website=u.USER_2['website'])
    address_user_2 = address_data_dict(lat=u.USER_2['address']['geo']['lat'],
                                       lng=u.USER_2['address']['geo']['lng'])
    expected_user_2 = common_dict(data_user_2, address_user_2)
    return {'user1': expected_user_1, 'user2': expected_user_2}


@pytest.fixture
def f_get_user_name_phone(user_data_dict):
    """Фикстура для теста test_get_user_name_phone"""
    expected_user_1 = user_data_dict(name=u.USER_1['name'], phone=u.USER_1['phone'])
    expected_user_2 = user_data_dict(name=u.USER_2['name'], phone=u.USER_2['phone'])
    return {'user1': expected_user_1, 'user2': expected_user_2}


@pytest.fixture
def f_get_user_id_uname_name_email_phone_web_addr_by_unexist_id(user_data_dict):
    """Фикстура для теста test_get_user_id_uname_name_email_phone_web_addr_by_unexist_id"""
    return user_data_dict(
        id=None, username=None, name=None, email=None, phone=None, website=None, address=None)


@pytest.fixture
def f_get_user_all_id_posts(user_posts_data_dict):
    """Фикстура для теста test_get_user_all_id_posts"""
    data = []
    for i in range(1, 11):
        data.append({'id': str(i)})
    return user_posts_data_dict(data)


@pytest.mark.query_user
@allure.feature('User')
@allure.story('Query')
class TestQueryUser:
    """Тесты для query user."""

    @pytest.mark.parametrize('idx, res', [(1, 'user1'), (2, 'user2')])
    @allure.title('Получение id, username, name, email, phone, web, addr юзера по существующему id')
    def test_get_user_id_uname_name_email_phone_web_addr(
            self, graphqlzero,  validate_json, check_response_status_code,
            response_body_msg, check_response_time, idx,
            f_get_user_id_uname_name_email_phone_web_addr, res):
        """Тестовая функция для проверки получения id, username, name,
        email, phone, web, addr юзера по существующему id.

        :param graphqlzero: фикстура, создающая и возвращающая экземпляр класса GraphqlClient
        :param validate_json: фикстура для валидации JSON схемы
        :param check_response_status_code: фикстура, проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param check_response_time: фикстура проверки времени ответа
        :param idx: id юзера
        :param res: ожидаемый юзер
        """
        query = """query ($id: ID!){user(id: $id){id username name 
        email phone website address {geo {lat lng}}}}"""

        response = graphqlzero.query(query, variables=vars_id(idx))
        user_data = response.json()

        check_response_status_code(response, 200)
        check_response_time(response)
        validate_json(user_data, GET_USER_SCHEMA)

        with allure.step(response_body_msg(user_data)):
            expected_user = f_get_user_id_uname_name_email_phone_web_addr[res]
            assert user_data == expected_user, f'ФР - {user_data}, ОР - {expected_user}'

    @pytest.mark.parametrize('idx, res', [(1, 'user1'), (2, 'user2')])
    @allure.title('Получение name, phone юзера по существующему id')
    def test_get_user_name_phone(
            self, graphqlzero, validate_json, check_response_status_code,
            response_body_msg, check_response_time, idx, res, f_get_user_name_phone):
        """Тестовая функция для проверки получения name, phone юзера по существующему id.

        :param graphqlzero: фикстура, создающая и возвращающая экземпляр класса GraphqlClient
        :param validate_json: фикстура для валидации JSON схемы
        :param check_response_status_code: фикстура, проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param check_response_time: фикстура проверки времени ответа
        :param idx: id юзера
        :param res: ожидаемый юзер
        """
        query = """query ($id: ID!){user(id: $id){name phone}}"""

        response = graphqlzero.query(query, variables=vars_id(idx))
        user_data = response.json()

        check_response_status_code(response, 200)
        check_response_time(response)
        validate_json(user_data, GET_USER_SCHEMA)

        with allure.step(response_body_msg(user_data)):
            expected_user = f_get_user_name_phone[res]
            assert user_data == expected_user, f'ФР - {user_data}, ОР - {expected_user}'

    @allure.title('Получение id, username, name, email, phone, web, addr юзера по несуществующему id')
    def test_get_user_id_uname_name_email_phone_web_addr_by_unexist_id(
            self, graphqlzero, validate_json, check_response_status_code,
            response_body_msg, check_response_time,
            f_get_user_id_uname_name_email_phone_web_addr_by_unexist_id):
        """Тестовая функция для проверки получения id, username, name,
        email, phone, web, addr юзера по несуществующему id.

        :param graphqlzero: фикстура, создающая и возвращающая экземпляр класса GraphqlClient
        :param validate_json: фикстура для валидации JSON схемы
        :param check_response_status_code: фикстура, проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param check_response_time: фикстура проверки времени ответа
        """
        query = """query {user(id: 101){id username name email phone website address {geo {lat lng}}}}"""

        response = graphqlzero.query(query)
        user_data = response.json()

        check_response_status_code(response, 200)
        check_response_time(response)
        validate_json(user_data, GET_USER_SCHEMA)

        with allure.step(response_body_msg(user_data)):
            assert user_data == f_get_user_id_uname_name_email_phone_web_addr_by_unexist_id, \
                f'ОР - {f_get_user_id_uname_name_email_phone_web_addr_by_unexist_id}, ФР - {user_data}'

    @allure.title('Получение id всех постов юзера')
    def test_get_user_all_id_posts(
            self, graphqlzero, validate_json, check_response_status_code,
            response_body_msg, check_response_time, f_get_user_all_id_posts):
        """Тестовая функция для проверки получения id всех постов юзера.

        :param graphqlzero: фикстура, создающая и возвращающая экземпляр класса GraphqlClient
        :param validate_json: фикстура для валидации JSON схемы
        :param check_response_status_code: фикстура, проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param check_response_time: фикстура проверки времени ответа
        """
        query = """query {user(id: 1){posts {data {id}}}}"""

        response = graphqlzero.query(query)
        user_data = response.json()
        post_data = user_data['data']['user']['posts']

        check_response_status_code(response, 200)
        check_response_time(response)
        validate_json(user_data, GET_USER_SCHEMA)
        validate_json(post_data, POSTS_SCHEMA)

        with allure.step(response_body_msg(user_data)):
            assert user_data == f_get_user_all_id_posts, \
                f'ОР - {f_get_user_all_id_posts}, ФР - {user_data}'
