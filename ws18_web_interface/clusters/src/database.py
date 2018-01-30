import psycopg2


def count_clusters():
    """
        Подсчет количества текстов в каждом кластере
        Возвращает описание кластера и количество текство в нем

    """
    connect = psycopg2.connect(
        database='forum_answers',
        user='roman',
        host='localhost',
        password='admin'
    )

    cursor = connect.cursor()
    cursor.execute(
        "SELECT cluster.id, cluster.name, count(*) "
        "FROM clusters_cluster AS cluster "
        "INNER JOIN texts_text AS text "
            "ON cluster.id = text.cluster_id "
        "GROUP BY cluster.name, cluster.id;"
    )

    clusters = cursor.fetchall()
    connect.close()

    return clusters


def cluster_of_text(text_id):
    """
        Получаем кластер по идентификатору текста

    """
    connect = psycopg2.connect(
        database='forum_answers',
        user='roman',
        host='localhost',
        password='admin'
    )

    cursor = connect.cursor()
    cursor.execute(
        "SELECT cluster.id, cluster.name "
        "FROM clusters_cluster AS cluster "
        "INNER JOIN texts_text AS text "
        "ON text.cluster_id = cluster.id "
        "WHERE text.id = {}".format(text_id)
    )
    cluster = cursor.fetchall()

    return cluster


if __name__ == '__main__':
    pass