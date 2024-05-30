"""Генераторы словарей (ожидаемых результатов) для сверки с результатами запросов к API."""

from addict import Dict


class UserResponseBodyGenerator:
    @staticmethod
    def user_data_dict(**kwargs):
        mapping = Dict()
        mapping.data.user = kwargs
        return mapping

    @staticmethod
    def address_data_dict(**kwargs):
        mapping = Dict()
        mapping.data.user.address.geo = kwargs
        return mapping

    @staticmethod
    def user_posts_data_dict(datas):
        mapping = Dict()
        mapping.data.user.posts.data = datas
        return mapping

    @staticmethod
    def users_data_dict(datas):
        mapping = Dict()
        mapping.data.users.data = datas
        return mapping
