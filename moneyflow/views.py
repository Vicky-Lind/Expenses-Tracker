from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Account, Document


from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views.generic import DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect


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


class OwnerFilteredMixin(LoginRequiredMixin):
    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class AccountsList(OwnerFilteredMixin, ListView):
    model = Account


class AccountDetail(OwnerFilteredMixin, DetailView):
    model = Account

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["transactions"] = self.object.transactions.all()
        return context


class TransactionsList(OwnerFilteredMixin, ListView):
    pass


class CategoriesList(OwnerFilteredMixin, ListView):
    pass


class DocumentsList(OwnerFilteredMixin, ListView):
    model = Document


class DocumentDetail(OwnerFilteredMixin, DetailView):
    model = Document

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["transactions"] = self.object.transactions.all()
        return context
