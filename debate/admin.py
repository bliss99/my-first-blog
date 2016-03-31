from django.contrib import admin

from .models import Agenda, Opinion, Category, OpinionLink

class OpinionLinkInline(admin.TabularInline):
    model = OpinionLink
    extra = 1
    fk_name = 'parent_opinion'

class OpinionAdmin(admin.ModelAdmin):
    inlines = (OpinionLinkInline,)

admin.site.register(Opinion, OpinionAdmin)
admin.site.register(OpinionLink)
admin.site.register(Agenda)
admin.site.register(Category)