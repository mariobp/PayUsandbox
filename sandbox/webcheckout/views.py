# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from sandbox.settings import APIKEY, ORIGIN, MERCHANTID, ACCOUNTID, URL_PAYU, TEST_PAYU
from django.http import HttpResponse, HttpResponseNotFound
import md5, string, random
# Create your views here.

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
# end def

def pagar(request):
    currency = "COP" # Moneda en la que se paga
    referenceCode = id_generator() # Debe ser unico por transacción
    buyerFullName = "Nombre del comprados"
    buyerEmail = "admin@gmail.com"
    amount = 20000 # Valor de la compra
    signature = "%s~%d~%s~%d~%s" % (APIKEY, MERCHANTID, referenceCode, amount, currency) # Es la firma digital creada para cada uno de las transacciones.
    signatureMD5 = md5.new(signature) # Se le aplica md5
    description = "Descripción del producto"
    confirmationUrl = "http://localhost:8000/payu/confirmacion/pago/" # Url de confirmación
    return render(request, 'webcheckout/compra.html', {"url": URL_PAYU, "test": TEST_PAYU, "merchantId": MERCHANTID, "accountId":ACCOUNTID, "referenceCode":referenceCode ,
                "buyerFullName":buyerFullName, "description": description, "currency": currency, "amount": amount, "buyerEmail": buyerEmail, "signature":signatureMD5.hexdigest(), "confirmationUrl": confirmationUrl})
#end def

def new_value(value):
    val = value.split(".")
    try:
        if val[1] == "00":
            num = val[0]+".0"
        else:
            num = value
        return num
    except:
        return value
# end if

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@csrf_exempt
def confirmacion(request):
    if request.method == "POST":
        form = forms.ConfirmacionPago(request.POST)
        state_pol = request.POST.get('state_pol', False)
        sign = request.POST.get('sign', False)
        if form.is_valid():
            con = form.save(commit=False)
            value = new_value(con.value)
            validacion = "%s~%d~%s~%s~%s~%s" % (APIKEY, con.merchant_id , con.reference_sale, value, con.currency, con.state_pol)
            validacionMD5 = md5.new(validacion)
            firma = validacionMD5.hexdigest()
            if sign == firma:
                con.validacion = True
            else:
                con.validacion = False
            # end if
            con.cita = cita
            con.save()
            return HttpResponse(status=200)
        # end if
        errors = form.errors.items()
        file = open(os.path.join(BASE_DIR, "confirmacion_ERROR.txt"), "w+")
        file.write(str(json.dumps(errors)))
        file.close()
        # return HttpResponse(json.dumps(errors), status=400)
    return HttpResponse(status=400)
# end def
