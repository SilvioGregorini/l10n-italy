# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import models, fields, api


class TrialBalanceReportWizard(models.TransientModel):
    _inherit = 'trial.balance.report.wizard'

    cee_balance = fields.Boolean(
        string="Civil code statutory financial statements"
    )

    @api.onchange('cee_balance')
    def onchange_cee_balance(self):
        if self.cee_balance:
            self.hierarchy_on = 'relation'

    @api.multi
    def button_export_html(self):
        self.ensure_one()
        if self.cee_balance:
            accounts = self.env['account.account'].search([])
            accounts.switch_groups()
            res = super().button_export_html()
            accounts.switch_groups()
        else:
            res = super().button_export_html()
        return res

    @api.multi
    def button_export_pdf(self):
        self.ensure_one()
        if self.cee_balance:
            accounts = self.env['account.account'].search([])
            accounts.switch_groups()
            res = super().button_export_pdf()
            accounts.switch_groups()
        else:
            res = super().button_export_html()
        return res

    @api.multi
    def button_export_xlsx(self):
        self.ensure_one()
        if self.cee_balance:
            accounts = self.env['account.account'].search([])
            accounts.switch_groups()
            res = super().button_export_xlsx()
            accounts.switch_groups()
        else:
            res = super().button_export_html()
        return res

    def _prepare_report_trial_balance(self):
        return dict(
            super()._prepare_report_trial_balance(),
            cee_balance=self.cee_balance
        )
