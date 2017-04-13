# -*- coding: utf-8 -*-
# Copyright 2015 Lorenzo Battistini <lorenzo.battistini@agilebg.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.osv import osv


class mail_thread(osv.AbstractModel):
    _inherit = 'mail.thread'

    def message_route_verify(
        self, cr, uid, message, message_dict, route, update_author=True,
        assert_model=True, create_fallback=True, allow_private=False,
        context=None
    ):
        res = ()
        if context is None:
            context = {}
        try:
            res = super(mail_thread, self).message_route_verify(
                cr, uid, message, message_dict, route,
                update_author=update_author, assert_model=assert_model,
                create_fallback=create_fallback, allow_private=allow_private,
                context=context)
        except ValueError as ve:
            fetchmail_server_id = context.get('fetchmail_server_id')
            if not fetchmail_server_id:
                raise ve
            fetchmail_server = self.pool['fetchmail.server'].browse(
                cr, uid, fetchmail_server_id, context)
            if not fetchmail_server.error_notice_template_id:
                raise ve
            context['sender_message'] = message
            context['route_exception'] = ve
            self.pool['mail.template'].send_mail(
                cr, uid, fetchmail_server.error_notice_template_id.id,
                fetchmail_server.id, context=context)
            context['error_notice_sent'] = True
        return res

    def message_route(
        self, cr, uid, message, message_dict, model=None, thread_id=None,
        custom_values=None, context=None
    ):
        if context is None:
            context = {}
        res = []
        try:
            res = super(mail_thread, self).message_route(
                cr, uid, message, message_dict, model=model,
                thread_id=thread_id, custom_values=custom_values,
                context=context)
        except ValueError as ve:
            if context.get('error_notice_sent'):
                # avoid raising exception and setting mail message UNSEEN
                return []
            else:
                raise ve
        return res
