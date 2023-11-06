from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Account


@login_required
def frontpage(request):
    context = {
        "account": Account.objects.filter(owner=request.user),
    }

    return render(request, "moneyflow/index.html", context)
