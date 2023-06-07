import pytest
from addict import Dict


@pytest.fixture
def user_data_dict():
    def __user_data_dict(**kwargs):
        mapping = Dict()
        mapping.data.user = kwargs
        return mapping
    return __user_data_dict


@pytest.fixture
def address_data_dict():
    def __address_data_dict(**kwargs):
        mapping = Dict()
        mapping.data.user.address.geo = kwargs
        return mapping
    return __address_data_dict


@pytest.fixture
def user_posts_data_dict():
    def __user_posts_data_dict(datas):
        mapping = Dict()
        mapping.data.user.posts.data = datas
        return mapping
    return __user_posts_data_dict


@pytest.fixture
def users_data_dict():
    def __users_data_dict(datas):
        mapping = Dict()
        mapping.data.users.data = datas
        return mapping
    return __users_data_dict
