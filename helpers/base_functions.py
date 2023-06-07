"""Модуль с вспомогательными функциями."""

from mergedeep import merge


def vars_id(idx, var_name='id'):
    return {var_name: idx}


def vars_limit(n, var_name='options'):
    return {var_name: {'paginate': {'limit': n}}}


def vars_sort(order, field, var_name='options'):
    return {var_name: {'sort': {'order': order, 'field': field}}}


def vars_title(title, var_name='input'):
    return {var_name: {'title': title}}


def vars_body(body, var_name='input'):
    return {var_name: {'body': body}}


def common_dict(*args):
    """Функция мержа словарей."""
    return merge(*args)


def data_for_list(**kwargs):
    return kwargs
