import psycopg2
from src.database import get_connect


def count_tags(url_id):
    """
        Получаем список из тегов и количество их уникальных вхождений

    """
    connect = get_connect()

    cursor = connect.cursor()
    cursor.execute(

        "SELECT tag.name, count(*) "
        "FROM tags_tag AS tag "
        "INNER JOIN texts_tagtext AS tagtext "
            "ON tag.id = tagtext.tag_id "
        "INNER JOIN texts_text AS text "
            "ON text.id = tagtext.text_id "
        "INNER JOIN texts_url AS url "
            "ON text.url_id = url.id "
        "WHERE url.id = {} "
        "GROUP BY tag.name;".format(url_id)

    )

    tag_count = cursor.fetchall()
    connect.close()

    return tag_count


def tags_of_text(text_id):
    """
        Получаем теги по идентификатору текста

    """
    connect = get_connect()

    cursor = connect.cursor()
    cursor.execute(
        "SELECT tag.name "
        "FROM tags_tag AS tag "
        "INNER JOIN texts_tagtext AS tagtext "
            "ON tag.id = tagtext.tag_id "
        "INNER JOIN texts_text AS text "
            "ON text.id = tagtext.text_id "
        "WHERE text.id = {}".format(text_id)
    )
    tags = cursor.fetchall()
    connect.close()

    return tags


if __name__ == "__main__":
    pass