"""Генераторы словарей (ожидаемых результатов) для сверки с результатами запросов к API."""

from addict import Dict


class PostResponseBodyGenerator:
    @staticmethod
    def post_data_dict(**kwargs):
        mapping = Dict()
        mapping.data.post = kwargs
        return mapping

    @staticmethod
    def posts_data_dict(datas):
        mapping = Dict()
        mapping.data.posts.data = datas
        return mapping

    @staticmethod
    def post_user_data_dict(**kwargs):
        mapping = Dict()
        mapping.data.post.user = kwargs
        return mapping

    @staticmethod
    def post_comments_dict(total_count='', datas=None):
        mapping = Dict()
        if total_count != '':
            mapping.data.post.comments.totalCount = total_count
        if datas is not None:
            mapping.data.post.comments.data = datas
        return mapping

    @staticmethod
    def post_update_data_dict(**kwargs):
        mapping = Dict()
        mapping.data.updatePost = kwargs
        return mapping

    @staticmethod
    def post_create_data_dict(**kwargs):
        mapping = Dict()
        mapping.data.createPost = kwargs
        return mapping
