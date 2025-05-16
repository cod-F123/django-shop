from django.contrib import admin
from .models import Category , Product , ProductDetail , ProductFeature , ProductImage , Comment , WishedProduct

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    
class ExteraImageProductAdmin(admin.StackedInline):
    model = ProductImage
    extra = 1
    
class ExtraProductDetailAdmin(admin.StackedInline):
    model = ProductDetail
    extra = 1

class ExtraProductFeatureAdmin(admin.StackedInline):
    model = ProductFeature
    extra = 1

class ExtraCommentAdmin(admin.StackedInline):
    model = Comment
    extra = 1
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name","category","is_sale","price"]
    readonly_fields = ["slug",]
    inlines = [ExteraImageProductAdmin,ExtraProductDetailAdmin,ExtraProductFeatureAdmin]


admin.site.register(ProductDetail)
admin.site.register(ProductFeature)
admin.site.register(ProductImage)
admin.site.register(Comment)
admin.site.register(WishedProduct)
