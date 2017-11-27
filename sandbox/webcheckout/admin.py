# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
import models
# Register your models here.



@admin.register(models.Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('state_pol', 'response_message_pol', 'value', 'currency', 'date')
    icon = '<i class="material-icons">payment</i>'
    list_per_page = 10

    def get_readonly_fields(self, request, obj=None):
        # make all fields readonly
        readonly_fields = list(set(
            [field.name for field in self.opts.local_fields] +
            [field.name for field in self.opts.local_many_to_many]
        ))
        if 'is_submitted' in readonly_fields:
            readonly_fields.remove('is_submitted')
        return readonly_fields

    def has_add_permission(self, request):
        return False
    # end def

    def has_delete_permission(self, request, obj=None):
        return False
    # end def

    def get_actions(self, request):
        actions = super(PagoAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        # end if
        return actions
    # end def
# end class
