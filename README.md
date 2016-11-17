# pelican-social-media
A plugin to add social media tags into article

## Usage

To show Open Graph and Twitter Card, insert this code inside of `<head></head>` of your `article.html` template:
```
{% for tag in article.social_media_tags %}
  {{ tag }}
{% endfor %}
```

## On Construction

I'm working on this README.

maybe.
