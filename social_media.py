# -*- coding: utf-8 -*- #
from collections import namedtuple
from datetime import datetime
from urllib.parse import urljoin

from jinja2 import Markup
from pelican import signals
from pelican.contents import Article
from pelican.utils import strftime

def init(article):
    if not isinstance(article, Article):
        return
    default_author_map = {
        'open_graph': {},
        'twitter': {},
    }
    SITEURL = article.settings.get('SITEURL', '')
    SITENAME = article.settings.get('SITENAME')
    DEFAULT_IMAGE = article.settings.get('DEFAULT_IMAGE', None)
    DEFAULT_TWITTER_CARD = article.settings.get('DEFAULT_TWITTER_CARD', 'summary')
    TWITTER_SITE = article.settings.get('TWITTER_SITE', None)
    AUTHOR_MAP = article.settings.get('AUTHOR_MAP', default_author_map)

    image_path = article.metadata.get('image', None) or DEFAULT_IMAGE
    image = urljoin(SITEURL, image_path)
    article_url = urljoin(SITEURL, article.url)
    summary = article.metadata.get('summary', None) or article.summary
    authors = [author.name for author in article.authors]
    tags = [tag.name for tag in article.tags] if hasattr(article, 'tags') else None
    og_authors = [AUTHOR_MAP['open_graph'].get(author, author) for author in authors]
    tw_author = AUTHOR_MAP['twitter'].get(authors[0], None)
    twitter_card = article.metadata.get('twitter_card', None) or DEFAULT_TWITTER_CARD

    if TWITTER_SITE and not TWITTER_SITE.startswith('@'):
        TWITTER_SITE = '@%s' % TWITTER_SITE
    if tw_author and not tw_author.startswith('@'):
        tw_author = '@%s' % tw_author

    article_meta = {
        'og': {
            'title': article.title,
            'type': 'article',
            'image': image,
            'url': article_url,
            'description': summary,
            'sitename': SITENAME,
        },
        'article': {
            'published_time': article.date,
            'modified_time': getattr(article, 'modified', None),
            'author': og_authors,
            'section': article.category.name,
            'tag': tags,
        },
        'twitter': {
            'card': twitter_card,
            'site': TWITTER_SITE,
            'creator': tw_author,
            'title': article.title,
            'description': summary,
            'image': image,
        },
    }

    article.social_media_tags = build_meta_tags(article_meta, list(), list())

def make_tag(name, content):
    if isinstance(content, datetime):
        content = strftime(content, '%Y-%m-%d')
    Tag = namedtuple('Tag', ['name', 'content'])
    content = Markup.escape(Markup.striptags(content))
    if name.startswith("twitter"):
        return '<meta name="%s" content="%s"/>' % (name, content)
    else:
        return '<meta property="%s" content="%s"/>' % (name, content)

def build_meta_tags(metadata, tags, context):
    for key, value in metadata.items():
        if not isinstance(value, dict):
            if not value:
                continue
            name = ':'.join(context + [key]) if key else ':'.join(context)
            if isinstance(value, list):
                tags.extend([make_tag(name, v) for v in value])
            else:
                tags.append(make_tag(name, value))
        else:
            context.append(key)
            build_meta_tags(value, tags, context)
            context.pop()
    return tags

def register ():
    signals.content_object_init.connect(init)
