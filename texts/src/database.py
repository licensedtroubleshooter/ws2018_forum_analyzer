import psycopg2
from src.database import get_connect


def texts_of_tag(tag, url_id):
    """
        Получаем список текстов, в которых встречался tag

    """
    connect = get_connect()

    cursor = connect.cursor()
    cursor.execute(

        "SELECT text.id "
        "FROM tags_tag AS tag "
        "INNER JOIN texts_tagtext AS tagtext "
            "ON tag.id = tagtext.tag_id "
        "INNER JOIN texts_text AS text "
            "ON text.id = tagtext.text_id "
        "INNER JOIN texts_url AS url "
            "ON text.url_id = url.id "
        "WHERE tag.name = '{}'  AND url.id = {} "
        "ORDER BY text.id;".format(tag, url_id)
    )

    texts = cursor.fetchall()
    connect.close()

    return texts


def texts_of_cluster(cluster_id, url_id):

    connect = get_connect()

    cursor = connect.cursor()
    cursor.execute(

        "SELECT text.id "
        "FROM clusters_cluster AS cluster "
        "INNER JOIN texts_text AS text "
            "ON cluster.id = text.cluster_id "
        "INNER JOIN texts_url AS url "
            "ON text.url_id = url.id "
        "WHERE cluster.id = {} AND url.id = {} "
        "ORDER BY text.id".format(cluster_id, url_id)

    )

    texts = cursor.fetchall()
    connect.close()

    return texts


def get_text(text_id):

    connect = get_connect()

    cursor = connect.cursor()

    cursor.execute(

        "SELECT text.plain_text "
        "FROM texts_text AS text "
        "WHERE text.id = {}".format(text_id)

    )
    text = cursor.fetchall()
    connect.close()

    return text


def get_texts(list_id):
    """
        Итератор текстов из поступающего на вход списка идетификаторов

    """
    connect = get_connect()

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
    connect = get_connect()

    cursor = connect.cursor()
    cursor.execute(
        "UPDATE texts_text "
        "SET status = 2 "
        "WHERE texts_text.id = {};".format(id_text)
    )
    print("Yes")
    connect.commit()
    connect.close()


def spam_status_to_non_active(id_text):
    """
            Убираем пометку о том, что текст является спамом

    """
    connect = get_connect()

    cursor = connect.cursor()
    cursor.execute(
        "UPDATE texts_text "
        "SET status = 0 "
        "WHERE texts_text.id = {};".format(id_text)
    )

    connect.commit()
    connect.close()


def get_url(text_id):

    connect = get_connect()
    cursor = connect.cursor()

    cursor.execute(

        "SELECT url.url "
        "FROM texts_text AS text "
        "INNER JOIN texts_url AS url "
        "ON text.url_id = url.id "
        "WHERE text.id = {}".format(text_id)

    )
    url = cursor.fetchall()
    connect.close()

    return url


def get_cluster_summary(cluster_id):
    connect = get_connect()
    cursor = connect.cursor()

    cursor.execute(

        "SELECT cluster.summary "
        "FROM clusters_cluster AS cluster "
        "WHERE cluster.id = {}".format(cluster_id)

    )
    summary = cursor.fetchall()
    connect.close()

    return summary


def get_all_url():
    """
        Iterator of all URLs from DB
    :return:
    """
    connect = get_connect()

    cursor = connect.cursor()
    cursor.execute(

        "SELECT url.id, url.url "
        "FROM texts_url AS url;"
    )
    urls = iter(cursor.fetchall())
    connect.close()
    for url in urls:
        yield url


def get_url_id(url):

    connect = get_connect()

    cursor = connect.cursor()
    cursor.execute(

        "SELECT url.id "
        "FROM texts_url AS url "
        "WHERE url.url = '{}';".format(url)
    )

    return cursor.fetchall()[0][0] #id of URL


def get_url_with_id(url_id):
    connect = get_connect()
    cursor = connect.cursor()

    cursor.execute(

        "SELECT url.url "
        "FROM texts_url AS url "
        "WHERE url.id = {}".format(url_id)

    )
    url = cursor.fetchall()
    connect.close()

    return url


if __name__ == "__main__":
    pass



