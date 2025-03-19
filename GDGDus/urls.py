from django.urls import path, include
from .views import (
    home, register_view, login_view, logout_view,
    MerekListView, MerekCreateView, MerekUpdateView, MerekDeleteView,
    MasterDusListView, MasterDusCreateView, MasterDusUpdateView, MasterDusDeleteView,
    DusListView, DusCreateView, DusUpdateView, DusDeleteView,
    StokListView,
    TransaksiMasukCreateView, TransaksiKeluarCreateView,
    TransaksiMasukDeleteView, TransaksiKeluarDeleteView,
    TransaksiMasukListView, TransaksiKeluarListView,
)

#API
from .views import (
    LoginView, LogoutView, StokListView, TransaksiMasukCreateView, TransaksiKeluarCreateView
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    #API
    #path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('stok/', StokListView.as_view(), name='stok'),
    path('transaksi-masuk/', TransaksiMasukCreateView.as_view(), name='transaksi-masuk'),
    path('transaksi-keluar/', TransaksiKeluarCreateView.as_view(), name='transaksi-keluar'),


    #################################################

    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),

    path('', home, name='home'),
    
    # URL Merek
    path('merek/', MerekListView.as_view(), name='merek-list'),
    path('merek/tambah/', MerekCreateView.as_view(), name='merek-create'),
    path('merek/edit/<int:pk>/', MerekUpdateView.as_view(), name='merek-update'),
    path('merek/hapus/<int:pk>/', MerekDeleteView.as_view(), name='merek-delete'),
    
    # URL MasterDus
    path('masterdus/', MasterDusListView.as_view(), name='masterdus-list'),
    path('masterdus/tambah/', MasterDusCreateView.as_view(), name='masterdus-create'),
    path('masterdus/edit/<int:pk>/', MasterDusUpdateView.as_view(), name='masterdus-update'),
    path('masterdus/hapus/<int:pk>/', MasterDusDeleteView.as_view(), name='masterdus-delete'),
    
    # URL Dus
    path('dus/', DusListView.as_view(), name='dus-list'),
    path('dus/tambah/', DusCreateView.as_view(), name='dus-create'),
    path('dus/edit/<int:pk>/', DusUpdateView.as_view(), name='dus-update'),
    path('dus/hapus/<int:pk>/', DusDeleteView.as_view(), name='dus-delete'),
    
    # URL Stok
    path('stok/', StokListView.as_view(), name='stok-list'),
    
    # URL Transaksi
    path('transaksimasuk/', TransaksiMasukListView.as_view(), name='transaksimasuk-list'),
    path('transaksikeluar/', TransaksiKeluarListView.as_view(), name='transaksikeluar-list'),
    path('transaksimasuk/tambah/', TransaksiMasukCreateView.as_view(), name='transaksimasuk-create'),
    path('transaksikeluar/tambah/', TransaksiKeluarCreateView.as_view(), name='transaksikeluar-create'),
    path('transaksi/masuk/hapus/<int:pk>/', TransaksiMasukDeleteView.as_view(), name='transaksi-masuk-delete'),
    path('transaksi/keluar/hapus/<int:pk>/', TransaksiKeluarDeleteView.as_view(), name='transaksi-keluar-delete'),
    
]
