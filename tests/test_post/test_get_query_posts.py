"""Модуль с тестами query запросов для Posts."""


import allure
import pytest

from config.base_test import BaseTest
from utils.helpers import Helper as h


@pytest.mark.query_posts
@allure.feature('Posts')
@allure.story('Query')
class TestQueryPosts(BaseTest):
    """Тесты для query posts."""

    @pytest.fixture
    def f_get_id_of_all_posts(self):
        """Фикстура для теста test_get_id_of_all_posts"""
        data = []
        for i in range(1, 101):
            data.append({'id': str(i)})
        return self.post_generator.posts_data_dict(data)

    @pytest.fixture
    def f_get_id_title_body_posts_with_limit(self):
        """Фикстура для теста test_get_id_title_body_posts_with_limit"""
        post_1 = h.data_for_list(id='1', title=self.post_data.POST_1['title'], body=self.post_data.POST_1['body'])
        post_2 = h.data_for_list(id='2', title=self.post_data.POST_2['title'], body=self.post_data.POST_2['body'])
        limit_1 = self.post_generator.posts_data_dict(datas=[post_1])
        limit_2 = self.post_generator.posts_data_dict(datas=[post_1, post_2])
        return {'limit1': limit_1, 'limit2': limit_2}

    @allure.title('Получение id всех постов')
    def test_get_id_of_all_posts(
            self, graphqlzero, f_get_id_of_all_posts, check):
        """Тестовая функция для проверки получения id всех постов.

        :param graphqlzero: фикстура, создающая и возвращающая экземпляр класса GraphqlClient
        """
        query = """query {posts{data {id}}}"""

        response = graphqlzero.query(query)
        post_data = response.json()

        check.check_response_status_code(response, 200)
        check.check_response_time(response)
        check.validate_json(post_data, self.get_posts_schema)

        with allure.step(check.response_body_msg(post_data)):
            assert post_data == f_get_id_of_all_posts, \
                f'ФР - {post_data}, ОР - {f_get_id_of_all_posts}'

    @pytest.mark.parametrize('limit, res', [(1, 'limit1'), (2, 'limit2')])
    @allure.title('Получение id, названия и тела нескольких постов')
    def test_get_id_title_body_posts_with_limit(
            self, graphqlzero, limit, res, f_get_id_title_body_posts_with_limit, check):
        """Тестовая функция для проверки получения id, названия и тела нескольких постов.

        :param graphqlzero: фикстура, создающая и возвращающая экземпляр класса GraphqlClient
        :param limit: количество постов
        :param res: ожидаемый список постов
        """
        query = """query ($options: PageQueryOptions){posts(options: $options) {data {id title body}}}"""

        response = graphqlzero.query(query, variables=self.query_vars.vars_limit(limit))
        post_data = response.json()

        check.check_response_status_code(response, 200)
        check.check_response_time(response)
        check.validate_json(post_data, self.get_posts_schema)

        with allure.step(check.response_body_msg(post_data)):
            expected_posts = f_get_id_title_body_posts_with_limit[res]
            assert post_data == expected_posts, f'ФР - {post_data}, ОР - {expected_posts}'
