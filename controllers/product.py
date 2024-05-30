import json
from odoo import http  # for using libray http
from odoo.http import request


class ProductApi(http.Controller):  # for inherit http controller
    # methods have 1-GET 2-POST 3-DELETE 4-PUT
    # type have http and json
    # you should make filter database in conf file
    # in postman you write localhost and port and route
    # in postman you write server host and port and route

    @http.route("/v1/product/json", methods=["POST"], type="json", auth="none", csrf=False)
    def post_product_json(self):
        args = request.httprequest.data.decode()  # for get data from api
        vals = json.loads(args)  # for convert data to dict
        res = 0
        if 'accessories' in vals:
            res = request.env['accessories'].sudo().create(vals)
        elif 'electricity' in vals:
            res = request.env['electricity'].sudo().create(vals)
        elif 'internal' in vals:
            res = request.env['internal'].sudo().create(vals)
        elif 'mobiles' in vals:
            res = request.env['mobiles'].sudo().create(vals)
        elif 'petrine_work' in vals:
            res = request.env['petrine_work'].sudo().create(vals)

        if res:
            return {  # return default json response
                "message": "The record has been created.",
                "id": res.id,
                "name": res.name,
            }

    @http.route("/v1/product", methods=["POST"], type="http", auth="none", csrf=False)
    def post_product(self):
        args = request.httprequest.data.decode()  # for get data from api
        vals = json.loads(args)  # for convert data to dict
        if not vals.get("name"):
            return request.make_json_response({
                "message": "The name is be required!",
            }, status=400)
        res = 0
        try:
            if 'accessories' in vals:
                res = request.env['accessories'].sudo().create(vals)
            elif 'electricity' in vals:
                res = request.env['electricity'].sudo().create(vals)
            elif 'internal' in vals:
                res = request.env['internal'].sudo().create(vals)
            elif 'mobiles' in vals:
                res = request.env['mobiles'].sudo().create(vals)
            elif 'petrine_work' in vals:
                res = request.env['petrine_work'].sudo().create(vals)

            if res:
                return request.make_json_response({  # for return json response
                    "message": "The record has been created.",
                    "id": res.id,
                    "name": res.name,
                }, status=200)
            else:
                return request.make_json_response({
                    "message": "You should enter category for product.",
                }, status=400)
        except Exception as error:
            if res:
                return request.make_json_response({
                    "message": "error"
                }, status=400)

    @http.route("/v1/product/accessories/<int:product_id>", methods=["PUT"], type="http", auth="none", csrf=False)
    def update_product(self, product_id):
        try:
            product_id = request.env['accessories'].sudo().search([('id', '=', product_id)])
            if not product_id:
                return request.make_json_response({
                    "message": "ID doesn't exist!",
                }, status=400)
            args = request.httprequest.data.decode()  # for get data from api
            vals = json.loads(args)  # for convert data to dict
            res = product_id.sudo().write(vals)
            return request.make_json_response({
                "message": "The record has been updated successfully.",
                "id": product_id.id,
                "name": product_id.name,
            }, status=200)
        except Exception as error:
            return request.make_json_response({
                "message": "error"
            }, status=400)

    @http.route("/v1/product/accessories/<int:product_id>", methods=["GET"], type="http", auth="none", csrf=False)
    def get_product(self, product_id):
        try:
            product_id = request.env['accessories'].sudo().search([('id', '=', product_id)])
            if not product_id:
                return request.make_json_response({
                    "message": "ID doesn't exist!",
                }, status=400)
            return request.make_json_response({
                "id": product_id.id,
                "ref": product_id.ref,
                "name": product_id.name,
                "accessories": product_id.accessories,
                "price": product_id.price,
                "count": product_id.count,
            }, status=200)
        except Exception as error:
            return request.make_json_response({
                "message": "error"
            }, status=400)

    @http.route("/v1/product/accessories/<int:product_id>", methods=["DELETE"], type="http", auth="none", csrf=False)
    def delete_product(self, product_id):
        try:
            product_id = request.env['accessories'].sudo().search([('id', '=', product_id)])
            if not product_id:
                return request.make_json_response({
                    "message": "ID doesn't exist!",
                }, status=400)
            product_id.unlink()
            return request.make_json_response({
                "message": "The record has been deleted successfully.",
            }, status=200)
        except Exception as error:
            return request.make_json_response({
                "message": "error"
            }, status=400)


