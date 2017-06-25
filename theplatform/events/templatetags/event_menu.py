from itertools import chain

from django import template
from wagtail.wagtailcore.models import Page
from theplatform.events.models import EventPage


register = template.Library()

@register.assignment_tag(takes_context=True)
def get_event_root(context, current_page):
    return Page.objects.type(EventPage).ancestor_of(current_page, inclusive=True).first()

@register.inclusion_tag('tags/secondary_menu.html', takes_context=True)
def get_event_menu(context, event_root, calling_page=None):
	menuitems = event_root.get_children().live()

	event_root.active = True	
	for menuitem in menuitems:
		menuitem.active = (calling_page.url.startswith(menuitem.url) if calling_page else False)
		if menuitem.active:
			event_root.active = False
	
	return {
		'calling_page' : calling_page,
		'event_root': event_root,
		'secondary_menuitems': menuitems,
		'request': context['request'],
	}