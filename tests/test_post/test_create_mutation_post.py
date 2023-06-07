"""Модуль с тестами mutation запросов на создание Post."""

import allure
import pytest

from helpers.schemas.post_schemas import CREATE_POST_SCHEMA
from helpers.data import Errors as er
from helpers.base_functions import vars_body, vars_title, common_dict


@pytest.fixture
def f_create_post_with_body_title_get_id_title_body(post_create_data_dict, get_params):
    """Фикстура для теста test_create_post_with_body_title_get_id_title_body"""
    return post_create_data_dict(
        id='101', title=get_params['title'], body=get_params['body'])


@pytest.mark.mutation_post_create
@allure.feature('Post')
@allure.story('Mutation - Create')
class TestMutationPostCreate:
    """Тесты для Mutation Create post."""

    @pytest.mark.parametrize('get_params', [({'title': 'super', 'body': 'hello world'}),
                                            ({'title': 'Привет', 'body': 'Тест'})])
    @allure.title('Создание поста с валидными title, body')
    def test_create_post_with_body_title_get_id_title_body(
            self, graphqlzero,  validate_json, check_response_status_code,
            response_body_msg, check_response_time, f_create_post_with_body_title_get_id_title_body,
            get_params):
        """Тестовая функция для проверки создания поста с валидными title, body.

        :param graphqlzero: фикстура, создающая и возвращающая экземпляр класса GraphqlClient
        :param validate_json: фикстура для валидации JSON схемы
        :param check_response_status_code: фикстура, проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param check_response_time: фикстура проверки времени ответа
        :param get_params: название поста
        """
        query = """mutation ($input: CreatePostInput!) {createPost(input: $input) {id title body}}"""

        response = graphqlzero.query(
            query, variables=common_dict(vars_title(get_params['title']), vars_body(get_params['body'])))
        post_data = response.json()

        check_response_status_code(response, 200)
        check_response_time(response)
        validate_json(post_data, CREATE_POST_SCHEMA)

        with allure.step(response_body_msg(post_data)):
            assert post_data == f_create_post_with_body_title_get_id_title_body, \
                f'ФР - {post_data}, ОР - {f_create_post_with_body_title_get_id_title_body}'

    @pytest.mark.parametrize('body', ['test'])
    @allure.title('Создание поста без title')
    def test_create_post_without_title(
            self, graphqlzero, validate_json, check_response_status_code,
            response_body_msg, check_response_time, body):
        """Тестовая функция для проверки создания поста без title.

        :param graphqlzero: фикстура, создающая и возвращающая экземпляр класса GraphqlClient
        :param validate_json: фикстура для валидации JSON схемы
        :param check_response_status_code: фикстура, проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param check_response_time: фикстура проверки времени ответа
        :param body: тело поста
        """
        query = """mutation ($input: CreatePostInput!) {createPost(input: $input) {id title body}}"""

        response = graphqlzero.query(query, variables=vars_body(body))
        post_data = response.json()

        check_response_status_code(response, 400)
        check_response_time(response)

        with allure.step(response_body_msg(post_data)):
            assert post_data['errors'][0]['message'] == er.create_post_wout_title(body), \
                f'ФР - {post_data}'

    @pytest.mark.parametrize('title', [None, 123, False])
    @allure.title('Создание поста с невалидным title')
    def test_create_post_with_invalid_title(
            self, graphqlzero, validate_json, check_response_status_code,
            response_body_msg, check_response_time, title):
        """Тестовая функция для проверки создания поста с невалидным title.

        :param graphqlzero: фикстура, создающая и возвращающая экземпляр класса GraphqlClient
        :param validate_json: фикстура для валидации JSON схемы
        :param check_response_status_code: фикстура, проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param check_response_time: фикстура проверки времени ответа
        :param title: название поста
        """
        query = """mutation ($input: CreatePostInput!) {createPost(input: $input) {id}}"""

        response = graphqlzero.query(
            query, variables=common_dict(vars_body('test'), vars_title(title)))
        post_data = response.json()

        check_response_status_code(response, 400)
        check_response_time(response)

        with allure.step(response_body_msg(post_data)):
            assert post_data['errors'][0]['message'] == er.create_post_invalid_title(title), \
                   f'ФР - {post_data}'
