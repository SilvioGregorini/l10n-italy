# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class AccountGroupCEE(models.Model):
    _inherit = 'account.group'

    cee_account_ids = fields.One2many(
        comodel_name='account.account',
        inverse_name='cee_group_id',
        string="CEE accounts"
    )

    cee_group = fields.Boolean(
        string="Civil code group"
    )


class Account(models.Model):
    _inherit = 'account.account'

    cee_group_id = fields.Many2one(
        'account.group',
        string="Civil code group"
    )

    def get_grouped_accounts_vals_for_switch(self):
        accounts_grouped = {}
        for account in self:
            key = account.group_id.id, account.cee_group_id.id
            if key not in accounts_grouped:
                accounts_grouped[key] = []
            accounts_grouped[key].append(account.id)
        return accounts_grouped

    def switch_groups(self):
        if not self:
            return

        # For faster computations, group data to launch `write` upon recordsets
        # instead of updating accounts one by one
        accounts_grouped = self.get_grouped_accounts_vals_for_switch()
        for (group_id, cee_group_id), account_ids in accounts_grouped.items():
            self.browse(account_ids).write({
                'cee_group_id': group_id,
                'group_id': cee_group_id,
            })
