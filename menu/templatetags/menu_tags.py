# menu/templatetags/menu_tags.py
from django import template

from menu.models import Menu, MenuItem

register = template.Library()


@register.inclusion_tag('menu/draw_menu.html', takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    try:
        menu = Menu.objects.get(name=menu_name)
        menu_items = MenuItem.objects.filter(menu=menu).select_related('parent').all()
        tree = build_tree(menu_items)
        active_item = get_active_item(request.path, menu_items)
        return {'menu': tree, 'active_item': active_item, 'request': request}
    except Menu.DoesNotExist:
        return {'menu': [], 'active_item': None, 'request': request}


def build_tree(menu_items):
    tree = {}
    for item in menu_items:
        if item.parent is None:
            tree[item] = []
        else:
            if item.parent not in tree:
                tree[item.parent] = []
            tree[item.parent].append(item)
    return tree


def get_active_item(path, menu_items):
    for item in menu_items:
        if item.get_url() == path:
            return item
    return None
