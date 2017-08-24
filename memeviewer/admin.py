from django.contrib import admin

from memeviewer.models import Meem, FacebookMeem, TwitterMeem, DiscordMeem, ImageInContext


class FacebookInline(admin.TabularInline):
    model = FacebookMeem
    extra = 0


class TwitterInline(admin.TabularInline):
    model = TwitterMeem
    extra = 0


class DiscordInline(admin.TabularInline):
    model = DiscordMeem
    extra = 0


class MeemAdmin(admin.ModelAdmin):
    list_display = ('number', 'meme_id', 'template', 'context', 'gen_date', 'meme_url')
    ordering = ('-number',)
    list_display_links = ('meme_id',)
    inlines = [FacebookInline, TwitterInline, DiscordInline]
    search_fields = ('number', 'meme_id', 'context', 'template')

    def meme_url(self, obj):
        return '<a href="{0}" target="_blank">{1}</a>'.format(obj.get_info_url(), "Meme page")

    meme_url.allow_tags = True
    meme_url.short_description = 'Page'

admin.site.register(Meem, MeemAdmin)


class ImageInContextAdmin(admin.ModelAdmin):
    list_display = ('image_name', 'image_type', 'context')
    list_display_links = ('image_name',)
    search_fields = ('image_name', 'image_type', 'context')


admin.site.register(ImageInContext, ImageInContextAdmin)
