from django.contrib import admin

from .models import Invoice, InvoiceItem


class InvoiceItemInline(admin.TabularInline):

    model = InvoiceItem

    extra = 0


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):

    list_display = (
        "invoice_number",
        "customer_name",
        "invoice_date",
        "subtotal",
        "gst",
        "grand_total",
    )

    inlines = [
        InvoiceItemInline
    ]


@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):

    list_display = (
        "product_name",
        "quantity",
        "price",
        "total",
    )