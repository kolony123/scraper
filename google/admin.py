from django.contrib import admin

# Register your models here.
from .models import SearchResult, TimeLimit, Link


@admin.register(SearchResult)
class SearchResultAdmin(admin.ModelAdmin):
    pass


@admin.register(TimeLimit)
class TimeLimitAdmin(admin.ModelAdmin):
    pass


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    pass