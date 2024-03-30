# -*- coding: utf-8 -*-
# from odoo import http


# class ShopPhone(http.Controller):
#     @http.route('/shop_phone/shop_phone', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/shop_phone/shop_phone/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('shop_phone.listing', {
#             'root': '/shop_phone/shop_phone',
#             'objects': http.request.env['shop_phone.shop_phone'].search([]),
#         })

#     @http.route('/shop_phone/shop_phone/objects/<model("shop_phone.shop_phone"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('shop_phone.object', {
#             'object': obj
#         })

