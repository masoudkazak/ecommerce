from django import template


register = template.Library()

@register.filter
def get_value_dict(value, key):
    return value.get(key)

@register.filter
def get_index_list(value, index):
    return value[index]


@register.filter
def number_to_range_point(number):
    return [range(number), range(5-number)]


@register.filter
def get_percent_point(number):
    percent_list = ["0%", "20%", "40%", "60%", "80%", "100%"]
    return percent_list[number]