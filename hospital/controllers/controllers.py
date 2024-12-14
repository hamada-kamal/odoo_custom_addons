# -*- coding: utf-8 -*-
# from odoo import http


# class Hospital(http.Controller):
#     @http.route('/hospital/hospital', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hospital/hospital/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('hospital.listing', {
#             'root': '/hospital/hospital',
#             'objects': http.request.env['hospital.hospital'].search([]),
#         })

#     @http.route('/hospital/hospital/objects/<model("hospital.hospital"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hospital.object', {
#             'object': obj
#         })
