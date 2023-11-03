from django.contrib import admin

from misinfo_main.forms import DBQueryAdminForm
from misinfo_main.models import Paper_SeSc, PaperClassification, DBQuery


class PaperClassAdmin(admin.ModelAdmin):

    list_display = ('paperclass',)
    exclude = []

class DBQueryAdmin(admin.ModelAdmin):

    list_display = ('id', 'active', 'updated_at', 'query')
    exclude = []
    form = DBQueryAdminForm

class PaperAdmin(admin.ModelAdmin):

    list_display = ('title', 'id', 'paperclass', 'comment')
    list_filter = ('paperclass',)
    exclude = []
# Register your models here.
admin.site.register(Paper_SeSc, PaperAdmin)
admin.site.register(PaperClassification)
admin.site.register(DBQuery, DBQueryAdmin)
