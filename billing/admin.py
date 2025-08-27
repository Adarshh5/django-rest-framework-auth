
from django.contrib import admin
from .models import ShopSector, Shop, Bill, BillItem

class BillItemInline(admin.TabularInline):
    model = BillItem
    extra = 1 

@admin.register(ShopSector)
class ShopSectorAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',) 

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'owner', 'sector', 'created_at')
    list_filter = ('sector', 'created_at')
    search_fields = ('name', 'owner', 'address')
    autocomplete_fields = ('sector',)  # Requires search_fields in ShopSectorAdmin
    raw_id_fields = ('user',)  # Better widget for large user databases

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ('shop', 'customer_name', 'total_amount', 'created_at')
    list_filter = ('shop', 'created_at')
    search_fields = ('customer_name', 'shop__name', 'customer_number')
    inlines = [BillItemInline]
    
    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.instance.update_total()  # Update total after saving items

@admin.register(BillItem)
class BillItemAdmin(admin.ModelAdmin):
    list_display = ('bill', 'product_name', 'quantity', 'unit', 'price', 'total_price')
    list_filter = ('unit',)
    search_fields = ('product_name', 'bill__id')