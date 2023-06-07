"""Модуль с тестами query запросов для Post."""


import allure
import pytest

from helpers.schemas.post_schemas import GET_POST_SCHEMA
from helpers.data import Post as p, User as u, Comments as c, Errors as er
from helpers.base_functions import vars_id, vars_limit, vars_sort, common_dict, data_for_list


@pytest.fixture
def f_get_post_id_title_body(post_data_dict):
    """Фикстура для теста test_get_post_id_title_body"""
    expected_post_1 = post_data_dict(
        id='1', title=p.POST_1['title'], body=p.POST_1['body'])
    expected_post_2 = post_data_dict(
        id='2', title=p.POST_2['title'], body=p.POST_2['body'])
    return {'post1': expected_post_1, 'post2': expected_post_2}


@pytest.fixture
def f_get_post_title(post_data_dict):
    """Фикстура для теста test_get_post_title"""
    expected_post_1 = post_data_dict(title=p.POST_1['title'])
    expected_post_2 = post_data_dict(title=p.POST_2['title'])
    return {'post1': expected_post_1, 'post2': expected_post_2}


@pytest.fixture
def f_get_post_id_title_body_by_unexist_id(post_data_dict):
    """Фикстура для теста test_get_post_id_title_body_by_unexist_id"""
    return post_data_dict(id=None, title=None, body=None)


@pytest.fixture
def f_get_post_user_data(post_user_data_dict):
    """Фикстура для теста test_get_post_user_data"""
    return post_user_data_dict(
        id='1', name=u.USER_1['name'], phone=u.USER_1['phone'],
        email=u.USER_1['email'], username=u.USER_1['username'])


@pytest.fixture
def f_comments_for_post_1():
    """Фикстура для теста test_get_post_comments"""
    comment_1 = data_for_list(
        id='1', name=c.COMMENT_1['name'], body=c.COMMENT_1['body'])
    comment_2 = data_for_list(
        id='2', name=c.COMMENT_2['name'], body=c.COMMENT_2['body'])
    comment_3 = data_for_list(
        id='3', name=c.COMMENT_3['name'], body=c.COMMENT_3['body'])
    comment_4 = data_for_list(
        id='4', name=c.COMMENT_4['name'], body=c.COMMENT_4['body'])
    comment_5 = data_for_list(
        id='5', name=c.COMMENT_5['name'], body=c.COMMENT_5['body'])
    return [comment_1, comment_2, comment_3, comment_4, comment_5]


@pytest.fixture
def f_comments_for_post_2():
    """Фикстура для теста test_get_post_comments"""
    comment_6 = data_for_list(
        id='6', name=c.COMMENT_6['name'], body=c.COMMENT_6['body'])
    comment_7 = data_for_list(
        id='7', name=c.COMMENT_7['name'], body=c.COMMENT_7['body'])
    comment_8 = data_for_list(
        id='8', name=c.COMMENT_8['name'], body=c.COMMENT_8['body'])
    comment_9 = data_for_list(
        id='9', name=c.COMMENT_9['name'], body=c.COMMENT_9['body'])
    comment_10 = data_for_list(
        id='10', name=c.COMMENT_10['name'], body=c.COMMENT_10['body'])
    return [comment_6, comment_7, comment_8, comment_9, comment_10]


@pytest.fixture
def f_get_post_comments(f_comments_for_post_1, f_comments_for_post_2, post_comments_dict):
    """Фикстура для теста test_get_post_comments"""
    comments_for_post_1 = f_comments_for_post_1
    comments_for_post_2 = f_comments_for_post_2
    res_1 = post_comments_dict(datas=comments_for_post_1)
    res_2 = post_comments_dict(datas=comments_for_post_2)
    return {'post1': res_1, 'post2': res_2}


@pytest.fixture
def f_get_post_comments_with_limit(f_comments_for_post_1, post_comments_dict):
    """Фикстура для теста test_get_post_comments_with_limit"""
    def __limit_comments(n):
        comments = f_comments_for_post_1
        return post_comments_dict(datas=comments[:n])
    return __limit_comments


@pytest.fixture
def f_get_post_comments_with_desc_sort(f_comments_for_post_1, post_comments_dict):
    """Фикстура для теста test_get_post_comments_with_desc_sort"""
    def __sort_comments(key):
        comments = f_comments_for_post_1
        sorted_comments = sorted(comments, key=lambda x: x[key], reverse=True)
        return post_comments_dict(datas=sorted_comments)
    return __sort_comments


@pytest.fixture
def f_get_post_comments_with_sort_and_limit(f_comments_for_post_1, post_comments_dict):
    """Фикстура для теста test_get_post_comments_with_sort_and_limit"""
    def __sort_limit_comments(n, key, reverse):
        comments = f_comments_for_post_1
        if reverse == 'DESC':
            rev = True
        else:
            rev = False
        sorted_comments = sorted(comments, key=lambda x: x[key], reverse=rev)[:n]
        return post_comments_dict(datas=sorted_comments)
    return __sort_limit_comments


@pytest.mark.query_post
@allure.feature('Post')
@allure.story('Query')
class TestQueryPost:
    """Тесты для query post."""

    @pytest.mark.parametrize('idx, res', [(1, 'post1'), (2, 'post2')])
    @allure.title('Получение id, названия и тела поста по существующему id')
    def test_get_post_id_title_body(
            self, graphqlzero,  validate_json, check_response_status_code,
            response_body_msg, check_response_time, idx, res, f_get_post_id_title_body):
        """Тестовая функция для проверки получения id, названия и тела поста по существующему id.

        :param graphqlzero: фикстура, создающая и возвращающая экземпляр класса GraphqlClient
        :param validate_json: фикстура для валидации JSON схемы
        :param check_response_status_code: фикстура, проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param check_response_time: фикстура проверки времени ответа
        :param idx: id поста
        :param res: ожидаемый пост
        """
        query = """query ($id: ID!){post(id: $id){id title body}}"""

        response = graphqlzero.query(query, variables=vars_id(idx))
        post_data = response.json()

        check_response_status_code(response, 200)
        check_response_time(response)
        validate_json(post_data, GET_POST_SCHEMA)

        with allure.step(response_body_msg(post_data)):
            expected_post = f_get_post_id_title_body[res]
            assert post_data == expected_post, f'ФР - {post_data}, ОР - {expected_post}'

    @pytest.mark.parametrize('idx, res', [(1, 'post1'), (2, 'post2')])
    @allure.title('Получение названия поста по существующему id')
    def test_get_post_title(
            self, graphqlzero, validate_json, check_response_status_code,
            response_body_msg, check_response_time, idx, res, f_get_post_title):
        """Тестовая функция для проверки получения названия поста по существующему id.

        :param graphqlzero: фикстура, создающая и возвращающая экземпляр класса GraphqlClient
        :param validate_json: фикстура для валидации JSON схемы
        :param check_response_status_code: фикстура, проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param check_response_time: фикстура проверки времени ответа
        :param idx: id поста
        :param res: ожидаемый пост
        """
        query = """query ($id: ID!){post(id: $id) {title}}"""

        response = graphqlzero.query(query, variables=vars_id(idx))
        post_data = response.json()

        check_response_status_code(response, 200)
        check_response_time(response)
        validate_json(post_data, GET_POST_SCHEMA)

        with allure.step(response_body_msg(post_data)):
            expected_post = f_get_post_title[res]
            assert post_data == expected_post, f'ФР - {post_data}, ОР - {expected_post}'

    @allure.title('Получение id, названия и тела поста по несуществующему id')
    def test_get_post_id_title_body_by_unexist_id(
            self, graphqlzero, validate_json, check_response_status_code,
            response_body_msg, check_response_time, f_get_post_id_title_body_by_unexist_id):
        """Тестовая функция для проверки получения id, названия и тела поста по несуществующему id.

        :param graphqlzero: фикстура, создающая и возвращающая экземпляр класса GraphqlClient
        :param validate_json: фикстура для валидации JSON схемы
        :param check_response_status_code: фикстура, проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param check_response_time: фикстура проверки времени ответа
        """
        query = """query {post(id: 200) {id title body}}"""

        response = graphqlzero.query(query)
        post_data = response.json()

        check_response_status_code(response, 200)
        check_response_time(response)
        validate_json(post_data, GET_POST_SCHEMA)

        with allure.step(response_body_msg(post_data)):
            assert post_data == f_get_post_id_title_body_by_unexist_id, \
                f'ОР - {f_get_post_id_title_body_by_unexist_id}, ФР - {post_data}'

    @allure.title('Получение информации об авторе поста по существующему id')
    def test_get_post_user_data(
            self, graphqlzero, validate_json, check_response_status_code,
            response_body_msg, check_response_time, f_get_post_user_data):
        """Тестовая функция для проверки получения информации об авторе поста по существующему id.

        :param graphqlzero: фикстура, создающая и возвращающая экземпляр класса GraphqlClient
        :param validate_json: фикстура для валидации JSON схемы
        :param check_response_status_code: фикстура, проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param check_response_time: фикстура проверки времени ответа
        """
        query = """query {post(id: 1){user {id name phone email username}}}"""

        response = graphqlzero.query(query)
        post_data = response.json()

        check_response_status_code(response, 200)
        check_response_time(response)
        validate_json(post_data, GET_POST_SCHEMA)

        with allure.step(response_body_msg(post_data)):
            assert post_data == f_get_post_user_data, \
                f'ОР - {f_get_post_user_data}, ФР - {post_data}'

    @allure.title('Получение ошибки при невалидном запросе автора поста по существующему id')
    def test_get_invalid_post_user(
            self, graphqlzero, validate_json, check_response_status_code,
            response_body_msg, check_response_time):
        """Тестовая функция для проверки получения ошибки при невалидном
        запросе автора поста по существующему id'.

        :param graphqlzero: фикстура, создающая и возвращающая экземпляр класса GraphqlClient
        :param validate_json: фикстура для валидации JSON схемы
        :param check_response_status_code: фикстура, проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param check_response_time: фикстура проверки времени ответа
        """
        query = """query {post(id: 1) {id user}}"""

        response = graphqlzero.query(query)
        post_data = response.json()

        check_response_status_code(response, 400)
        check_response_time(response)

        with allure.step(response_body_msg(post_data)):
            assert post_data['errors'][0]['message'] == er.invalid_query_post_user(), \
                   f'ОР - {er.invalid_query_post_user()}, ФР - {post_data}'

    @pytest.mark.parametrize('idx, res', [(1, 'post1'), (2, 'post2')])
    @allure.title('Получение комментариев поста')
    def test_get_post_comments(
            self, graphqlzero, validate_json, check_response_status_code,
            response_body_msg, check_response_time, idx, res, f_get_post_comments):
        """Тестовая функция для проверки получения информации об комментах поста по существующему id.

        :param graphqlzero: фикстура, создающая и возвращающая экземпляр класса GraphqlClient
        :param validate_json: фикстура для валидации JSON схемы
        :param check_response_status_code: фикстура, проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param check_response_time: фикстура проверки времени ответа
        :param idx: id поста
        :param res: ожидаемый результат для поста
        """
        query = """query ($id: ID!){post(id: $id){comments {data {id name body}}}}"""

        response = graphqlzero.query(query, variables=vars_id(idx))
        post_data = response.json()

        check_response_status_code(response, 200)
        check_response_time(response)
        validate_json(post_data, GET_POST_SCHEMA)

        with allure.step(response_body_msg(post_data)):
            expected_post = f_get_post_comments[res]
            assert post_data == expected_post, f'ФР - {post_data}, ОР - {expected_post}'

    @pytest.mark.parametrize('limit', [1, 3])
    @allure.title('Получение части комментариев поста')
    def test_get_post_comments_with_limit(
            self, graphqlzero, validate_json, check_response_status_code,
            response_body_msg, check_response_time, limit,
            f_get_post_comments_with_limit):
        """Тестовая функция для проверки получения нескольких комментов поста.

        :param graphqlzero: фикстура, создающая и возвращающая экземпляр класса GraphqlClient
        :param validate_json: фикстура для валидации JSON схемы
        :param check_response_status_code: фикстура, проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param check_response_time: фикстура проверки времени ответа
        :param limit: количество комментов
        """
        query = """query ($options: PageQueryOptions, $id: ID!){post(id: $id) {
        comments (options: $options){data {id name body}}}}"""

        response = graphqlzero.query(query, variables=common_dict(vars_limit(limit), vars_id(1)))
        post_data = response.json()

        check_response_status_code(response, 200)
        check_response_time(response)
        validate_json(post_data, GET_POST_SCHEMA)

        with allure.step(response_body_msg(post_data)):
            expected_post = f_get_post_comments_with_limit(limit)
            assert post_data == expected_post, f'ФР - {post_data}, ОР - {expected_post}'

    @pytest.mark.parametrize('sort_by', ['id', 'name', 'body'])
    @allure.title('Получение отсортированных по убыванию комментариев поста')
    def test_get_post_comments_with_desc_sort(
            self, graphqlzero, validate_json, check_response_status_code,
            response_body_msg, check_response_time, sort_by,
            f_get_post_comments_with_desc_sort):
        """Тестовая функция для проверки получения отсортированных по убыванию комментов
         поста.

        :param graphqlzero: фикстура, создающая и возвращающая экземпляр класса GraphqlClient
        :param validate_json: фикстура для валидации JSON схемы
        :param check_response_status_code: фикстура, проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param check_response_time: фикстура проверки времени ответа
        :param sort_by: по каким полям сортировка
        """
        query = """query ($options: PageQueryOptions, $id: ID!){post(id: $id) {
            comments (options: $options){data {id name body}}}}"""

        response = graphqlzero.query(query, variables=common_dict(vars_sort('DESC', sort_by), vars_id(1)))
        post_data = response.json()

        check_response_status_code(response, 200)
        check_response_time(response)
        validate_json(post_data, GET_POST_SCHEMA)

        with allure.step(response_body_msg(post_data)):
            expected_post = f_get_post_comments_with_desc_sort(sort_by)
            assert post_data == expected_post, f'ФР - {post_data}, ОР - {expected_post}'

    @pytest.mark.parametrize('sort_by, limit, sort_type', [('id', 2, 'DESC'), ('name', 1, 'ASC')])
    @allure.title('Получение отсортированных части комментариев поста')
    def test_get_post_comments_with_sort_and_limit(
            self, graphqlzero, validate_json, check_response_status_code,
            response_body_msg, check_response_time, sort_by,
            limit, sort_type, f_get_post_comments_with_sort_and_limit):
        """Тестовая функция для проверки получения отсортированных части комментариев поста.

        :param graphqlzero: фикстура, создающая и возвращающая экземпляр класса GraphqlClient
        :param validate_json: фикстура для валидации JSON схемы
        :param check_response_status_code: фикстура, проверки кода ответа
        :param response_body_msg: фикстура, возвращающая текст проверки тела ответа
        :param check_response_time: фикстура проверки времени ответа
        :param sort_by: по каким полям сортировка
        :param limit: количество постов
        :param sort_type: тип сортировки
        """
        query = """query ($options: PageQueryOptions){post(id: 1) {
                comments (options: $options){data {id name body}}}}"""

        response = graphqlzero.query(query, variables=common_dict(
            vars_limit(limit), vars_sort(sort_type, sort_by)))
        post_data = response.json()

        check_response_status_code(response, 200)
        check_response_time(response)
        validate_json(post_data, GET_POST_SCHEMA)

        with allure.step(response_body_msg(post_data)):
            expected_post = f_get_post_comments_with_sort_and_limit(limit, sort_by, sort_type)
            assert post_data == expected_post, f'ФР - {post_data}, ОР - {expected_post}'
