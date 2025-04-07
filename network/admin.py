from django.contrib import admin
from .models import NetworkNode, Product


@admin.action(description="Очистить задолженность перед поставщиком")
def clear_debt(modeladmin, request, queryset):
    queryset.update(debt=0)


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'country', 'supplier', 'debt')
    list_filter = ('city',)
    actions = [clear_debt]
    search_fields = ('name',)

    readonly_fields = ('created_at',)

    def supplier_link(self, obj):
        if obj.supplier:
            return f'<a href="/admin/network/networknode/{obj.supplier.id}/change/">{obj.supplier.name}</a>'
        return "-"
    supplier_link.allow_tags = True
    supplier_link.short_description = "Поставщик"

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'model', 'release_date', 'node')
