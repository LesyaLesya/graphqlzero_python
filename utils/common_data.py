"""Модуль с классами с данными для проверок."""

import json


class Errors:
    @staticmethod
    def create_post_wout_title(body):
        return f'Variable \"$input\" got invalid value {{ body: \"{body}\" }}; ' \
                   f'Field "title" of required type "String!" was not provided.'

    @staticmethod
    def create_post_invalid_title(title):
        title = json.dumps(title)
        if title == 'null':
            return f'Variable "$input" got invalid value {title} at "input.title"; ' \
                   f'Expected non-nullable type "String!" not to be {title}.'
        else:
            return f'Variable \"$input\" got invalid value {title} at \"input.title\"; ' \
                   f'String cannot represent a non string value: {title}'

    @staticmethod
    def invalid_query_post_user():
        return 'Field \"user\" of type \"User\" must have a selection of subfields. ' \
               'Did you mean \"user { ... }\"?'


class Messages:
    DELETED_POST = {'msg': {'data': {'deletePost': True}}}
