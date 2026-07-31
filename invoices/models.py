from django.db import models
from django.contrib.auth.models import User


class Invoice(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    invoice_number = models.CharField(
        max_length=50,
        unique=True
    )

    customer_name = models.CharField(
        max_length=100
    )

    customer_email = models.EmailField()

    customer_phone = models.CharField(
        max_length=15
    )

    customer_address = models.TextField()

    invoice_date = models.DateField(
        auto_now_add=True
    )

    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    gst = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    grand_total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.invoice_number


class InvoiceItem(models.Model):

    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product_name = models.CharField(
        max_length=200
    )

    quantity = models.PositiveIntegerField()

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    total = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    def __str__(self):
        return self.product_name