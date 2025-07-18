# -*- coding: utf-8 -*-
import json
from odoo import http
from psycopg2 import errors
from psycopg2 import IntegrityError
from odoo.http import request

# local package
from ..controllers.supplier_controller import SupplierController
from ..middlewares.verify_token import verify_token
from ..helper.response_format import responseFormat


class SupplierRoute(http.Controller):
    @http.route("/api/nagaco_supplier", type="http", auth="public", methods=["GET"], csrf=False)
    @verify_token
    def get_all(self, **kw):
        user_role = request.user_role
        if user_role == 'admin':
            return SupplierController().get_all(kw)
        else:
            return responseFormat(403, "Khong co quyen truy cap")

    @http.route("/api/nagaco_supplier/page/<int:page>", type="http", auth="public", methods=["GET"], csrf=False)
    def get_by_page(self, page, **kw):
        return SupplierController().get_by_page(page, kw)

    @http.route("/api/nagaco_supplier", type="http", auth="public", methods=["POST"], csrf=False)
    def store(self):
        return SupplierController().store()

    @http.route("/api/nagaco_supplier/<int:id>", type="http", auth="public", methods=["GET"], csrf=False)
    def get_by_id(self, id, **kw):
        return SupplierController().get_by_id(id, kw)

    @http.route("/api/nagaco_supplier/<int:id>", type="http", auth="public", methods=["PUT"], csrf=False)
    def update(self, id):
        return SupplierController().update(id)

    @http.route("/api/nagaco_supplier/<int:id>", type="http", auth="public", methods=["DELETE"], csrf=False)
    def delete(self, id):
        return SupplierController().delete(id)

    @http.route("/api/nagaco_supplier/copy/<int:id>", type="http", auth="public", methods=["POST"], csrf=False)
    def copy(self, id):
        return SupplierController().copy(id)

    @http.route("/api/nagaco_supplier/copy", type="http", auth="public", methods=["POST"], csrf=False,)
    def mass_copy(self, **kw):
        return SupplierController().mass_copy(kw)

    @http.route("/api/nagaco_supplier/delete", type="http", auth="public", methods=["DELETE"], csrf=False)
    def mass_delete(self, **kw):
        return SupplierController().mass_delete(kw)

    @http.route("/api/nagaco_supplier/export/<int:id>", type="http", auth="public", methods=["GET"], csrf=False)
    def export_by_id(self, id, **kw):
        return SupplierController().export_by_id(id, kw)

    @http.route("/api/nagaco_supplier/export", type="http", auth="public", methods=["GET"], csrf=False)
    def mass_export(self, **kw):
        return SupplierController().mass_export(kw)

    @http.route("/api/nagaco_supplier/import", type="http", auth="public", methods=["POST"], csrf=False)
    def import_data(self, **kw):
        return SupplierController().import_data(kw)
