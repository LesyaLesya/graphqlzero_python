"""Модуль с тестами mutation запросов на создание Post."""

import allure
import pytest

from config.base_test import BaseTest
from utils.helpers import Helper as h


@pytest.mark.mutation_post_create
@allure.feature('Post')
@allure.story('Mutation - Create')
class TestMutationPostCreate(BaseTest):
    """Тесты для Mutation Create post."""

    @pytest.fixture
    def f_create_post_with_body_title_get_id_title_body(self, get_params):
        """Фикстура для теста test_create_post_with_body_title_get_id_title_body"""
        return self.post_generator.post_create_data_dict(
            id='101', title=get_params['title'], body=get_params['body'])

    @pytest.mark.parametrize('get_params', [({'title': 'super', 'body': 'hello world'}),
                                            ({'title': 'Привет', 'body': 'Тест'})])
    @allure.title('Создание поста с валидными title, body')
    def test_create_post_with_body_title_get_id_title_body(
            self, graphqlzero, f_create_post_with_body_title_get_id_title_body,
            get_params, check):
        """Тестовая функция для проверки создания поста с валидными title, body.

        :param graphqlzero: фикстура, создающая и возвращающая экземпляр класса GraphqlClient
        :param get_params: название поста
        """
        query = """mutation ($input: CreatePostInput!) {createPost(input: $input) {id title body}}"""

        response = graphqlzero.query(
            query, variables=h.common_dict(
                self.query_vars.vars_title(get_params['title']),
                self.query_vars.vars_body(get_params['body'])))
        post_data = response.json()

        check.check_response_status_code(response, 200)
        check.check_response_time(response)
        check.validate_json(post_data, self.create_post_schema)

        with allure.step(check.response_body_msg(post_data)):
            assert post_data == f_create_post_with_body_title_get_id_title_body, \
                f'ФР - {post_data}, ОР - {f_create_post_with_body_title_get_id_title_body}'

    @pytest.mark.parametrize('body', ['test'])
    @allure.title('Создание поста без title')
    def test_create_post_without_title(self, graphqlzero, body, check):
        """Тестовая функция для проверки создания поста без title.

        :param graphqlzero: фикстура, создающая и возвращающая экземпляр класса GraphqlClient
        :param body: тело поста
        """
        query = """mutation ($input: CreatePostInput!) {createPost(input: $input) {id title body}}"""

        response = graphqlzero.query(query, variables=self.query_vars.vars_body(body))
        post_data = response.json()

        check.check_response_status_code(response, 200)
        check.check_response_time(response)

        with allure.step(check.response_body_msg(post_data)):
            assert post_data['errors'][0]['message'] == self.errors.create_post_wout_title(body), \
                f'ФР - {post_data["errors"][0]["message"]}'

    @pytest.mark.parametrize('title', [None, 123, False])
    @allure.title('Создание поста с невалидным title')
    def test_create_post_with_invalid_title(self, graphqlzero, title, check):
        """Тестовая функция для проверки создания поста с невалидным title.

        :param graphqlzero: фикстура, создающая и возвращающая экземпляр класса GraphqlClient
        :param title: название поста
        """
        query = """mutation ($input: CreatePostInput!) {createPost(input: $input) {id}}"""

        response = graphqlzero.query(
            query, variables=h.common_dict(
                self.query_vars.vars_body('test'), self.query_vars.vars_title(title)))
        post_data = response.json()

        check.check_response_status_code(response, 200)
        check.check_response_time(response)

        with allure.step(check.response_body_msg(post_data)):
            assert post_data['errors'][0]['message'] == self.errors.create_post_invalid_title(title), \
                   f'ФР - {post_data["errors"][0]["message"]}'
