from django import template

from ..models import Tag

register = template.Library()


def tags(quote_tags):

    tags = []
    for tag_ in quote_tags.iterator():
        tag = Tag.objects.filter(name=tag_).first()
        tags.append(tag)

    # return ', '.join([str(name) for name in quote_tags.all()])
    return tags

register.filter('tags', tags)
