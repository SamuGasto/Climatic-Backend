from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('info', views.Info),
    path('u10/<str:typechart>/<str:unidadmedida>/<str:latitude>/<str:longitude>/<str:time>', views.u10),
    path('u/<str:typechart>/<str:unidadmedida>/<str:latitude>/<str:longitude>/<str:time>', views.u),
    path('t2m/<str:typechart>/<str:unidadmedida>/<str:latitude>/<str:longitude>/<str:time>', views.t2m),
    path('anor/<str:typechart>/<str:unidadmedida>/<str:latitude>/<str:longitude>', views.anor),
    path('isor/<str:typechart>/<str:unidadmedida>/<str:latitude>/<str:longitude>', views.isor),
    path('z/<str:typechart>/<str:unidadmedida>/<str:latitude>/<str:longitude>/<str:time>/<str:level>', views.z),
    path('z_surface/<str:typechart>/<str:unidadmedida>/<str:latitude>/<str:longitude>', views.z_surface),
    path('cvh/<str:typechart>/<str:unidadmedida>/<str:latitude>/<str:longitude>', views.cvh),
    path('cl/<str:typechart>/<str:unidadmedida>/<str:latitude>/<str:longitude>', views.cl),
    path('lsm/<str:typechart>/<str:unidadmedida>/<str:latitude>/<str:longitude>', views.lsm),
    path('cvl/<str:typechart>/<str:unidadmedida>/<str:latitude>/<str:longitude>', views.cvl),
    path('msl/<str:typechart>/<str:unidadmedida>/<str:latitude>/<str:longitude>/<str:time>', views.msl),
    path('siconc/<str:typechart>/<str:unidadmedida>/<str:latitude>/<str:longitude>/<str:time>', views.siconc),
    path('sst/<str:typechart>/<str:unidadmedida>/<str:latitude>/<str:longitude>/<str:time>', views.sst),
    path('slor/<str:typechart>/<str:unidadmedida>/<str:latitude>/<str:longitude>', views.slor),
    path('slt/<str:typechart>/<str:unidadmedida>/<str:latitude>/<str:longitude>', views.slt),
    path('q/<str:typechart>/<str:unidadmedida>/<str:latitude>/<str:longitude>/<str:time>/<str:level>', views.q),
    path('sdfor/<str:typechart>/<str:unidadmedida>/<str:latitude>/<str:longitude>', views.sdfor),
    path('sdor/<str:typechart>/<str:unidadmedida>/<str:latitude>/<str:longitude>', views.sdor),
    path('sp/<str:typechart>/<str:unidadmedida>/<str:latitude>/<str:longitude>/<str:time>', views.sp),
    path('t/<str:typechart>/<str:unidadmedida>/<str:latitude>/<str:longitude>/<str:time>/<str:level>', views.t),
    path('tisr/<str:typechart>/<str:unidadmedida>/<str:latitude>/<str:longitude>/<str:time>', views.tisr),
    path('tcc/<str:typechart>/<str:unidadmedida>/<str:latitude>/<str:longitude>/<str:time>', views.tcc),
    path('tvh/<str:typechart>/<str:unidadmedida>/<str:latitude>/<str:longitude>', views.tvh),
    path('tvl/<str:typechart>/<str:unidadmedida>/<str:latitude>/<str:longitude>', views.tvl),
    path('w/<str:typechart>/<str:unidadmedida>/<str:latitude>/<str:longitude>/<str:time>/<str:level>', views.w),
]
