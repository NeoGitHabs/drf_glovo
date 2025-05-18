from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin, TranslationInlineModelAdmin
from .translate import *


class ContactInlines(admin.TabularInline, TranslationInlineModelAdmin):
    model = Contact
    extra = 1

class ProductInlines(admin.TabularInline, TranslationInlineModelAdmin):
    model = Product
    extra = 1

class ComboInlines(admin.TabularInline, TranslationInlineModelAdmin):
    model = Combo
    extra = 1

@admin.register(Store)
class StoreAdmin(TranslationAdmin):
    inlines = [ContactInlines, ProductInlines, ComboInlines]
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

@admin.register(Category, StoreReview)
class TranslateAdmin(TranslationAdmin):
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


admin.site.register(UserProfile)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(Courier)
admin.site.register(CourierRating)