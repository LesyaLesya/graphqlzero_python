import pytest
from addict import Dict


@pytest.fixture
def post_data_dict():
    def __post_data_dict(**kwargs):
        mapping = Dict()
        mapping.data.post = kwargs
        return mapping
    return __post_data_dict


@pytest.fixture
def posts_data_dict():
    def __posts_data_dict(datas):
        mapping = Dict()
        mapping.data.posts.data = datas
        return mapping
    return __posts_data_dict


@pytest.fixture
def post_user_data_dict():
    def __post_user_data_dict(**kwargs):
        mapping = Dict()
        mapping.data.post.user = kwargs
        return mapping
    return __post_user_data_dict


@pytest.fixture
def post_comments_dict():
    def __post_comments_dict(total_count='', datas=None):
        mapping = Dict()
        if total_count != '':
            mapping.data.post.comments.totalCount = total_count
        if datas is not None:
            mapping.data.post.comments.data = datas
        return mapping
    return __post_comments_dict


@pytest.fixture
def post_update_data_dict():
    def __post_update_data_dict(**kwargs):
        mapping = Dict()
        mapping.data.updatePost = kwargs
        return mapping
    return __post_update_data_dict


@pytest.fixture
def post_create_data_dict():
    def __post_create_data_dict(**kwargs):
        mapping = Dict()
        mapping.data.createPost = kwargs
        return mapping
    return __post_create_data_dict
