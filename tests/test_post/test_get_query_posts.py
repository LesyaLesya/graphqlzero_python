"""Модуль с тестами query запросов для Posts."""


import allure
import pytest


from helpers.base_functions import vars_limit, data_for_list
from helpers.data import Post as p
from helpers.schemas.post_schemas import GET_POSTS_SCHEMA


@pytest.fixture
def f_get_id_of_all_posts(posts_data_dict):
    """Фикстура для теста test_get_id_of_all_posts"""
    data = []
    for i in range(1, 101):
        data.append({'id': str(i)})
    return posts_data_dict(data)


@pytest.fixture
def f_get_id_title_body_posts_with_limit(posts_data_dict):
    """Фикстура для теста test_get_id_title_body_posts_with_limit"""
    post_1 = data_for_list(id='1', title=p.POST_1['title'], body=p.POST_1['body'])
    post_2 = data_for_list(id='2', title=p.POST_2['title'], body=p.POST_2['body'])
    limit_1 = posts_data_dict(datas=[post_1])
    limit_2 = posts_data_dict(datas=[post_1, post_2])
    return {'limit1': limit_1, 'limit2': limit_2}


@pytest.mark.query_posts
@allure.feature('Posts')
@allure.story('Query')
class TestQueryPosts:
    """Тесты для query posts."""

    @allure.title('Получение id всех постов')
    def test_get_id_of_all_posts(
            self, graphqlzero,  validate_json, check_response_status_code,
            response_body_msg, check_response_time, f_get_id_of_all_posts):
        """Тестовая функция для проверки получения id всех постов.

        :param graphqlzero: фикстура, создающая и возвращающая экземпляр класса GraphqlClient
        :param validate_json: фикстура для валидации JSON схемы
        :param check_response_status_code: фикстура, проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param check_response_time: фикстура проверки времени ответа
        """
        query = """query {posts{data {id}}}"""

        response = graphqlzero.query(query)
        post_data = response.json()

        check_response_status_code(response, 200)
        check_response_time(response)
        validate_json(post_data, GET_POSTS_SCHEMA)

        with allure.step(response_body_msg(post_data)):
            assert post_data == f_get_id_of_all_posts, \
                f'ФР - {post_data}, ОР - {f_get_id_of_all_posts}'

    @pytest.mark.parametrize('limit, res', [(1, 'limit1'), (2, 'limit2')])
    @allure.title('Получение id, названия и тела нескольких постов')
    def test_get_id_title_body_posts_with_limit(
            self, graphqlzero, validate_json, check_response_status_code,
            response_body_msg, check_response_time, limit, res, f_get_id_title_body_posts_with_limit):
        """Тестовая функция для проверки получения id, названия и тела нескольких постов.

        :param graphqlzero: фикстура, создающая и возвращающая экземпляр класса GraphqlClient
        :param validate_json: фикстура для валидации JSON схемы
        :param check_response_status_code: фикстура, проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param check_response_time: фикстура проверки времени ответа
        :param limit: количество постов
        :param res: ожидаемый список постов
        """
        query = """query ($options: PageQueryOptions){posts(options: $options) {data {id title body}}}"""

        response = graphqlzero.query(query, variables=vars_limit(limit))
        post_data = response.json()

        check_response_status_code(response, 200)
        check_response_time(response)
        validate_json(post_data, GET_POSTS_SCHEMA)

        with allure.step(response_body_msg(post_data)):
            expected_posts = f_get_id_title_body_posts_with_limit[res]
            assert post_data == expected_posts, f'ФР - {post_data}, ОР - {expected_posts}'
