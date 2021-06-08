from django.contrib import admin
from tips.models import Tips, Tags, Links
# Register your models here.

# admin.site.register(Tips)
admin.site.register(Tags)
admin.site.register(Links)


@admin.register(Tips)
class TipsAdmin(admin.ModelAdmin):
    # list_select_related = ('tags',)
    list_display = ('tip', 'retweets', 'account', 'email')
    ordering = ('account', )