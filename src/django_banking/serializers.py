from rest_framework import serializers

from django_banking.models import Trade, Country, Currency, TradeType


class TradeCSVSerializer(serializers.Serializer):
    file = serializers.FileField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    class Meta:
        fields = ('file',)


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = ['label', 'slug']


class CurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = ['label', 'iso_code']


class TradeTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = TradeType
        fields = ['label']


class TradeSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(format="%Y-%m-%d")
    country = CountrySerializer()
    trade_type = TradeTypeSerializer()
    currency = CurrencySerializer()

    class Meta:
        model = Trade
        fields = ['date', 'country', 'trade_type', 'currency', 'net', 'vat']
