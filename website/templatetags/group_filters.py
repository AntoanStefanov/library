from tokenize import group
from django import template

register = template.Library()

# https://stackoverflow.com/questions/34571880/how-to-check-in-template-if-user-belongs-to-a-group
@register.filter()
def has_group(user, group_names):
    """
        Check if user has atleast one of the given group names.
    """
    group_names = group_names.split(', ')
    return user.groups.filter(name__in=group_names).exists()
