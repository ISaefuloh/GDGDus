from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Stok, TransaksiMasuk, TransaksiKeluar, Merek, MasterDus, Dus
from .forms import TransaksiMasukForm, TransaksiKeluarForm, MerekForm, MasterDusForm, DusForm

from django.db.models import Sum, Subquery, OuterRef, Value, IntegerField, F
from django.db.models.functions import Coalesce
from django.utils.timezone import now

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .serializers import (
    UserSerializer, DusSerializer, TransaksiMasukSerializer, TransaksiKeluarSerializer, StokSerializer
)

class LoginView(APIView):
    permission_classes = []

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            })
        return Response({"error": "Invalid credentials"}, status=400)

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged out successfully"})
        except Exception:
            return Response({"error": "Invalid token"}, status=400)

class StokListView(generics.ListAPIView):
    queryset = Stok.objects.all()
    serializer_class = StokSerializer
    permission_classes = [permissions.IsAuthenticated]

class TransaksiMasukCreateView(generics.CreateAPIView):
    queryset = TransaksiMasuk.objects.all()
    serializer_class = TransaksiMasukSerializer
    permission_classes = [permissions.IsAuthenticated]

class TransaksiKeluarCreateView(generics.CreateAPIView):
    queryset = TransaksiKeluar.objects.all()
    serializer_class = TransaksiKeluarSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


###############################################

def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("stok-list")
    else:
        form = UserCreationForm()
    return render(request, "GDGDus/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("stok-list")
    else:
        form = AuthenticationForm()
    return render(request, "GDGDus/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("login")

def home(request):
    return render(request, "GDGDus/home.html")


class MerekListView(LoginRequiredMixin, ListView):
    model = Merek
    template_name = "GDGDus/merek_list.html"
    context_object_name = "merek_list"


class MerekCreateView(LoginRequiredMixin, CreateView):
    model = Merek
    form_class = MerekForm
    template_name = "GDGDus/merek_form.html"
    success_url = reverse_lazy("merek-list")

    def form_valid(self, form):
        messages.success(self.request, "Merek berhasil ditambahkan.")
        return super().form_valid(form)


class MerekUpdateView(LoginRequiredMixin, UpdateView):
    model = Merek
    form_class = MerekForm
    template_name = "GDGDus/merek_form.html"
    success_url = reverse_lazy("merek-list")

    def form_valid(self, form):
        messages.success(self.request, "Merek berhasil diperbarui.")
        return super().form_valid(form)


class MerekDeleteView(LoginRequiredMixin, DeleteView):
    model = Merek
    template_name = "GDGDus/merek_delete.html"
    success_url = reverse_lazy("merek-list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Merek berhasil dihapus.")
        return super().delete(request, *args, **kwargs)

# Views for MasterDus
class MasterDusListView(LoginRequiredMixin, ListView):
    model = MasterDus
    template_name = "GDGDus/masterdus_list.html"
    context_object_name = "masterdus_list"

class MasterDusCreateView(LoginRequiredMixin, CreateView):
    model = MasterDus
    form_class = MasterDusForm
    template_name = "GDGDus/masterdus_form.html"
    success_url = reverse_lazy("masterdus-list")

class MasterDusUpdateView(LoginRequiredMixin, UpdateView):
    model = MasterDus
    form_class = MasterDusForm
    template_name = "GDGDus/masterdus_form.html"
    success_url = reverse_lazy("masterdus-list")

class MasterDusDeleteView(LoginRequiredMixin, DeleteView):
    model = MasterDus
    template_name = "GDGDus/masterdus_delete.html"
    success_url = reverse_lazy("masterdus-list")

# Views for Dus
class DusListView(LoginRequiredMixin, ListView):
    model = Dus
    template_name = "GDGDus/dus_list.html"
    context_object_name = "dus_list"


class DusCreateView(LoginRequiredMixin, CreateView):
    model = Dus
    form_class = DusForm
    template_name = "GDGDus/dus_form.html"
    success_url = reverse_lazy("dus-list")


class DusUpdateView(LoginRequiredMixin, UpdateView):
    model = Dus
    form_class = DusForm
    template_name = "GDGDus/dus_form.html"
    success_url = reverse_lazy("dus-list")


class DusDeleteView(LoginRequiredMixin, DeleteView):
    model = Dus
    template_name = "GDGDus/dus_delete.html"
    success_url = reverse_lazy("dus-list")


class StokListView(LoginRequiredMixin, ListView):
    model = Stok
    template_name = "GDGDus/stok_list.html"
    context_object_name = "stok_list"

    def get_queryset(self):
        tanggal_mulai = self.request.GET.get("tanggal_mulai")
        tanggal_selesai = self.request.GET.get("tanggal_selesai")

        if not tanggal_mulai:
            tanggal_mulai = now().date()
        if not tanggal_selesai:
            tanggal_selesai = now().date()

        # Subquery untuk mendapatkan stok akhir sebelum tanggal_mulai (stok awal)
        subquery_stok_awal = Stok.objects.filter(
            tipe=OuterRef("tipe"),
            tanggal__lt=tanggal_mulai
        ).order_by("-tanggal").values("stok_akhir")[:1]

        queryset = Stok.objects.filter(tanggal__range=[tanggal_mulai, tanggal_selesai])

        queryset = queryset.values("tipe__tipe__tipe").annotate(
            total_stok_awal=Coalesce(Subquery(subquery_stok_awal, output_field=IntegerField()), Value(0)),
            total_stok_masuk=Coalesce(Sum("stok_masuk"), Value(0)),
            total_stok_keluar=Coalesce(Sum("stok_keluar"), Value(0)),
        ).annotate(
            total_stok_akhir=F("total_stok_awal") + F("total_stok_masuk") - F("total_stok_keluar")
        ).order_by("tipe__tipe__tipe")

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tanggal_mulai = self.request.GET.get("tanggal_mulai") or now().date()
        tanggal_selesai = self.request.GET.get("tanggal_selesai") or now().date()

        context["tanggal_mulai"] = tanggal_mulai
        context["tanggal_selesai"] = tanggal_selesai

        return context

    
class TransaksiMasukListView(LoginRequiredMixin, ListView):
    model = TransaksiMasuk
    template_name = "GDGDus/transaksimasuk_list.html"
    context_object_name = "transaksimasuk_list"

class TransaksiKeluarListView(LoginRequiredMixin, ListView):
    model = TransaksiKeluar
    template_name = "GDGDus/transaksikeluar_list.html"
    context_object_name = "transaksikeluar_list"

class TransaksiMasukCreateView(LoginRequiredMixin, CreateView):
    model = TransaksiMasuk
    form_class = TransaksiMasukForm
    template_name = "GDGDus/transaksi_masuk_form.html"
    success_url = reverse_lazy("stok-list")

    def form_valid(self, form):
        messages.success(self.request, "Transaksi masuk berhasil ditambahkan.")
        return super().form_valid(form)


class TransaksiKeluarCreateView(LoginRequiredMixin, CreateView):
    model = TransaksiKeluar
    form_class = TransaksiKeluarForm
    template_name = "GDGDus/transaksi_keluar_form.html"
    success_url = reverse_lazy("stok-list")

    def form_valid(self, form):
        form.instance.user = self.request.user  # Menyimpan user yang sedang login
        
        if form.instance.tipe.stok_tersedia() < form.instance.jumlah_keluar:
            messages.error(self.request, "Stok tidak mencukupi.")
            return redirect("stok-list")
        
        messages.success(self.request, "Transaksi keluar berhasil ditambahkan.")
        return super().form_valid(form)


#class TransaksiKeluarCreateView(CreateView):
#    model = TransaksiKeluar
#    form_class = TransaksiKeluarForm
#    template_name = "GDGDus/transaksi_keluar_form.html"
#    success_url = reverse_lazy("stok-list")
#
#    def form_valid(self, form):
#        if form.instance.tipe.stok_tersedia() < form.instance.jumlah_keluar:
#            messages.error(self.request, "Stok tidak mencukupi.")
#            return redirect("stok-list")
#        messages.success(self.request, "Transaksi keluar berhasil ditambahkan.")
#        return super().form_valid(form)


class TransaksiMasukDeleteView(LoginRequiredMixin, DeleteView):
    model = TransaksiMasuk
    template_name = "GDGDus/transaksi_delete.html"
    success_url = reverse_lazy("stok-list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Transaksi masuk berhasil dihapus.")
        return super().delete(request, *args, **kwargs)


class TransaksiKeluarDeleteView(LoginRequiredMixin, DeleteView):
    model = TransaksiKeluar
    template_name = "GDGDus/transaksi_delete.html"
    success_url = reverse_lazy("stok-list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Transaksi keluar berhasil dihapus.")
        return super().delete(request, *args, **kwargs)
