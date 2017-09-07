# -*- coding: utf-8 -*-
# Copyright 2017 Lorenzo Battistini - Agile Business Group
# Copyright 2017 Alex Comba - Agile Business Group
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl).

from openerp import api, models, SUPERUSER_ID, _
from openerp.exceptions import Warning


class IrModel(models.Model):
    _inherit = 'ir.model'

    def _register_hook(self, cr):

        def make_create():
            @api.model
            def create(self, vals):
                user = self.env.user
                if user.readonly_user:
                    raise Warning(
                        _('Error'),
                        _("Readonly user can't create records"))
                else:
                    return create.origin(vals)

        def make_write():
            @api.multi
            def write(self, vals):
                user = self.env.user
                if user.readonly_user:
                    raise Warning(
                        _('Error'),
                        _("Readonly user can't create records"))
                else:
                    return write.origin(vals)

        def make_unlink():
            @api.multi
            def unlink(self):
                user = self.env.user
                if user.readonly_user:
                    raise Warning(
                        _('Error'),
                        _("Readonly user can't create records"))
                else:
                    return unlink.origin()

        for model in self.browse(cr, SUPERUSER_ID, []):
            Model = self.pool.get(model.model)
            if Model:
                Model._patch_method('create', make_create())
                Model._patch_method('write', make_write())
                Model._patch_method('unlink', make_unlink())
        return super(IrModel, self)._register_hook(cr)
