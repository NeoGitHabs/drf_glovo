from modeltranslation.translator import TranslationOptions, register
from .models import Category, Contact, Product, Combo, StoreReview, Store


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('product_name', 'product_description')

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('category_name',)

@register(Contact)
class ContactTranslationOptions(TranslationOptions):
    fields = ('contact_name',)

@register(Combo)
class ComboTranslationOptions(TranslationOptions):
    fields = ('combo_name', 'combo_description')

@register(Store)
class StoreTranslationOptions(TranslationOptions):
    fields = ('store_name', 'store_description')

@register(StoreReview)
class StoreReviewTranslationOptions(TranslationOptions):
    fields = ('review_text_store',)