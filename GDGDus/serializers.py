from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Dus, TransaksiMasuk, TransaksiKeluar, Stok

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class DusSerializer(serializers.ModelSerializer):
    stok_tersedia = serializers.SerializerMethodField()

    class Meta:
        model = Dus
        fields = ['id', 'tipe', 'stok_tersedia']

    def get_stok_tersedia(self, obj):
        return obj.stok_tersedia()

class TransaksiMasukSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransaksiMasuk
        fields = '__all__'

class TransaksiKeluarSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransaksiKeluar
        fields = '__all__'

class StokSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stok
        fields = '__all__'
