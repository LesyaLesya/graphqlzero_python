"""Модуль с тестами mutation запросов на изменение Post."""


import allure
import pytest

from config.base_test import BaseTest
from utils.helpers import Helper as h


@pytest.mark.mutation_post_update
@allure.feature('Post')
@allure.story('Mutation - Update')
class TestMutationPostUpdate(BaseTest):
    """Тесты для Mutation Update post."""

    @pytest.fixture
    def f_update_post_title_get_id_body_title(self, get_params):
        """Фикстура для теста test_update_post_title_get_id_body_title"""
        return self.post_generator.post_update_data_dict(
            id='1', title=get_params, body=self.post_data.POST_1['body'])

    @pytest.fixture
    def f_update_post_title_body_get_body_title(self, get_params):
        """Фикстура для теста test_update_post_title_body_get_body_title"""
        return self.post_generator.post_update_data_dict(
            body=get_params['body'], title=get_params['title'])

    @pytest.mark.parametrize('get_params', ['test', '123', None])
    @allure.title('Обновление названия поста')
    def test_update_post_title_get_id_body_title(
            self, graphqlzero, f_update_post_title_get_id_body_title, get_params, check):
        """Тестовая функция для проверки обновления названия поста.

        :param graphqlzero: фикстура, создающая и возвращающая экземпляр класса GraphqlClient
        :param get_params: название поста
        """
        query = """mutation ($input: UpdatePostInput!) {updatePost(id: 1, input: $input) {id body title}}"""

        response = graphqlzero.query(query, variables=self.query_vars.vars_title(get_params))
        post_data = response.json()

        check.check_response_status_code(response, 200)
        check.check_response_time(response)
        check.validate_json(post_data, self.update_post_schema)

        with allure.step(check.response_body_msg(post_data)):
            assert post_data == f_update_post_title_get_id_body_title, \
                f'ФР - {post_data}, ОР - {f_update_post_title_get_id_body_title}'

    @pytest.mark.parametrize('get_params', [({'title': 'super', 'body': 'hello world'}),
                                            ({'title': None, 'body': None})])
    @allure.title('Обновление названия поста')
    def test_update_post_title_body_get_body_title(
            self, graphqlzero, get_params, f_update_post_title_body_get_body_title, check):
        """Тестовая функция для проверки обновления названия и тела поста.

        :param graphqlzero: фикстура, создающая и возвращающая экземпляр класса GraphqlClient
        :param get_params: название поста
        """
        query = """mutation ($input: UpdatePostInput!) {updatePost(id: 1, input: $input) {body title}}"""

        response = graphqlzero.query(
            query, variables=h.common_dict(self.query_vars.vars_title(get_params['title']),
                                           self.query_vars.vars_body(get_params['body'])))
        post_data = response.json()

        check.check_response_status_code(response, 200)
        check.check_response_time(response)
        check.validate_json(post_data, self.update_post_schema)

        with allure.step(check.response_body_msg(post_data)):
            assert post_data == f_update_post_title_body_get_body_title, \
                f'ФР - {post_data}, ОР - {f_update_post_title_body_get_body_title}'
