from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimestampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))

    class Meta:
        abstract = True


class OwnedModel(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("owner"),
    )

    class Meta:
        abstract = True


class Document(TimestampModel, OwnedModel):
    class Type(models.TextChoices):
        BILL = ("BILL", _("Bill"))
        RECEIPT = ("RECEIPT", _("Receipt"))
        ESTIMATION = ("ESTIMATION", _("Estimation"))
        OTHER = ("OTHER", _("Other"))

    type = models.CharField(max_length=20, choices=Type.choices, verbose_name=_("type"))

    name = models.CharField(max_length=100, blank=True, verbose_name=_("name"))

    file = models.FileField(upload_to="docs/%Y-%m-%d/", verbose_name=_("file"))

    class Meta:
        verbose_name = _("document")
        verbose_name_plural = _("documents")

    def __str__(self):
        return self.name if self.name else f"Document {self.id}"


class Category(TimestampModel, OwnedModel):
    name = models.CharField(max_length=100, verbose_name=_("name"))

    parent = models.ForeignKey(
        "self",
        blank=True,
        null=True,
        related_name="subcategories",
        on_delete=models.CASCADE,
        verbose_name=_("parent category"),
    )

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def __str__(self, level=0):
        # Varmista level-parametrilla, että syklit eivät aiheuta
        # loputonta rekursiota
        if self.parent and level < 20:
            parent_str = self.parent.__str__(level=level + 1)
        elif self.parent:
            parent_str = "..."
        else:
            parent_str = ""
        prefix = f"{parent_str} / " if parent_str else ""
        return f"{prefix}{self.name}"


class Account(TimestampModel, OwnedModel):
    name = models.CharField(max_length=100, verbose_name=_("name"))

    bank_account = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name=_("bank account"),
    )

    class Meta:
        verbose_name = _("account")
        verbose_name_plural = _("accounts")

    def __str__(self):
        return f"{self.id:04d} {self.name}"


class Transaction(TimestampModel):
    class Type(models.TextChoices):
        INCOME = ("INCOME", _("Income"))
        EXPENSE = ("EXPENSE", _("Expense"))

    class State(models.TextChoices):
        UPCOMING = ("UPCOMING", _("Upcoming"))
        DONE = ("DONE", _("Done"))
        CANCELED = ("CANCELED", _("Canceled"))
        MISSED = ("MISSED", _("Missed"))

    # class Category2(models.TextChoices):
    #     Car = ("Car", _("Auto"))
    #     Food = ("Food", _("Ruoka"))
    #     Home = ("Home", _("Koti"))
    #     Salary = ("Salary", _("Palkka"))
    #     Savings = ("Savings", _("Säästöt"))
    #     Shopping = ("Shopping", _("Shoppailu"))
    #     Transport = ("Transport", _("Liikenne"))
    #     Travel = ("Travel", _("Matkustus"))
    #     Utilities = ("Utilities", _("Laskut"))
    #     Other = ("Other", _("Muu"))

    account = models.ForeignKey(
        Account,
        on_delete=models.RESTRICT,
        verbose_name=_("account"),
        related_name="transactions",
    )

    name = models.CharField(
        max_length=100,
        verbose_name=_("name"),
        null=True,
    )

    description = models.TextField(
        max_length=1000,
        verbose_name=_("description"),
        null=True,
        blank=True,
    )

    type = models.CharField(
        max_length=20,
        choices=Type.choices,
        verbose_name=_("type"),
    )

    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_("category"),
    )

    # category2 = models.CharField(
    #     max_length=20,
    #     choices=Category2.choices,
    #     verbose_name=_("kategoria"),
    #     null=True,
    #     blank=True,
    # )

    state = models.CharField(
        max_length=20,
        choices=State.choices,
        verbose_name=_("state"),
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("created at"),
    )

    date = models.DateField(
        verbose_name=_("date"),
    )

    amount = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        verbose_name=_("amount"),
    )

    documents = models.ManyToManyField(
        Document,
        related_name="transactions",
        blank=True,
        verbose_name=_("documents"),
    )

    class Meta:
        verbose_name = _("transaction")
        verbose_name_plural = _("transactions")

    def __str__(self):
        return (
            f"{self.name}, {self.amount}€"
            if self.name
            else f"{self.date} {self.account} {self.amount} ({self.state})"
        )
