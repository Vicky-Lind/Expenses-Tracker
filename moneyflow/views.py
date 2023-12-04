from typing import Any
from django.contrib.auth.decorators import login_required
from django.db import models
from django.forms.models import BaseModelForm
from django.http import HttpResponse

from .models import Account, Document, Transaction, Category

from django.shortcuts import render, redirect
from django.views.generic import DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.views.generic.edit import CreateView

from django.urls import reverse


# @login_required
def frontpage(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
        else:
            # If the form is invalid, re-render the page with the form
            return render(request, "moneyflow/main.html", {"form": form})
    else:
        form = AuthenticationForm()
        return render(request, "moneyflow/main.html", {"form": form})


@login_required
def dashboard(request):
    return render(request, "moneyflow/dashboard.html")

# ------------------------------------#
class OwnerFilteredMixin(LoginRequiredMixin):
    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

class OwnerAutoFillinCreateView(OwnerFilteredMixin, CreateView):
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
# ------------------------------------#


class AccountsList(OwnerFilteredMixin, ListView):
    model = Account


class AccountDetail(OwnerFilteredMixin, DetailView):
    model = Account

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["transactions"] = self.object.transactions.all()
        return context


# ------------------------------------#


class TransactionsList(ListView):
    model = Transaction

    def get_queryset(self):
        return super().get_queryset().filter(account__owner=self.request.user)


class TransactionDetail(DetailView):
    model = Transaction

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class TransactionCreate(OwnerAutoFillinCreateView):
    model = Transaction
    fields = ["account", "name", "description", "type", "category", "state", "date", "amount", "documents"]

# ------------------------------------#

class CategoryList(OwnerFilteredMixin, ListView):
    model = Category


class CategoryDetail(OwnerFilteredMixin, DetailView):
    model = Category

class CategoryCreate(OwnerAutoFillinCreateView):
    model = Category
    fields = ["name", "parent"]
    
    
class DocumentsList(OwnerFilteredMixin, ListView):
    model = Document


class DocumentDetail(OwnerFilteredMixin, DetailView):
    model = Document

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["transactions"] = self.object.transactions.all()
        return context
    
def create_default_categories(request):
    
    return redirect(reverse("categories"))