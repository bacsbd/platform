from __future__ import unicode_literals

from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.wagtailcore.models import Page
from wagtail.wagtailsearch import index
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel

from wagtailsurveys import models as surveys_models


class EventIndexPage(Page):
	subpage_types = [
        'EventPage'
    ]

class EventPage(Page):
	parent_page_types = [
        'EventIndexPage'
    ]
	subpage_types = [
        'EventRegistrationPage'
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


