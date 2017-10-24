from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)

from authentication.models import APIAuth

class APIAuthModelAdmin(ModelAdmin):
	model = APIAuth
	menu_label = 'API Registration'
	menu_icon = 'password'
	list_display = ('description', 'secret')

modeladmin_register(APIAuthModelAdmin)