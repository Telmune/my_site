from django.contrib import admin

from .models import Product


admin.site.site_header = "My django app"
admin.site.site_title = "Title of django"
admin.site.index_title = "My admin"


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description')
    search_fields =  ('name',)
    list_editable = ('price', 'description')
    actions = ('make_zero',)
    def make_zero(self, request, qwuryset):
        qwuryset.update(price=0)

admin.site.register(Product, ProductAdmin)