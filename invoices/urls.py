from django.urls import path

from . import views


urlpatterns = [

    path(
        "",
        views.dashboard,
        name="dashboard"
    ),

    path(
        "register/",
        views.register_view,
        name="register"
    ),

    path(
        "login/",
        views.login_view,
        name="login"
    ),

    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),

    path(
        "create/",
        views.create_invoice,
        name="create_invoice"
    ),

    path(
        "invoice/<int:invoice_id>/",
        views.invoice_detail,
        name="invoice_detail"
    ),

    path(
        "invoice/<int:invoice_id>/delete/",
        views.delete_invoice,
        name="delete_invoice"
    ),
]