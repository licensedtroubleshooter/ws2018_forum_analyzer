import psycopg2


def get_connect():
    """
        Получаем connect к БД (для использования в скриптах с запросами)
    """

    connect = psycopg2.connect(
        database='forum_answers',
        user='roman',
        host='localhost',
        password='admin'
    )

    return connect