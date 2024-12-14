# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class book(models.Model):
	_name = 'library.book'
	_description = 'Represents books information'
	_order = 'name desc, short_name'



	def _get_default_company(self):
		return self.env.user.company_id.id

	name = fields.Char(string="ITSS Name", required=True, copy=False, translate=True)
	short_name = fields.Char()
	long_description = fields.Text()
	state = fields.Selection([('0', 'Not Available'),
								('1', 'Available'),
								('2', 'Lost')],
								default='0',string='State', readonly=False, help="This field will Show you the book status")
	description = fields.Html('Description', states={'0': [('invisible', True)], '1': [('readonly', True)]})
	cover = fields.Binary('Book Cover')
	out_of_print = fields.Boolean('Out of Print?')
	date_release = fields.Date('Release Date')
	date_updated = fields.Datetime('Last Updated')
	pages = fields.Integer('Number of Pages', default=3)
	reader_rating = fields.Float('Reader Average Rating', digits=(14, 2)) # Optional precision decimals)

	price = fields.Monetary('Book Price', digits=(14, 2), currency_field='currency_id') # Optional precision decimals)
	company_id = fields.Many2one('res.company', default=_get_default_company)
	currency_id = fields.Many2one('res.currency', related='company_id.currency_id')
	# Relational Fields
	shelf_id = fields.Many2one('library.shelf')
	author_ids = fields.Many2many('library.author','book_author_rel','book_id','author_id','Authors')

	context_field = fields.Boolean(default=False)



	# Helpers fields
	shelf_description = fields.Char(related='shelf_id.description')


	def mybutton(self):
		raise ValidationError("Hello Ezz")

	def show_my_authors(self):
		if self.author_ids:
			if len(self.author_ids) == 1:
				return{
					'name': ('My Authors'),
		            'view_mode': 'form',
		            'res_model': 'library.author',
		            'res_id': self.author_ids.ids[0],
		            'type': 'ir.actions.act_window',
				}
			elif len(self.author_ids) > 1:
				return{

					'name': ('My Authors'),
		            'view_mode': 'tree,form',
		            'res_model': 'library.author',
		            'domain': [('id', 'in', self.author_ids.ids)],
		            'type': 'ir.actions.act_window',
				}
		else:
			raise ValidationError(" There is no authors")
		# action = self.env.ref('book_library.actions_author')
		# action1 = self.env['ir.actions.actions']._for_xml_id('book_library.actions_author')
		# print("Action = ", action)
		# print("Action 1= ", action1)
		return action1


	def make_available(self):
		if not self.out_of_print:
			self.state = '1'
		else:
			raise ValidationError(" There are no prints of this current book.")


	def actions_author_by_book(self):
		return{
		'name': 'Authors',
		'type': 'ir.actions.act_window',
		'view_mode': 'tree,form',
		'res_model': 'library.author',
		'domain': [('id','in',self.author_ids.ids)]
		}


	def open_make_lost(self):
		return {
			'name':'Book Lost Confirmation',
			'type':'ir.actions.act_window',
			'view_mode': 'form',
			'res_model': 'make.lost.wizard',
			'target': 'new',
			'context': {'default_book_id': self.id}
		}


	def open_make_price(self):
		return {
			'name':'Set Book Price',
			'type':'ir.actions.act_window',
			'view_mode': 'form',
			'res_model': 'make.price.wizard',
			'target': 'new',
			'context': {'default_book_id': self.id}
		}

class shelf(models.Model):
	_name = 'library.shelf'
	_description = 'Represents shelf information'
	# _order = 'name desc, description'
	# _rec_name = 'description'


	name = fields.Char()
	description = fields.Char()
	book_ids = fields.One2many('library.book', 'shelf_id',context={'default_context_field':True}, domain="['|',('out_of_print','=',False),('long_description','!=',False)]")
	no_of_books = fields.Integer('Total Books', compute='_compute_books', store=True)


	@api.depends('book_ids')
	def _compute_books(self):
		self.no_of_books = len(self.book_ids)


	def open_make_not_available(self):
		our_books = self.book_ids.filtered(lambda x: x.state != '0')
		return {
			'name': 'Select books to make un-available',
			'type': 'ir.actions.act_window',
			'res_model': 'make.not.available.wizard',
			'view_mode': 'form',
			'target': 'new',
			'context': {'default_book_ids': our_books.ids}
		}


class Author(models.Model):
	_name = 'library.author'
	_description = 'Represents author information'

	name = fields.Char()
	book_ids = fields.Many2many('library.book','book_author_rel','author_id','book_id','Books')

class BookCategory(models.Model):
	_name = 'library.book.category'
	_parent_store = True
	_parent_name = "parent_id"

	name = fields.Char(default="/")
	parent_id = fields.Many2one('library.book.category')
	child_ids = fields.One2many('library.book.category','parent_id')
	parent_path = fields.Char(index=True)



	@api.constrains('parent_id')
	def _check_hierarchy(self):
		if not self._check_recursion():
			raise ValidationError('Error! You cannot create recursive categories.')


