import psycopg2


def count_clusters():
    """
        Подсчет количества текстов в каждом кластере

    """
    connect = psycopg2.connect(database='forum_answers', user='roman',
                               host='localhost', password='admin')

    cursor = connect.cursor()
    cursor.execute(
        "SELECT cluster.id, cluster.name, count(*) "
        "FROM clusters_cluster AS cluster "
        "INNER JOIN texts_text AS text "
            "ON cluster.id = text.cluster_id "
        "GROUP BY cluster.name, cluster.id;"
    )

    clusters = cursor.fetchall()

    return clusters