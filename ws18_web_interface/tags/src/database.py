import psycopg2


def count_tags():
    """
        Получаем список из тегов и количество их уникальных вхождений

    """
    connect = psycopg2.connect(
        database='forum_answers',
        user='roman',
        host='localhost',
        password='admin'
    )

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


def tags_of_text(text_id):
    """
        Получаем теги по идентификатору текста

    """
    connect = psycopg2.connect(
        database='forum_answers',
        user='roman',
        host='localhost',
        password='admin'
    )

    cursor = connect.cursor()
    cursor.execute(
        "SELECT tag.name "
        "FROM tags_tag AS tag "
        "INNER JOIN texts_tag_text AS tag_text "
            "ON tag.id = tag_text.tag_id "
        "INNER JOIN texts_text AS text "
            "ON text.id = tag_text.text_id "
        "WHERE text.id = {}".format(text_id)
    )
    tags = cursor.fetchall()

    return tags


if __name__ == "__main__":
    pass