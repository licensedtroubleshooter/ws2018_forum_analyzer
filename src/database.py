# coding=utf-8
import os
import re
import shutil

import pandas as pd
import psycopg2
import vk

import core.preprocessor as preprocessor

IS_BUSY = False


def get_connect():
    """
        Получаем connect к БД (для использования в скриптах с запросами)
    """

    connect = psycopg2.connect(
        database='ForumAnalyzer',
        user='postgres',
        host='localhost',
        password='123'
    )

    return connect


def context_manager_psycopg(request):
    """
        Forget Django ORM and managers contexts(

    :param request: request to DATABASE
    :return: response from DB
    """

    connect = get_connect()
    cursor = connect.cursor()

    cursor.execute(request)

    response = cursor.fetchall()
    connect.close()

    return response


def add_group_to_postgres(url=''):
    global IS_BUSY
    if IS_BUSY:
        print('server is busy')
    else:
        # return False
        if url != '':
            IS_BUSY = True
            path = os.path.join(os.path.dirname(__file__),
                                '..',
                                'forum_analyzer',
                                'preprocessor',
                                'resources')
            if preprocessor.preprocessed_group(url):
                url_id = add_url_to_postgres(url, path)

                save_data_to_postgres(url_id, clusters_csv=os.path.join(path, 'clusters.csv'),
                                      tags_csv=os.path.join(path, 'tags.csv'),
                                      cleaned_comments_csv=os.path.join(path, 'neg_pos_comments31.csv'),
                                      tag_comments_csv=os.path.join(path, 'tags_comments.csv'),
                                      comments_clusters_csv=os.path.join(path, 'comments.csv'))
                IS_BUSY = False
                return url_id
            else:
                IS_BUSY = False
                print('Error preprocessing of link!')
        else:
            print('URL is empty!')


def add_url_to_postgres(url='', path='.'):
    session = vk.Session()
    vk_api = vk.API(session)

    name_group = vk_api.groups.getById(group_ids=re.sub('https://[^/]*/', '', url))[0]['name'].replace(' ', '')

    connect = get_connect()
    cursor = connect.cursor()

    cursor.execute(
        'INSERT INTO texts_url (url, name_url) '
        'VALUES (\'{0}\', \'{1}\') RETURNING id;'.format(url, name_group))
    url_id = cursor.fetchone()[0]

    rename = os.path.join(path, '..', '..', '..', 'static', 'img', str(url_id) + '_url.png')
    shutil.copy(os.path.join(path, 'images', 'corpus.png'), rename)
    # reopen = open(rename, 'rb')
    # django_file = File(reopen)

    cursor.execute(
        'UPDATE texts_url SET image = \'{0}\' WHERE id = {1};'.format(str(url_id) + '_url.png', url_id)
    )

    connect.commit()
    connect.close()
    return url_id


def save_data_to_postgres(url_id, clusters_csv='clusters.csv', tags_csv='tags.csv',
                          cleaned_comments_csv='neg_pos_comments31.csv', tag_comments_csv='tags_comments.csv',
                          comments_clusters_csv='comments.csv'):
    connect = get_connect()
    cursor = connect.cursor()
    clusters = pd.read_csv(clusters_csv)
    tags = pd.read_csv(tags_csv)
    cleaned_comments = pd.read_csv(cleaned_comments_csv)
    tag_comments = pd.read_csv(tag_comments_csv)
    comments_clusters = pd.read_csv(comments_clusters_csv)

    clusters_ids = {}
    for i in range(len(clusters.cluster_id)):
        cursor.execute(
            'INSERT INTO clusters_cluster (summary) '
            'VALUES (\'{}\') RETURNING id;'.format(clusters.summary[i])
        )
        id = cursor.fetchone()[0]
        clusters_ids[clusters.cluster_id[i]] = id
        # rename = os.path.join(os.path.dirname(__file__), '..', 'forum_analyzer', 'preprocessor', 'resources',
        #                          'images', str(i) + '.png')
        rename = os.path.join(os.path.dirname(__file__), '..', 'static', 'img', str(id) + '_cluster.png')
        shutil.copy(os.path.join(os.path.dirname(__file__), '..', 'forum_analyzer', 'preprocessor', 'resources',
                                 'images', str(i) + '.png'), rename)
        # reopen = open(, 'rb')
        # django_file = File(reopen)
        cursor.execute(
            'UPDATE clusters_cluster SET image = \'{0}\' WHERE id = {1};'.format(str(id) + '_cluster.png', id)
        )
    connect.commit()
    tags_ids = {}
    for i in range(len(tags.name)):
        cursor.execute(
            'INSERT INTO tags_tag (name) '
            'VALUES (\'{}\') RETURNING id;'.format(tags.name[i])
        )
        id = cursor.fetchone()[0]
        tags_ids[tags.tag_id[i]] = id
    connect.commit()
    comments_ids = {}
    for i in range(len(cleaned_comments.text)):
        cursor.execute(
            'INSERT INTO texts_text (plain_text, status, tonality, cluster_id, url_id) '
            'VALUES (\'{0}\', {1}, {2}, {3}, {4}) RETURNING id;'.format(cleaned_comments.text[i],
                                                                        cleaned_comments.status[i],
                                                                        cleaned_comments.sentiment[i],
                                                                        clusters_ids[comments_clusters.cluster_id[i]],
                                                                        url_id)
        )
        id = cursor.fetchone()[0]
        comments_ids[i] = id
    connect.commit()

    for i in range(len(tag_comments.tag_id)):
        cursor.execute(
            'INSERT INTO texts_tagtext (tag_id, text_id) '
            'VALUES ({0}, {1});'.format(tags_ids[tag_comments.tag_id[i]],
                                        comments_ids[tag_comments.comment_id[i]])
        )
    connect.commit()

    connect.close()


if __name__ == '__main__':
    path = os.path.join(os.path.dirname(__file__),
                        '..',
                        'forum_analyzer',
                        'preprocessor',
                        'resources')
    add_url_to_postgres('TESTSTS', path)