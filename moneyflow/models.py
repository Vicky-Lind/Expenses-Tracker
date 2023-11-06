from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimestampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("luotu"))

    class Meta:
        abstract = True


class OwnedModel(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("omistaja"),
    )

    class Meta:
        abstract = True


class Document(TimestampModel, OwnedModel):
    class Type(models.TextChoices):
        BILL = ("BILL", _("Lasku"))
        RECEIPT = ("RECEIPT", _("Kuitti"))
        ESTIMATION = ("ESTIMATION", _("Laskelma"))
        OTHER = ("OTHER", _("Muu"))

    type = models.CharField(
        max_length=20, choices=Type.choices, verbose_name=_("tyyppi")
    )

    name = models.CharField(max_length=100, blank=True, verbose_name=_("nimi"))

    file = models.FileField(upload_to="docs/%Y-%m-%d/", verbose_name=_("tiedosto"))

    class Meta:
        verbose_name = _("dokumentti")
        verbose_name_plural = _("dokumentit")

    def __str__(self):
        return self.name if self.name else f"Document {self.id}"


class Category(TimestampModel, OwnedModel):
    name = models.CharField(max_length=100, verbose_name=_("nimi"))

    parent = models.ForeignKey(
        "self",
        blank=True,
        null=True,
        related_name="subcategories",
        on_delete=models.CASCADE,
        verbose_name=_("yläkategoria"),
    )

    class Meta:
        verbose_name = _("kategoria")
        verbose_name_plural = _("kategoriat")

    def __str__(self):
        prefix = f"{self.parent} / " if self.parent else ""
        return f"{prefix}{self.name}"


class Account(TimestampModel, OwnedModel):
    name = models.CharField(max_length=100, verbose_name=_("nimi"))

    bank_account = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name=_("pankitili"),
    )

    class Meta:
        verbose_name = _("tili")
        verbose_name_plural = _("tilit")

    def __str__(self):
        return f"{self.id:04d} {self.name}"


class Transaction(TimestampModel):
    class Type(models.TextChoices):
        INCOME = ("INCOME", _("Tulo"))
        EXPENSE = ("EXPENSE", _("Meno"))

    class State(models.TextChoices):
        UPCOMING = ("UPCOMING", _("Tuleva"))
        DONE = ("DONE", _("Tapahtunut"))
        CANCELED = ("CANCELED", _("Peruttu"))
        MISSED = ("MISSED", _("Mennyt"))

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
        verbose_name=_("tili"),
    )

    name = models.CharField(
        max_length=100,
        verbose_name=_("nimi"),
        null=True,
    )

    description = models.TextField(
        max_length=1000,
        verbose_name=_("kuvaus"),
        null=True,
        blank=True,
    )

    type = models.CharField(
        max_length=20,
        choices=Type.choices,
        verbose_name=_("tyyppi"),
    )

    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_("kategoria"),
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
        verbose_name=_("tila"),
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("luotu"),
    )

    date = models.DateField(
        verbose_name=_("päivämäärä"),
    )

    amount = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        verbose_name=_("summa"),
    )

    documents = models.ManyToManyField(
        Document,
        related_name="transactions",
        blank=True,
        verbose_name=_("dokumentit"),
    )

    class Meta:
        verbose_name = _("tapahtuma")
        verbose_name_plural = _("tapahtumat")

    def __str__(self):
        return (
            f"{self.name}, {self.amount}€"
            if self.name
            else f"{self.date} {self.account} {self.amount} ({self.state})"
        )
