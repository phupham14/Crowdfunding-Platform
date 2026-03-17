from rest_framework import serializers
from accounts.models.wallet import Wallet

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['balance', 'currency']
