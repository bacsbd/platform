from __future__ import unicode_literals

from django.db import models
import django.utils.timezone
from modelcluster.fields import ParentalKey

from wagtail.wagtailcore.models import Page
from wagtail.wagtailsearch import index
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import (FieldPanel, InlinePanel, StreamFieldPanel)

from wagtailsurveys import models as surveys_models
from theplatform.blocks import GlobalStreamBlock


class EventIndexPage(Page):
	subpage_types = [
        'EventPage'
    ]

	parent_page_types = ['home.HomePage']
	
	def get_context(self, request):
		context = super(EventIndexPage, self).get_context(request)
		context['events'] = EventPage.objects.descendant_of(
		    self).live().order_by(
		    '-first_published_at')
		return context

	


class EventPage(Page):
	summary = models.TextField(
        help_text='An event summary which will be shown on index page',
        blank=True)
	
	description = RichTextField(blank=True)
	
	datetime_from = models.DateTimeField('Start datetime', default=django.utils.timezone.now, blank=True)
	datetime_to = models.DateTimeField('End datetime', null=True, blank = True)

	parent_page_types = [
        'EventIndexPage'
    ]
	subpage_types = [
        'EventRegistrationPage'
    ]

	content_panels = Page.content_panels + [
		FieldPanel('summary'),
		FieldPanel('description'),
		FieldPanel('datetime_from'),
		FieldPanel('datetime_to'),
	]


class EventRegistrationPage(surveys_models.AbstractSurvey):
	parent_page_types = [
		'EventPage'
	]
	intro = RichTextField(blank=True)
	thank_you_text = RichTextField(blank=True)

	def get_form_fields(self):
		return self.event_registration_form_fields.all()
	
	content_panels = surveys_models.AbstractSurvey.content_panels + [
        FieldPanel('intro', classname="full"),
        InlinePanel('event_registration_form_fields', label="Form fields"),
        FieldPanel('thank_you_text', classname="full"),
    ]

class EventRegistrationFormField(surveys_models.AbstractFormField):
	page = ParentalKey(EventRegistrationPage, related_name='event_registration_form_fields')


