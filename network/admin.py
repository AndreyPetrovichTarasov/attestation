from django.contrib import admin
from django.utils.html import format_html
from .models import NetworkNode, Product


@admin.action(description="Очистить задолженность перед поставщиком")
def clear_debt(modeladmin, request, queryset):
    queryset.update(debt=0)


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "country", "supplier_link", "debt")
    list_filter = ("city",)
    actions = [clear_debt]
    search_fields = ("name",)
    readonly_fields = ("created_at",)  # Поля только для чтения

    # Отображение ссылки на поставщика в списке
    def supplier_link(self, obj):
        if obj.supplier:
            return format_html(
                '<a href="/admin/network/networknode/{}/change/">{}</a>',
                obj.supplier.id,
                obj.supplier.name,
            )
        return "-"

    supplier_link.short_description = "Поставщик"

    # Метод для отображения ссылки на поставщика на странице редактирования
    def supplier_link_detail(self, obj):
        if obj and obj.supplier:
            return format_html(
                '<a href="/admin/network/networknode/{}/change/">{}</a>',
                obj.supplier.id,
                obj.supplier.name,
            )
        return "-"

    supplier_link_detail.short_description = "Поставщик"

    # Переопределяем метод get_fieldsets
    def get_fieldsets(self, request, obj=None):
        # Стандартные поля
        fieldsets = super().get_fieldsets(request, obj)

        # Если объект существует (мы на странице редактирования), добавляем ссылку на поставщика
        if obj:
            supplier_fieldset = (
                "Поставщик",
                {
                    "fields": ("supplier_link_detail",),
                },
            )
            fieldsets = list(fieldsets)
            fieldsets.append(supplier_fieldset)

        return fieldsets

    # Переопределяем метод get_readonly_fields, чтобы сделать ссылку на поставщика только для чтения
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if obj:
            readonly_fields += ("supplier_link_detail",)
        return readonly_fields


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "model", "release_date", "node")
