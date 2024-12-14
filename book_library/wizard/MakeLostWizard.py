# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class MakeLostWizard(models.TransientModel):
	_name = 'make.lost.wizard'

	book_id = fields.Many2one('library.book')

	def confirm_make_lost(self):
		self.book_id.state = '2'


class MakePriceWizard(models.TransientModel):
	_name = 'make.price.wizard'

	book_id = fields.Many2one('library.book')
	price = fields.Float()

	def confirm_price(self):
		self.book_id.price = self.price

class MakeNotAvailableWizard(models.TransientModel):
	_name = 'make.not.available.wizard'

	book_ids = fields.Many2many('library.book',string="Books")

	def confirm_not_available(self):
		self.book_ids.state = '0'
