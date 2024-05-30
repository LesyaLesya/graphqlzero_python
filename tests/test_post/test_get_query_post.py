"""Модуль с тестами query запросов для Post."""


import allure
import pytest

from config.base_test import BaseTest
from utils.helpers import Helper as h


@pytest.mark.query_post
@allure.feature('Post')
@allure.story('Query')
class TestQueryPost(BaseTest):
    """Тесты для query post."""

    @pytest.fixture
    def f_get_post_id_title_body(self):
        """Фикстура для теста test_get_post_id_title_body"""
        expected_post_1 = self.post_generator.post_data_dict(
            id='1', title=self.post_data.POST_1['title'], body=self.post_data.POST_1['body'])
        expected_post_2 = self.post_generator.post_data_dict(
            id='2', title=self.post_data.POST_2['title'], body=self.post_data.POST_2['body'])
        return {'post1': expected_post_1, 'post2': expected_post_2}

    @pytest.fixture
    def f_get_post_title(self):
        """Фикстура для теста test_get_post_title"""
        expected_post_1 = self.post_generator.post_data_dict(title=self.post_data.POST_1['title'])
        expected_post_2 = self.post_generator.post_data_dict(title=self.post_data.POST_2['title'])
        return {'post1': expected_post_1, 'post2': expected_post_2}

    @pytest.fixture
    def f_get_post_id_title_body_by_unexist_id(self):
        """Фикстура для теста test_get_post_id_title_body_by_unexist_id"""
        return self.post_generator.post_data_dict(id=None, title=None, body=None)

    @pytest.fixture
    def f_get_post_user_data(self):
        """Фикстура для теста test_get_post_user_data"""
        return self.post_generator.post_user_data_dict(
            id='1', name=self.user_data.USER_1['name'], phone=self.user_data.USER_1['phone'],
            email=self.user_data.USER_1['email'], username=self.user_data.USER_1['username'])

    @pytest.fixture
    def f_comments_for_post_1(self):
        """Фикстура для теста test_get_post_comments"""
        comment_1 = h.data_for_list(
            id='1', name=self.comments_data.COMMENT_1['name'], body=self.comments_data.COMMENT_1['body'])
        comment_2 = h.data_for_list(
            id='2', name=self.comments_data.COMMENT_2['name'], body=self.comments_data.COMMENT_2['body'])
        comment_3 = h.data_for_list(
            id='3', name=self.comments_data.COMMENT_3['name'], body=self.comments_data.COMMENT_3['body'])
        comment_4 = h.data_for_list(
            id='4', name=self.comments_data.COMMENT_4['name'], body=self.comments_data.COMMENT_4['body'])
        comment_5 = h.data_for_list(
            id='5', name=self.comments_data.COMMENT_5['name'], body=self.comments_data.COMMENT_5['body'])
        return [comment_1, comment_2, comment_3, comment_4, comment_5]

    @pytest.fixture
    def f_comments_for_post_2(self):
        """Фикстура для теста test_get_post_comments"""
        comment_6 = h.data_for_list(
            id='6', name=self.comments_data.COMMENT_6['name'], body=self.comments_data.COMMENT_6['body'])
        comment_7 = h.data_for_list(
            id='7', name=self.comments_data.COMMENT_7['name'], body=self.comments_data.COMMENT_7['body'])
        comment_8 = h.data_for_list(
            id='8', name=self.comments_data.COMMENT_8['name'], body=self.comments_data.COMMENT_8['body'])
        comment_9 = h.data_for_list(
            id='9', name=self.comments_data.COMMENT_9['name'], body=self.comments_data.COMMENT_9['body'])
        comment_10 = h.data_for_list(
            id='10', name=self.comments_data.COMMENT_10['name'], body=self.comments_data.COMMENT_10['body'])
        return [comment_6, comment_7, comment_8, comment_9, comment_10]

    @pytest.fixture
    def f_get_post_comments(self, f_comments_for_post_1, f_comments_for_post_2):
        """Фикстура для теста test_get_post_comments"""
        comments_for_post_1 = f_comments_for_post_1
        comments_for_post_2 = f_comments_for_post_2
        res_1 = self.post_generator.post_comments_dict(datas=comments_for_post_1)
        res_2 = self.post_generator.post_comments_dict(datas=comments_for_post_2)
        return {'post1': res_1, 'post2': res_2}

    @pytest.fixture
    def f_get_post_comments_with_limit(self, f_comments_for_post_1):
        """Фикстура для теста test_get_post_comments_with_limit"""

        def __limit_comments(n):
            comments = f_comments_for_post_1
            return self.post_generator.post_comments_dict(datas=comments[:n])

        return __limit_comments

    @pytest.fixture
    def f_get_post_comments_with_desc_sort(self, f_comments_for_post_1):
        """Фикстура для теста test_get_post_comments_with_desc_sort"""

        def __sort_comments(key):
            comments = f_comments_for_post_1
            sorted_comments = sorted(comments, key=lambda x: x[key], reverse=True)
            return self.post_generator.post_comments_dict(datas=sorted_comments)

        return __sort_comments

    @pytest.fixture
    def f_get_post_comments_with_sort_and_limit(self, f_comments_for_post_1):
        """Фикстура для теста test_get_post_comments_with_sort_and_limit"""

        def __sort_limit_comments(n, key, reverse):
            comments = f_comments_for_post_1
            if reverse == 'DESC':
                rev = True
            else:
                rev = False
            sorted_comments = sorted(comments, key=lambda x: x[key], reverse=rev)[:n]
            return self.post_generator.post_comments_dict(datas=sorted_comments)

        return __sort_limit_comments

    @pytest.mark.parametrize('idx, res', [(1, 'post1'), (2, 'post2')])
    @allure.title('Получение id, названия и тела поста по существующему id')
    def test_get_post_id_title_body(
            self, graphqlzero, idx, res, f_get_post_id_title_body, check):
        """Тестовая функция для проверки получения id, названия и тела поста по существующему id.

        :param graphqlzero: фикстура, создающая и возвращающая экземпляр класса GraphqlClient
        :param idx: id поста
        :param res: ожидаемый пост
        """
        query = """query ($id: ID!){post(id: $id){id title body}}"""

        response = graphqlzero.query(query, variables=self.query_vars.vars_id(idx))
        post_data = response.json()

        check.check_response_status_code(response, 200)
        check.check_response_time(response)
        check.validate_json(post_data, self.get_post_schema)

        with allure.step(check.response_body_msg(post_data)):
            expected_post = f_get_post_id_title_body[res]
            assert post_data == expected_post, f'ФР - {post_data}, ОР - {expected_post}'

    @pytest.mark.parametrize('idx, res', [(1, 'post1'), (2, 'post2')])
    @allure.title('Получение названия поста по существующему id')
    def test_get_post_title(
            self, graphqlzero, idx, res, f_get_post_title, check):
        """Тестовая функция для проверки получения названия поста по существующему id.

        :param graphqlzero: фикстура, создающая и возвращающая экземпляр класса GraphqlClient
        :param idx: id поста
        :param res: ожидаемый пост
        """
        query = """query ($id: ID!){post(id: $id) {title}}"""

        response = graphqlzero.query(query, variables=self.query_vars.vars_id(idx))
        post_data = response.json()

        check.check_response_status_code(response, 200)
        check.check_response_time(response)
        check.validate_json(post_data, self.get_post_schema)

        with allure.step(check.response_body_msg(post_data)):
            expected_post = f_get_post_title[res]
            assert post_data == expected_post, f'ФР - {post_data}, ОР - {expected_post}'

    @allure.title('Получение id, названия и тела поста по несуществующему id')
    def test_get_post_id_title_body_by_unexist_id(
            self, graphqlzero, f_get_post_id_title_body_by_unexist_id, check):
        """Тестовая функция для проверки получения id, названия и тела поста по несуществующему id.

        :param graphqlzero: фикстура, создающая и возвращающая экземпляр класса GraphqlClient
        """
        query = """query {post(id: 200) {id title body}}"""

        response = graphqlzero.query(query)
        post_data = response.json()

        check.check_response_status_code(response, 200)
        check.check_response_time(response)
        check.validate_json(post_data, self.get_post_schema)

        with allure.step(check.response_body_msg(post_data)):
            assert post_data == f_get_post_id_title_body_by_unexist_id, \
                f'ОР - {f_get_post_id_title_body_by_unexist_id}, ФР - {post_data}'

    @allure.title('Получение информации об авторе поста по существующему id')
    def test_get_post_user_data(
            self, graphqlzero, f_get_post_user_data, check):
        """Тестовая функция для проверки получения информации об авторе поста по существующему id.

        :param graphqlzero: фикстура, создающая и возвращающая экземпляр класса GraphqlClient
        """
        query = """query {post(id: 1){user {id name phone email username}}}"""

        response = graphqlzero.query(query)
        post_data = response.json()

        check.check_response_status_code(response, 200)
        check.check_response_time(response)
        check.validate_json(post_data, self.get_post_schema)

        with allure.step(check.response_body_msg(post_data)):
            assert post_data == f_get_post_user_data, \
                f'ОР - {f_get_post_user_data}, ФР - {post_data}'

    @allure.title('Получение ошибки при невалидном запросе автора поста по существующему id')
    def test_get_invalid_post_user(self, graphqlzero, check):
        """Тестовая функция для проверки получения ошибки при невалидном
        запросе автора поста по существующему id'.

        :param graphqlzero: фикстура, создающая и возвращающая экземпляр класса GraphqlClient
        """
        query = """query {post(id: 1) {id user}}"""

        response = graphqlzero.query(query)
        post_data = response.json()

        check.check_response_status_code(response, 400)
        check.check_response_time(response)

        with allure.step(check.response_body_msg(post_data)):
            assert post_data['errors'][0]['message'] == self.errors.invalid_query_post_user(), \
                   f'ОР - {self.errors.invalid_query_post_user()}, ФР - {post_data}'

    @pytest.mark.parametrize('idx, res', [(1, 'post1'), (2, 'post2')])
    @allure.title('Получение комментариев поста')
    def test_get_post_comments(
            self, graphqlzero, idx, res, f_get_post_comments, check):
        """Тестовая функция для проверки получения информации об комментах поста по существующему id.

        :param graphqlzero: фикстура, создающая и возвращающая экземпляр класса GraphqlClient
        :param idx: id поста
        :param res: ожидаемый результат для поста
        """
        query = """query ($id: ID!){post(id: $id){comments {data {id name body}}}}"""

        response = graphqlzero.query(query, variables=self.query_vars.vars_id(idx))
        post_data = response.json()

        check.check_response_status_code(response, 200)
        check.check_response_time(response)
        check.validate_json(post_data, self.get_post_schema)

        with allure.step(check.response_body_msg(post_data)):
            expected_post = f_get_post_comments[res]
            assert post_data == expected_post, f'ФР - {post_data}, ОР - {expected_post}'

    @pytest.mark.parametrize('limit', [1, 3])
    @allure.title('Получение части комментариев поста')
    def test_get_post_comments_with_limit(
            self, graphqlzero, limit, f_get_post_comments_with_limit, check):
        """Тестовая функция для проверки получения нескольких комментов поста.

        :param graphqlzero: фикстура, создающая и возвращающая экземпляр класса GraphqlClient
        :param limit: количество комментов
        """
        query = """query ($options: PageQueryOptions, $id: ID!){post(id: $id) {
        comments (options: $options){data {id name body}}}}"""

        response = graphqlzero.query(query, variables=h.common_dict(
            self.query_vars.vars_limit(limit), self.query_vars.vars_id(1)))
        post_data = response.json()

        check.check_response_status_code(response, 200)
        check.check_response_time(response)
        check.validate_json(post_data, self.get_post_schema)

        with allure.step(check.response_body_msg(post_data)):
            expected_post = f_get_post_comments_with_limit(limit)
            assert post_data == expected_post, f'ФР - {post_data}, ОР - {expected_post}'

    @pytest.mark.parametrize('sort_by', ['id', 'name', 'body'])
    @allure.title('Получение отсортированных по убыванию комментариев поста')
    def test_get_post_comments_with_desc_sort(
            self, graphqlzero, sort_by, f_get_post_comments_with_desc_sort, check):
        """Тестовая функция для проверки получения отсортированных по убыванию комментов
         поста.

        :param graphqlzero: фикстура, создающая и возвращающая экземпляр класса GraphqlClient
        :param sort_by: по каким полям сортировка
        """
        query = """query ($options: PageQueryOptions, $id: ID!){post(id: $id) {
            comments (options: $options){data {id name body}}}}"""

        response = graphqlzero.query(query, variables=h.common_dict(
            self.query_vars.vars_sort('DESC', sort_by), self.query_vars.vars_id(1)))
        post_data = response.json()

        check.check_response_status_code(response, 200)
        check.check_response_time(response)
        check.validate_json(post_data, self.get_post_schema)

        with allure.step(check.response_body_msg(post_data)):
            expected_post = f_get_post_comments_with_desc_sort(sort_by)
            assert post_data == expected_post, f'ФР - {post_data}, ОР - {expected_post}'

    @pytest.mark.parametrize('sort_by, limit, sort_type', [('id', 2, 'DESC'), ('name', 1, 'ASC')])
    @allure.title('Получение отсортированных части комментариев поста')
    def test_get_post_comments_with_sort_and_limit(
            self, graphqlzero, sort_by, limit, sort_type, f_get_post_comments_with_sort_and_limit, check):
        """Тестовая функция для проверки получения отсортированных части комментариев поста.

        :param graphqlzero: фикстура, создающая и возвращающая экземпляр класса GraphqlClient
        :param sort_by: по каким полям сортировка
        :param limit: количество постов
        :param sort_type: тип сортировки
        """
        query = """query ($options: PageQueryOptions){post(id: 1) {
                comments (options: $options){data {id name body}}}}"""

        response = graphqlzero.query(query, variables=h.common_dict(
            self.query_vars.vars_limit(limit), self.query_vars.vars_sort(sort_type, sort_by)))
        post_data = response.json()

        check.check_response_status_code(response, 200)
        check.check_response_time(response)
        check.validate_json(post_data, self.get_post_schema)

        with allure.step(check.response_body_msg(post_data)):
            expected_post = f_get_post_comments_with_sort_and_limit(limit, sort_by, sort_type)
            assert post_data == expected_post, f'ФР - {post_data}, ОР - {expected_post}'
