import psycopg2


def texts_of_tag(tag):
    """
        Получаем список текстов, в которых встречался tag

    """
    connect = psycopg2.connect(
        database='forum_answers',
        user='roman',
        host='localhost',
        password='admin'
    )

    cursor = connect.cursor()
    cursor.execute(

        "SELECT text.id "
        "FROM tags_tag AS tag "
        "INNER JOIN texts_tag_text AS tag_text "
            "ON tag.id = tag_text.tag_id "
        "INNER JOIN texts_text AS text "
            "ON text.id = tag_text.text_id "
        "WHERE tag.name = '{}'".format(tag)

    )

    texts = cursor.fetchall()
    connect.close()

    return texts


def texts_of_cluster(cluster_id):

    connect = psycopg2.connect(
        database='forum_answers',
        user='roman',
        host='localhost',
        password='admin'
    )

    cursor = connect.cursor()
    cursor.execute(

        "SELECT text.id "
        "FROM clusters_cluster AS cluster "
        "INNER JOIN texts_text AS text "
        "ON cluster.id = text.cluster_id "
        "WHERE cluster.id = '{}'".format(cluster_id)

    )

    texts = cursor.fetchall()
    connect.close()

    return texts


def get_text(text_id):

    connect = psycopg2.connect(
        database='forum_answers',
        user='roman',
        host='localhost',
        password='admin'
    )
    cursor = connect.cursor()

    cursor.execute(

        "SELECT text.plain_text "
        "FROM texts_text AS text "
        "WHERE text.id = {}".format(text_id)

    )
    url = cursor.fetchall()

    return url


def get_texts(list_id):
    """
        Итератор текстов из поступающего на вход списка идетификаторов

    """
    connect = psycopg2.connect(
        database='forum_answers',
        user='roman',
        host='localhost',
        password='admin'
    )

    cursor = connect.cursor()
    for item in list_id:
        cursor.execute(

            "SELECT text.plain_text, text.id "
            "FROM texts_text AS text "
            "WHERE text.id = {}".format(item[0])

        )
        yield cursor.fetchall()
    connect.close()


def spam_status_to_active(id_text):
    """
        Пометка о том, что текст является спамом

    """
    connect = psycopg2.connect(
        database='forum_answers',
        user='roman',
        host='localhost',
        password='admin'
    )

    cursor = connect.cursor()
    cursor.execute(
        "UPDATE texts_text "
        "SET status = 2 "
        "WHERE texts_text.id = {};".format(id_text)
    )
    connect.commit()
    connect.close()


def spam_status_to_non_active(id_text):
    """
            Убираем пометку о том, что текст является спамом

    """
    connect = psycopg2.connect(
        database='forum_answers',
        user='roman',
        host='localhost',
        password='admin'
    )

    cursor = connect.cursor()
    cursor.execute(
        "UPDATE texts_text "
        "SET status = 0 "
        "WHERE texts_text.id = {};".format(id_text)
    )
    connect.commit()
    connect.close()


def get_source_url(text_id):

    connect = psycopg2.connect(
        database='forum_answers',
        user='roman',
        host='localhost',
        password='admin'
    )
    cursor = connect.cursor()

    cursor.execute(

        "SELECT text.source_url "
        "FROM texts_text AS text "
        "WHERE text.id = {}".format(text_id)

    )
    url = cursor.fetchall()

    return url


if __name__ == "__main__":
    pass



