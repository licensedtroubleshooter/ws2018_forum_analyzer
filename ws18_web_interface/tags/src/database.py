import psycopg2


def count_tags():
    """
        Получаем список из тегов и количество их уникальных вхождений

    """
    connect = psycopg2.connect(database='forum_answers', user='roman',
                               host='localhost', password='admin')

    cursor = connect.cursor()
    cursor.execute(

        "SELECT tag.name, count(*) "
        "FROM tags_tag AS tag "
        "INNER JOIN texts_tag_text AS tag_text "
            "ON tag.id = tag_text.tag_id "
        "GROUP BY tag.name;"

    )

    tag_count = cursor.fetchall()
    connect.close()

    return tag_count


if __name__ == "__main__":
    pass