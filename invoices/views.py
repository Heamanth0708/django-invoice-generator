from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import InvoiceForm
from .models import Invoice, InvoiceItem


def register_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(
                request,
                "Username already exists."
            )
            return redirect("register")

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(
            request,
            "Registration successful."
        )

        return redirect("login")

    return render(
        request,
        "register.html"
    )


def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect("dashboard")

        messages.error(
            request,
            "Invalid username or password."
        )

    return render(
        request,
        "login.html"
    )


@login_required
def logout_view(request):

    logout(request)

    return redirect("login")


@login_required
def dashboard(request):

    invoices = Invoice.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "dashboard.html",
        {
            "invoices": invoices
        }
    )


@login_required
def create_invoice(request):

    if request.method == "POST":

        customer_name = request.POST.get(
            "customer_name"
        )

        customer_email = request.POST.get(
            "customer_email"
        )

        customer_phone = request.POST.get(
            "customer_phone"
        )

        customer_address = request.POST.get(
            "customer_address"
        )

        product_names = request.POST.getlist(
            "product_name"
        )

        quantities = request.POST.getlist(
            "quantity"
        )

        prices = request.POST.getlist(
            "price"
        )

        invoice_number = (
            f"INV-{Invoice.objects.count() + 1:05d}"
        )

        subtotal = Decimal("0")

        items = []

        for i in range(len(product_names)):

            if not product_names[i]:
                continue

            quantity = int(quantities[i])

            price = Decimal(prices[i])

            total = quantity * price

            subtotal += total

            items.append(
                {
                    "product_name": product_names[i],
                    "quantity": quantity,
                    "price": price,
                    "total": total,
                }
            )

        gst = subtotal * Decimal("0.18")

        grand_total = subtotal + gst

        invoice = Invoice.objects.create(
            user=request.user,
            invoice_number=invoice_number,
            customer_name=customer_name,
            customer_email=customer_email,
            customer_phone=customer_phone,
            customer_address=customer_address,
            subtotal=subtotal,
            gst=gst,
            grand_total=grand_total
        )

        for item in items:

            InvoiceItem.objects.create(
                invoice=invoice,
                product_name=item["product_name"],
                quantity=item["quantity"],
                price=item["price"],
                total=item["total"]
            )

        messages.success(
            request,
            "Invoice created successfully."
        )

        return redirect(
            "invoice_detail",
            invoice_id=invoice.id
        )

    return render(
        request,
        "create_invoice.html"
    )


@login_required
def invoice_detail(request, invoice_id):

    invoice = get_object_or_404(
        Invoice,
        id=invoice_id,
        user=request.user
    )

    return render(
        request,
        "invoice_detail.html",
        {
            "invoice": invoice
        }
    )


@login_required
def delete_invoice(request, invoice_id):

    invoice = get_object_or_404(
        Invoice,
        id=invoice_id,
        user=request.user
    )

    if request.method == "POST":

        invoice.delete()

        messages.success(
            request,
            "Invoice deleted."
        )

        return redirect("dashboard")

    return render(
        request,
        "confirm_delete.html",
        {
            "invoice": invoice
        }
    )