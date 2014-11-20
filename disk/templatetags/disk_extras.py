from django import template

register = template.Library()


def count_share(server):
    i = 0
    for partition in server.partition.all():
        i += partition.share.count()
    return i

register.filter('count_share', count_share)
