from django.urls import path

from moneyflow.views import *
from . import views

urlpatterns = [
    path("", frontpage, name="frontpage"),
    path("dashboard/", dashboard, name="dashboard"),
    path("accounts/", views.AccountsList.as_view(), name="accounts"),
    path(
        "accounts/<int:pk>/",
        views.AccountDetail.as_view(),
        name="account-detail",
    ),
    path("transactions/", views.TransactionsList.as_view(), name="transactions"),
    path(
        "transactions/create/",
        views.TransactionCreate.as_view(),
        name="transaction-create",
    ),
    path(
        "transactions/<int:pk>/",
        views.TransactionDetail.as_view(),
        name="transaction-detail",
    ),
    path("categories/", views.CategoriesList.as_view(), name="categories"),
    path("documents/", views.DocumentsList.as_view(), name="documents"),
    path("documents/<int:pk>/", views.DocumentDetail.as_view(), name="document-detail"),
]
