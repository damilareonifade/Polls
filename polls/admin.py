from django.contrib import admin

from .models import *


class OptionInline(admin.TabularInline):
    model = Option
    

@admin.register(Polls)
class PollsAdmin(admin.ModelAdmin):
    list_display = ['title','slug','author','is_active']
    prepopulated_fields = {'title':('slug',)}
    inlines = [OptionInline,]
    
admin.site.register(Vote)
