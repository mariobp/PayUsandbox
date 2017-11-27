from django.conf.urls import include, url
import views

"""
 Payu
"""

urlpatterns = [
    url(r'^pagar/$', views.pagar, name="pagar"),
    url(r'^confirmacion/pago/$', views.confirmacion, name="confirmacion"),
]
