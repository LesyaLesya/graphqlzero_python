"""Модуль с тестами mutation запросов на удаление Post."""


import allure
import pytest

from config.base_test import BaseTest


@pytest.mark.mutation_post_delete
@allure.feature('Post')
@allure.story('Mutation - Delete')
class TestMutationPostDelete(BaseTest):
    """Тесты для Mutation Delete post."""

    @pytest.mark.parametrize('idx', [1, 101])
    @allure.title('Удаление поста по id')
    def test_delete_post_by_id(self, graphqlzero, idx, check):
        """Тестовая функция для проверки удаления поста по id.

        :param graphqlzero: фикстура, создающая и возвращающая экземпляр класса GraphqlClient
        :param idx: id поста
        """
        query = """mutation ($id: ID!) {deletePost(id: $id)}"""

        response = graphqlzero.query(query, variables=self.query_vars.vars_id(idx))
        post_data = response.json()

        check.check_response_status_code(response, 200)
        check.check_response_time(response)

        with allure.step(check.response_body_msg(post_data)):
            assert post_data == self.messages.DELETED_POST['msg'], \
                f'ФР - {post_data}, ОР - {self.messages.DELETED_POST["msg"]}'
