# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
import models

class ConfirmacionPago(forms.ModelForm):

    class Meta:
        model = models.Pago
        exclude = ()
    # end class
# end class
