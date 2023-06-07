"""Модуль с тестами mutation запросов на изменение Post."""


import allure
import pytest

from helpers.base_functions import vars_body, vars_title, common_dict
from helpers.data import Post as p
from helpers.schemas.post_schemas import UPDATE_POST_SCHEMA


@pytest.fixture
def f_update_post_title_get_id_body_title(post_update_data_dict, get_params):
    """Фикстура для теста test_update_post_title_get_id_body_title"""
    return post_update_data_dict(id='1', title=get_params, body=p.POST_1['body'])


@pytest.fixture
def f_update_post_title_body_get_body_title(post_update_data_dict, get_params):
    """Фикстура для теста test_update_post_title_body_get_body_title"""
    return post_update_data_dict(body=get_params['body'], title=get_params['title'])


@pytest.mark.mutation_post_update
@allure.feature('Post')
@allure.story('Mutation - Update')
class TestMutationPostUpdate:
    """Тесты для Mutation Update post."""

    @pytest.mark.parametrize('get_params', ['test', '123', None])
    @allure.title('Обновление названия поста')
    def test_update_post_title_get_id_body_title(
            self, graphqlzero,  validate_json, check_response_status_code,
            response_body_msg, check_response_time, f_update_post_title_get_id_body_title,
            get_params):
        """Тестовая функция для проверки обновления названия поста.

        :param graphqlzero: фикстура, создающая и возвращающая экземпляр класса GraphqlClient
        :param validate_json: фикстура для валидации JSON схемы
        :param check_response_status_code: фикстура, проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param check_response_time: фикстура проверки времени ответа
        :param get_params: название поста
        """
        query = """mutation ($input: UpdatePostInput!) {updatePost(id: 1, input: $input) {id body title}}"""

        response = graphqlzero.query(query, variables=vars_title(get_params))
        post_data = response.json()

        check_response_status_code(response, 200)
        check_response_time(response)
        validate_json(post_data, UPDATE_POST_SCHEMA)

        with allure.step(response_body_msg(post_data)):
            assert post_data == f_update_post_title_get_id_body_title, \
                f'ФР - {post_data}, ОР - {f_update_post_title_get_id_body_title}'

    @pytest.mark.parametrize('get_params', [({'title': 'super', 'body': 'hello world'}),
                                            ({'title': None, 'body': None})])
    @allure.title('Обновление названия поста')
    def test_update_post_title_body_get_body_title(
            self, graphqlzero, validate_json, check_response_status_code,
            response_body_msg, check_response_time,
            get_params, f_update_post_title_body_get_body_title):
        """Тестовая функция для проверки обновления названия и тела поста.

        :param graphqlzero: фикстура, создающая и возвращающая экземпляр класса GraphqlClient
        :param validate_json: фикстура для валидации JSON схемы
        :param check_response_status_code: фикстура, проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param check_response_time: фикстура проверки времени ответа
        :param get_params: название поста
        """
        query = """mutation ($input: UpdatePostInput!) {updatePost(id: 1, input: $input) {body title}}"""

        response = graphqlzero.query(
            query, variables=common_dict(vars_title(get_params['title']), vars_body(get_params['body'])))
        post_data = response.json()

        check_response_status_code(response, 200)
        check_response_time(response)
        validate_json(post_data, UPDATE_POST_SCHEMA)

        with allure.step(response_body_msg(post_data)):
            assert post_data == f_update_post_title_body_get_body_title, \
                f'ФР - {post_data}, ОР - {f_update_post_title_body_get_body_title}'
