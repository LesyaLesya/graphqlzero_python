class QueryVariables:

    @staticmethod
    def vars_id(idx, var_name='id'):
        return {var_name: idx}

    @staticmethod
    def vars_limit(n, var_name='options'):
        return {var_name: {'paginate': {'limit': n}}}

    @staticmethod
    def vars_sort(order, field, var_name='options'):
        return {var_name: {'sort': {'order': order, 'field': field}}}

    @staticmethod
    def vars_title(title, var_name='input'):
        return {var_name: {'title': title}}

    @staticmethod
    def vars_body(body, var_name='input'):
        return {var_name: {'body': body}}
