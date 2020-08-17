from django import template

from apps.adv_board.models import Advertisement

register = template.Library()

@register.inclusion_tag(
    'components/header.html', takes_context=True
)
def adv_list(context):
    context['adv_list'] = Advertisement.objects.all()
    return context

# @register.inclusion_tag('adv/adv_list.html', takes_context=True)
# def adv_list(context):
#     context['adv_list'] = Advertisement.objects.all()
#     return context