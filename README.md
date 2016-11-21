# pelican-social-media
A pelican plugin to add social media tags into article.

## Usage
Add this plugin in `pelicanconf.py`.
```python
PLUGINS = ["pelican-social-media"]
```

Insert this code inside of `<head></head>` of your `article.html` template:
```
{% for tag in article.social_media_tags %}
  {{ tag }}
{% endfor %}
```

## Plugin settings
You can set these global settings in `pelicanconf.py` for this plugin. All theses settings are optional.

1.  `DEFAULT_IMAGE`

    If this is set, `og:image` and `twitter.image` will be the given value when the image is not specified in the article metadata. The value should be relative path of the image from `SITEURL`.
2.  `DEFAULT_TWITTER_CARD`

    The value can be either `summary` or `summary_large_image`, and the default value is `summary` if not specified. See [twitter card documentation](https://dev.twitter.com/cards/types) for the detail.
3.  `TWITTER_SITE`

    If this is set, `twitter:site` will be set by the given value. See [twitter documentation](https://dev.twitter.com/cards/markup) for the detail.
4.  `AUTHOR_MAP`

    ```python
    AUTHOR_MAP = {
        "<author in pelican>": {
            "twitter": "<twitter username of the author>",
            ["open_graph": "<username of the author>",]
        },
    }
    ```
    To set `twitter:creator`, you have to set twitter username. Though `article:author` is set automatically without this setting, you can override it with the optional setting `open_graph`.

## Article settings
You can set article metadata with these keys for this plugin.

1.  `image`

    The value should be relative path of the image from `SITEURL`.
2.  `summary`

    Summary is automatically generated, but you can override by this article metadata.
3.  `twitter_card`

    This is article-specific setting of `DEFAULT_TWITTER_CARD`. The value can be either `summary` or `summary_large_image`, and the default value is `summary` if not specified. See [twitter card documentation](https://dev.twitter.com/cards/types) for the detail.
