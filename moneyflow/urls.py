from django.urls import path

from moneyflow.views import *
from . import views

urlpatterns = [
    path("", frontpage, name="frontpage"),
    
    path("accounts/", views.AccountsList.as_view(), name="accounts"),
    path("accounts/<int:pk>/",
        views.AccountDetail.as_view(), name="account-detail"),
    
    path("transactions/", views.TransactionsList.as_view(), name="transactions"),
    path("transactions/<int:pk>/", views.TransactionDetail.as_view(), name="transaction-detail"),
    path("transactions/create/", views.TransactionCreate.as_view(), name="transaction-create"),
    
    path("categories/", views.CategoryList.as_view(), name="categories"),
    path("categories/<int:pk>/", views.CategoryDetail.as_view(), name="category-detail"),
    path("categories/create/", views.CategoryCreate.as_view(), name="category-create"),
    
    path("categories/create-defaults", views.create_default_categories, name="categories-create-defaults"),
    
    path("documents/", views.DocumentsList.as_view(), name="documents"),
    path("documents/<int:pk>/", views.DocumentDetail.as_view(), name="document-detail"),
]
