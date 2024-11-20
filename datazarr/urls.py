from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('info', views.Info),
    path('u10/<str:typechart>/<str:unidadmedida>/<str:latitude>/<str:longitude>/<str:time>', views.u10),
    path('u/<str:typechart>/<str:unidadmedida>/<str:latitude>/<str:longitude>/<str:time>/<str:level>', views.u),
    path('t2m/<str:typechart>/<str:unidadmedida>/<str:latitude>/<str:longitude>/<str:time>', views.t2m),
    path('t/<str:typechart>/<str:unidadmedida>/<str:latitude>/<str:longitude>/<str:time>/<str:level>', views.t),
    path('msl/<str:typechart>/<str:unidadmedida>/<str:latitude>/<str:longitude>/<str:time>', views.msl),
    path('q/<str:typechart>/<str:unidadmedida>/<str:latitude>/<str:longitude>/<str:time>/<str:level>', views.q),
    path('sp/<str:typechart>/<str:unidadmedida>/<str:latitude>/<str:longitude>/<str:time>', views.sp),
    path('tisr/<str:typechart>/<str:unidadmedida>/<str:latitude>/<str:longitude>/<str:time>', views.tisr),
    path('tcc/<str:typechart>/<str:unidadmedida>/<str:latitude>/<str:longitude>/<str:time>', views.tcc),
    path('w/<str:typechart>/<str:unidadmedida>/<str:latitude>/<str:longitude>/<str:time>/<str:level>', views.w),
    path('tp/<str:typechart>/<str:unidadmedida>/<str:latitude>/<str:longitude>/<str:time>', views.tp),
]
