from django import forms


class InvoiceForm(forms.Form):

    customer_name = forms.CharField(
        max_length=100
    )

    customer_email = forms.EmailField()

    customer_phone = forms.CharField(
        max_length=15
    )

    customer_address = forms.CharField(
        widget=forms.Textarea
    )


class ItemForm(forms.Form):

    product_name = forms.CharField(
        max_length=200
    )

    quantity = forms.IntegerField(
        min_value=1
    )

    price = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=0
    )