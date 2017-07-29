from __future__ import unicode_literals

import json

from django.conf import settings
from django.db import models
import django.utils.timezone
from django.core.serializers.json import DjangoJSONEncoder
from modelcluster.fields import ParentalKey
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

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

	def get_data_fields(self):
		data_fields = [
			('username', 'Username'),
			('fullname', 'FullName'),
			('email', 'Email'),
			('institution', 'Institution'),
			('tshirt_size', 'Tshirt Size')
		]
		data_fields += super(EventRegistrationPage, self).get_data_fields()
		return data_fields

	def get_submission_class(self):
		return CustomEventSubmission
	
	def process_form_submission(self, form):
		submission, created = self.get_submission_class().objects.get_or_create(
			page=self, user=form.user
		)
		submission.form_data=json.dumps(form.cleaned_data, cls=DjangoJSONEncoder)
		submission.save()
	
	def serve(self, request, *args, **kwargs):
		if request.method == 'POST':
			form = self.get_form(request.POST, page=self, user=request.user)

			if form.is_valid():
				self.process_form_submission(form)

				# render the landing_page
				return render(
					request,
					self.landing_page_template,
					self.get_context(request)
				)
		else:
			form = self.get_form(page=self, user=request.user)
			if request.user.is_authenticated:
				try:
					submission = self.get_submission_class().objects.get(
						page=self, user=form.user
					)
				except ObjectDoesNotExist:
					pass
				else:
					submission = json.loads(submission.form_data)
					for key, val in submission.items():
						form.fields[key].initial = val
		
		context = self.get_context(request)
		context['form'] = form
		return render(
			request,
			self.template,
			context
		)




class EventRegistrationFormField(surveys_models.AbstractFormField):
	page = ParentalKey(EventRegistrationPage, related_name='event_registration_form_fields')


class CustomEventSubmission(surveys_models.AbstractFormSubmission):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

	def get_data(self):
		form_data = super(CustomEventSubmission, self).get_data()
		form_data.update({
			'username': self.user.username,
			'email': self.user.email,
			'institution': self.user.institution,
			'fullname': self.user.first_name + ' ' + self.user.last_name,
			'tshirt_size': self.user.tshirt_size,
		})
		
		return form_data

