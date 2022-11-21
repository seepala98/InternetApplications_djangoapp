from django.contrib import admin
from .models import Category, Product, Client, Order

# Register your models here.
admin.site.register(Category)
# admin.site.register(Product)
# admin.site.register(Client)
admin.site.register(Order)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'available')

    def add_50(self, request, queryset):
        for product in queryset:
            product.stock += 50
            product.save()
            queryset.update(stock=product.stock)

    # add the action to the ProductAdmin class
    actions = ['add_50']


admin.site.register(Product, ProductAdmin)

class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'city')

admin.site.register(Client, ClientAdmin)

