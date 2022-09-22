from django.db import models


class ProcessingStatus(models.Model):
    PENDING_SLUG = 'pending'
    PROCESSING_SLUG = 'processing'
    PROCESSED_SLUG = 'processed'

    label = models.CharField(max_length=255, blank=False, null=False)
    slug = models.CharField(max_length=255, blank=False, null=False, unique=True)

    class Meta:
        ordering = ['label']

    def __str__(self):
        return self.label


class CSVImport(models.Model):
    original_name = models.CharField(max_length=255, blank=False, null=False)
    stored_name = models.CharField(max_length=255, blank=False, null=False, unique=True)
    uploaded_at = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    processed_at = models.DateTimeField(blank=True, null=True)
    processing_status = models.ForeignKey(ProcessingStatus, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.original_name} - {self.uploaded_at}"


class Country(models.Model):
    label = models.CharField(max_length=255, blank=False, null=False)
    slug = models.CharField(max_length=255, blank=False, null=False, unique=True)

    class Meta:
        ordering = ['label']

    def __str__(self):
        return self.label


class Currency(models.Model):
    label = models.CharField(max_length=255, blank=False, null=False)
    iso_code = models.CharField(max_length=255, blank=False, null=False, unique=True)

    class Meta:
        ordering = ['label']

    def __str__(self):
        return self.label


class CurrencyValue(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, blank=False, null=False)
    day = models.DateField(blank=False, null=False)
    rate = models.FloatField(blank=False, null=False)

    class Meta:
        ordering = ['day', 'currency']

    def __str__(self):
        return f"{self.currency.label} - {self.day}"


class TradeType(models.Model):
    SALE_SLUG = 'sale'
    PURCHASE_SLUG = 'purchase'

    label = models.CharField(max_length=255, blank=False, null=False)
    slug = models.CharField(max_length=255, blank=False, null=False, unique=True)

    class Meta:
        ordering = ['label']

    def __str__(self):
        return self.label


class TradeTypeSpelling(models.Model):
    spelling = models.CharField(max_length=255, blank=False, null=False)
    trade_type = models.ForeignKey(TradeType, on_delete=models.CASCADE)

    class Meta:
        ordering = ['spelling']

    def __str__(self):
        return self.spelling


class Trade(models.Model):
    date = models.DateTimeField(blank=False, null=False)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=False, null=False)
    trade_type = models.ForeignKey(TradeType, on_delete=models.CASCADE, blank=False, null=False)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, blank=False, null=False)
    net = models.FloatField(blank=False, null=False)
    vat = models.FloatField(blank=False, null=False)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f"{self.trade_type.label} - {self.trade_type}"
