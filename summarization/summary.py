from gensim.summarization import summarize


class SummarizeTextHelper(object):
    def __init__(self):
        pass

    def summarize_text_per_tag(self, tags_with_posts, plaintext_posts):
        tags_with_post_summary = dict()
        for tag in tags_with_posts.keys():
            tags_with_post_summary[tag] = {'posts': tags_with_posts[tag],
                                           'summary': summarize('. '.join(plaintext_posts[tags_with_posts[tag]]))}
        return tags_with_post_summary
