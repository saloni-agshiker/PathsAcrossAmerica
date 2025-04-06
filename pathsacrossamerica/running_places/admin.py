from django.contrib import admin
from .models import RunningPlace, Review
admin.site.register(RunningPlace)

# Register your models here.
class MovieAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']
admin.site.register(RunningPlace, MovieAdmin)
admin.site.register(Review)