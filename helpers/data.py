"""Модуль с классами с данными для проверок."""
import json


class ID:
    @staticmethod
    def get_id(num):
        return str(num)


class Post:
    """Посты."""
    POST_1 = {
        'title': 'sunt aut facere repellat provident occaecati excepturi optio reprehenderit',
        'body': 'quia et suscipit\nsuscipit recusandae consequuntur expedita et cum'
                '\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est '
                'autem sunt rem eveniet architecto'}
    POST_2 = {
        'title': 'qui est esse',
        'body': 'est rerum tempore vitae\nsequi sint nihil reprehenderit dolor beatae '
                'ea dolores neque\nfugiat blanditiis voluptate porro vel nihil molestiae ut '
                'reiciendis\nqui aperiam non debitis possimus qui neque nisi nulla'}

    POST_100 = {'title': 'at nam consequatur ea labore ea harum',
                'body': 'cupiditate quo est a modi nesciunt soluta\nipsa voluptas error '
                        'itaque dicta in\nautem qui minus magnam et distinctio eum\n'
                        'accusamus ratione error aut'}
    POST_99 = {'title': 'temporibus sit alias delectus eligendi possimus magni',
               'body': 'quo deleniti praesentium dicta non quod\naut est molestias\n'
                       'molestias et officia quis nihil\nitaque dolorem quia'}
    POST_98 = {'title': 'laboriosam dolor voluptates',
               'body': 'doloremque ex facilis sit sint culpa\nsoluta assumenda eligendi '
                       'non ut eius\nsequi ducimus vel quasi\nveritatis est dolores'}


class User:
    """Юзеры."""
    USER_1 = {'name': 'Leanne Graham', 'phone': '1-770-736-8031 x56442',
              'email': 'Sincere@april.biz', 'username': 'Bret', 'website': 'hildegard.org',
              'address': {'geo': {'lat': -37.3159, 'lng': 81.1496}}}
    USER_2 = {'name': 'Ervin Howell', 'phone': '010-692-6593 x09125',
              'email': 'Shanna@melissa.tv', 'username': 'Antonette', 'website': 'anastasia.net',
              'address': {'geo': {'lat': -43.9509, 'lng': -34.4618}}}


class CommentsMeta:
    NULL = None


class Comments:
    """Комментарии к постам."""
    COMMENT_1 = {'name': 'id labore ex et quam laborum',
                 'body': 'laudantium enim quasi est quidem magnam voluptate ipsam eos\n'
                         'tempora quo necessitatibus\ndolor quam autem quasi\nreiciendis '
                         'et nam sapiente accusantium'}
    COMMENT_2 = {'name': 'quo vero reiciendis velit similique earum',
                 'body': 'est natus enim nihil est dolore omnis voluptatem numquam\net '
                         'omnis occaecati quod ullam at\nvoluptatem error expedita pariatur\n'
                         'nihil sint nostrum voluptatem reiciendis et'}
    COMMENT_3 = {'name': 'odio adipisci rerum aut animi',
                 'body': 'quia molestiae reprehenderit quasi aspernatur\naut expedita '
                         'occaecati aliquam eveniet laudantium\nomnis quibusdam delectus saepe '
                         'quia accusamus maiores nam est\ncum et ducimus et vero voluptates '
                         'excepturi deleniti ratione'}
    COMMENT_4 = {'name': 'alias odio sit',
                 'body': 'non et atque\noccaecati deserunt quas accusantium unde odit nobis qui '
                         'voluptatem\nquia voluptas consequuntur itaque dolor\net qui '
                         'rerum deleniti ut occaecati'}
    COMMENT_5 = {'name': 'vero eaque aliquid doloribus et culpa',
                 'body': 'harum non quasi et ratione\ntempore iure ex voluptates in ratione'
                         '\nharum architecto fugit inventore cupiditate\nvoluptates magni quo et'}

    COMMENT_6 = {'name': 'et fugit eligendi deleniti quidem qui sint nihil autem',
                 'body': 'doloribus at sed quis culpa deserunt consectetur qui praesentium\n'
                         'accusamus fugiat dicta\nvoluptatem rerum ut voluptate autem\nvoluptatem '
                         'repellendus aspernatur dolorem in'}

    COMMENT_7 = {'name': 'repellat consequatur praesentium vel minus molestias voluptatum',
                 'body': 'maiores sed dolores similique labore et inventore et\nquasi temporibus esse '
                         'sunt id et\neos voluptatem aliquam\naliquid ratione corporis '
                         'molestiae mollitia quia et magnam dolor'}

    COMMENT_8 = {'name': 'et omnis dolorem',
                 'body': 'ut voluptatem corrupti velit\nad voluptatem maiores\n'
                         'et nisi velit vero accusamus maiores\nvoluptates quia aliquid ullam eaque'}

    COMMENT_9 = {'name': 'provident id voluptas',
                 'body': 'sapiente assumenda molestiae atque\nadipisci laborum distinctio '
                         'aperiam et ab ut omnis\net occaecati aspernatur odit sit rem '
                         'expedita\nquas enim ipsam minus'}

    COMMENT_10 = {'name': 'eaque et deleniti atque tenetur ut quo ut',
                  'body': 'voluptate iusto quis nobis reprehenderit ipsum amet nulla\n'
                          'quia quas dolores velit et non\naut quia necessitatibus\nnostrum '
                          'quaerat nulla et accusamus nisi facilis'}


class Errors:
    @staticmethod
    def create_post_wout_title(body):
        return f'Variable \"$input\" got invalid value {{ body: \"{body}\" }}; ' \
                   f'Field title of required type String! was not provided.'

    @staticmethod
    def create_post_invalid_title(title):
        title = json.dumps(title)
        if title == 'null':
            return f'Variable "$input" got invalid value {title} at "input.title"; ' \
                   f'Expected non-nullable type String! not to be {title}.'
        else:
            return f'Variable \"$input\" got invalid value {title} at \"input.title\"; ' \
                   f'Expected type String. String cannot represent a non string value: {title}'

    @staticmethod
    def invalid_query_post_user():
        return 'Field \"user\" of type \"User\" must have a selection of subfields. ' \
               'Did you mean \"user { ... }\"?'


class Messages:
    DELETED_POST = {'msg': {'data': {'deletePost': True}}}

