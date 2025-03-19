from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import User

class Merek(models.Model):
    nama = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nama

class MasterDus(models.Model):
    tipe = models.CharField(max_length=20, unique=True)
    merek = models.ForeignKey(Merek, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.tipe} - {self.merek or 'Tanpa Merek'}"

class Dus(models.Model):
    tipe = models.ForeignKey(MasterDus, on_delete=models.CASCADE)
    
    def stok_tersedia(self):
        stok_terakhir = Stok.objects.filter(tipe=self).order_by('-tanggal').first()
        return stok_terakhir.stok_akhir if stok_terakhir else 0

    def __str__(self):
        return f"{self.tipe.tipe} - {self.tipe.merek or 'Tanpa Merek'}"

class TransaksiMasuk(models.Model):
    tanggal = models.DateTimeField(default=timezone.now)
    tipe = models.ForeignKey(Dus, on_delete=models.CASCADE)
    jumlah_masuk = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.tanggal} - {self.tipe}"


class TransaksiKeluar(models.Model):
    tanggal = models.DateTimeField(default=timezone.now)
    tipe = models.ForeignKey(Dus, on_delete=models.CASCADE)
    jumlah_keluar = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Menambahkan field user

    def save(self, *args, **kwargs):
        if not self.user_id and hasattr(self, '_request_user'):
            self.user = self._request_user  # Menyimpan user yang sedang login
        
        if self.tipe.stok_tersedia() < self.jumlah_keluar:
            raise ValidationError("Stok tidak mencukupi untuk transaksi ini.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tanggal} - {self.tipe} ({self.user})"


class Stok(models.Model):
    tipe = models.ForeignKey(Dus, on_delete=models.CASCADE)
    tanggal = models.DateField(auto_now_add=True)
    stok_awal = models.PositiveIntegerField(default=0)
    stok_masuk = models.PositiveIntegerField(default=0)
    stok_keluar = models.PositiveIntegerField(default=0)
    stok_akhir = models.PositiveIntegerField(default=0)

    def hitung_stok(self):
        stok_masuk = TransaksiMasuk.objects.filter(
            tipe=self.tipe, tanggal__date=self.tanggal
        ).aggregate(Sum("jumlah_masuk"))['jumlah_masuk__sum'] or 0
        
        stok_keluar = TransaksiKeluar.objects.filter(
            tipe=self.tipe, tanggal__date=self.tanggal
        ).aggregate(Sum("jumlah_keluar"))['jumlah_keluar__sum'] or 0

        stok_sebelumnya = Stok.objects.filter(
            tipe=self.tipe, tanggal__lt=self.tanggal
        ).order_by('-tanggal').values('stok_akhir').first()
        
        stok_awal = stok_sebelumnya['stok_akhir'] if stok_sebelumnya else 0
        self.stok_awal = stok_awal
        self.stok_masuk = stok_masuk
        self.stok_keluar = stok_keluar
        self.stok_akhir = stok_awal + stok_masuk - stok_keluar

    def save(self, *args, **kwargs):
        self.hitung_stok()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tanggal} - {self.tipe.tipe} | Awal: {self.stok_awal}, Masuk: {self.stok_masuk}, Keluar: {self.stok_keluar}, Akhir: {self.stok_akhir}"

@receiver(post_save, sender=TransaksiMasuk)
@receiver(post_save, sender=TransaksiKeluar)
@receiver(post_delete, sender=TransaksiMasuk)
@receiver(post_delete, sender=TransaksiKeluar)
def update_laporan_stok(sender, instance, **kwargs):
    tanggal_laporan = instance.tanggal.date()
    laporan, _ = Stok.objects.get_or_create(tipe=instance.tipe, tanggal=tanggal_laporan)
    laporan.hitung_stok()
    laporan.save()
