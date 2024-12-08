
from django.urls import path
from packApp2 import views as app2

urlpatterns = [
    path('pack_promocion/', app2.pack_promocion, name='pack_promocion'),
    path('ver_selecion/', app2.ver_selecion, name='ver_selecion'),

]
