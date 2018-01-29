import psycopg2


def texts_of_tag(tag):
    """
        Получаем список текстов, в которых встречался tag

    """
    connect = psycopg2.connect(database='forum_answers', user='roman',
                               host='localhost', password='admin')

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

    return texts


def texts_of_cluster(cluster_id):


    connect = psycopg2.connect(database='forum_answers', user='roman',
                               host='localhost', password='admin')

    cursor = connect.cursor()
    cursor.execute(

        "SELECT text.id "
        "FROM clusters_cluster AS cluster "
        "INNER JOIN texts_text AS text "
        "ON cluster.id = text.cluster_id "
        "WHERE cluster.id = '{}'".format(cluster_id)

    )

    texts = cursor.fetchall()

    return texts


def get_texts(id_list):
    """
        Итератор текстов из поступающего на вход списка идетификаторов

    """
    connect = psycopg2.connect(database='forum_answers', user='roman',
                               host='localhost', password='admin')

    cursor = connect.cursor()
    for item in id_list:
        cursor.execute(

            "SELECT text.plain_text "
            "FROM texts_text AS text "
            "WHERE text.id = {}".format(item[0])

        )
        yield cursor.fetchall()


if __name__ == "__main__":
    pass