import sys
import re
import os
import vk

MAX_COUNT_COMMENTS = 100  # ограничение VK


def save_comments_to_csv(group: str, path='.') -> str:
    print('start load comments from group...')
    clean_pattern1 = re.compile('\'')
    clean_pattern2 = re.compile('<[^>]*>')
    clean_pattern3 = re.compile('[^A-Za-zА-ЯЁа-яё0-9 ,.?!;:)(]+')
    emoji_pattern = re.compile(
        '(\ud83d[\ude00-\ude4f])|'  # emoticons
        '(\ud83c[\udf00-\uffff])|'  # symbols & pictographs (1 of 2)
        '(\ud83d[\u0000-\uddff])|'  # symbols & pictographs (2 of 2)
        '(\ud83d[\ude80-\udeff])|'  # transport & map symbols
        '(\ud83c[\udde0-\uddff])'  # flags (iOS)
        '+', flags=re.UNICODE)
    respect_pattern = re.compile('уважаем..')

    session = vk.Session()
    vk_api = vk.API(session)

    group = re.sub('https://[^/]*/', '', group)
    raw_comments = 'likes,status,text\n'

    gid = vk_api.groups.getById(group_id=group)[0]['gid']
    topics = vk_api.board.getTopics(group_id=gid)['topics']

    for t in topics[1:]:
        cur_comment_id = 0
        while True:
            comments = vk_api.board.getComments(group_id=gid,
                                                topic_id=t['tid'],
                                                offset=cur_comment_id,
                                                count=MAX_COUNT_COMMENTS,
                                                need_likes=1)['comments']
            for c in comments[1:]:
                info = str(c['likes']['count']) + ',0,'
                text = clean_pattern3.sub(' ',
                                          clean_pattern2.sub(' ',
                                                             clean_pattern1.sub(' ',
                                                                                emoji_pattern.sub('', c['text']))))
                if text != '' and text.find(':bp') == -1 and respect_pattern.search(text.lower()) is None:
                    raw_comments += info + '"' + text + '"' + '\n'
            cur_comment_id += MAX_COUNT_COMMENTS

            if cur_comment_id > comments[0]:
                break
    raw_csv = os.path.join(path, 'raw_comments.csv')
    with open(raw_csv, 'w') as file:
        file.write(raw_comments)

    print('end load comments from group...')
    return raw_csv


def main():

    groups = ''

    if len(sys.argv) > 1:
        for p in sys.argv[1:]:
            groups += p + ' '
        # parse_groups(groups[:-1])
        save_comments_to_csv(groups[:-1])
    else:
        groups = input('Please, input link to group: ')
        if groups != '':
            # parse_groups(groups)
            print(save_comments_to_csv(groups[:-1]))
        else:
            print('Error: empty list of groups and list of arguments!')


if __name__ == '__main__':
    main()
