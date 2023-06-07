"""Модуль с тестами mutation запросов на удаление Post."""


import allure
import pytest

from helpers.base_functions import vars_id
from helpers.data import Messages as m


@pytest.mark.mutation_post_delete
@allure.feature('Post')
@allure.story('Mutation - Delete')
class TestMutationPostDelete:
    """Тесты для Mutation Delete post."""

    @pytest.mark.parametrize('idx', [1, 101])
    @allure.title('Удаление поста по id')
    def test_delete_post_by_id(
            self, graphqlzero,  validate_json, check_response_status_code,
            response_body_msg, check_response_time, idx):
        """Тестовая функция для проверки удаления поста по id.

        :param graphqlzero: фикстура, создающая и возвращающая экземпляр класса GraphqlClient
        :param validate_json: фикстура для валидации JSON схемы
        :param check_response_status_code: фикстура, проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param check_response_time: фикстура проверки времени ответа
        :param idx: id поста
        """
        query = """mutation ($id: ID!) {deletePost(id: $id)}"""

        response = graphqlzero.query(query, variables=vars_id(idx))
        post_data = response.json()

        check_response_status_code(response, 200)
        check_response_time(response)

        with allure.step(response_body_msg(post_data)):
            assert post_data == m.DELETED_POST['msg'], \
                f'ФР - {post_data}, ОР - {m.DELETED_POST["msg"]}'
