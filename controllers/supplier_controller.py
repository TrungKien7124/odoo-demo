# -*- coding: utf-8 -*-
import json
from odoo import http
from psycopg2 import errors
from psycopg2 import IntegrityError
from odoo.http import request

# local package
from ..services.supplier_service import SupplierService
from ..utils.error_format import ErrorFormat
from ..utils.response_format import get_response


class SupplierController(http.Controller):
    """
    Controller điều phối request đến service tương ứng
    - Danh sách các thuộc tính:

    - Các thương thức:
        + get_all: Lấy tất cả nhà cung cấp
        + get_by_page: Lấy nhà cung cấp theo trang
        + store: Thêm mới nhà cung cấp
        + get_by_id: Lấy nhà cung cấp theo id
        + update: Cập nhật nhà cung cấp theo id
        + delete: Xóa nhà cung cấp theo id
        + copy: Sao chép nhà cung cấp theo id
        + mass_copy: Sao chép nhiều nhà cung cấp
        + mass_delete: Xóa nhiều nhà cung cấp
        + export_by_id: Xuất nhà cung cấp theo id
        + mass_export: Xuất nhiều nhà cung cấp
        + import_data: Nhập dữ liệu nhà cung cấp từ
    """

    @http.route('/api/nagaco_supplier', type='http', auth='public', methods=['GET'], csrf=False)
    def get_all(self, **data):
        try:
            columnlist = data.get('columnlist', None)

            return get_response(SupplierService().get_all(columnlist))

        except ErrorFormat as e:
            return e.get_response()

        except Exception as e:
            return ErrorFormat("B600", "error", "Thất bại", str(e), None).get_response()

    @http.route('/api/nagaco_supplier/page/<int:page>', type='http', auth='public', methods=['GET'], csrf=False)
    def get_by_page(self, page, **data):
        try:
            size = data.get("size") or 10
            order = data.get("order") or "id:0"
            search = data.get("search")
            columnlist = data.get("columnlist")
            toplist = data.get("toplist")

            result = SupplierService().get_by_page(
                page, size, order, search, columnlist, toplist)
            return get_response(result)
        except ErrorFormat as e:
            return e.get_response()
        except Exception as e:
            return ErrorFormat("C600", "Error", str(e), None).get_response()

    @http.route('/api/nagaco_supplier', type='http', auth='public', methods=['POST'], csrf=False)
    def store(self, **data):
        try:
            result = SupplierService().store(data)
            return get_response(result)

        except ErrorFormat as e:
            return e.get_response()
        except Exception as e:
            if 'duplicate key value' in str(e) and 'supplier_code_unique' in str(e):
                return ErrorFormat(
                    "E603", "Error", "Lỗi kiểm tra dữ liệu.", {'code': 'Trường này không được trùng nhau'}).get_response()
            return ErrorFormat("E600", "error", "Lỗi không xác định", str(e)).get_response()

    @http.route('/api/nagaco_supplier/<int:id>', type='http', auth='public', methods=['GET'], csrf=False)
    def get_by_id(self, id, **data):
        try:
            columnlist = data.get("columnlist")
            result = SupplierService().get_by_id(id, columnlist)
            return get_response(result)
        except ErrorFormat as e:
            return e.get_response()
        except Exception as e:
            return ErrorFormat("D600", "error", "Lỗi không xác định", str(e), None).get_response()

    @http.route('/api/nagaco_supplier/<int:id>', type='http', auth='public', methods=['PUT'], csrf=False)
    def update(self, id, **data):
        try:
            result = SupplierService().update(id, data)
            return get_response(result)
        except ErrorFormat as e:
            return e.get_response()
        except Exception as e:
            if 'duplicate key value' in str(e) and 'supplier_code_unique' in str(e):
                return ErrorFormat(
                    "F603", "Error", "Lỗi kiểm tra dữ liệu.", {'code': 'Trường này không được trùng nhau'}).get_response()
            return ErrorFormat("F600", "Error", "Lỗi không xác định", str(e)).get_response()

    @http.route('/api/nagaco_supplier/<int:id>', type='http', auth='public', methods=['DELETE'], csrf=False)
    def delete(self, id):
        try:
            result = SupplierService().delete(id)
            return get_response(result)
        except ErrorFormat as e:
            return e.get_response()
        except Exception as e:
            return ErrorFormat("G600", "Error", "Lỗi không xác định", str(e)).get_response()

    @http.route('/api/nagaco_supplier/copy/<int:id>', type='http', auth='public', methods=['POST'], csrf=False)
    def copy(self, id):
        try:
            result = SupplierService().copy(id)
            return get_response(result)
        except ErrorFormat as e:
            return e.get_response()
        except Exception as e:
            return ErrorFormat("H600", "Error", "Lỗi không xác định", str(e)).get_response()

    @http.route('/api/nagaco_supplier/copy', type='http', auth='public', methods=['POST'], csrf=False)
    def mass_copy(self, **data):
        try:
            idlist = data.get('idlist', None)
            result = SupplierService().mass_copy(idlist)
            return get_response(result)
        except ErrorFormat as e:
            return e.get_response()
        except Exception as e:
            return ErrorFormat("H600", "Error", "Lỗi không xác định", str(e)).get_response()

    @http.route('/api/nagaco_supplier/delete', type='http', auth='public', methods=['DELETE'], csrf=False)
    def mass_deletstoree(self, **data):
        try:
            idlist = data.get('idlist', None)
            result = SupplierService().mass_delete(idlist)
            return get_response(result)
        except ErrorFormat as e:
            return e.get_response()
        except Exception as e:
            return ErrorFormat("G600", "Error", "Lỗi không xác định", str(e)).get_response()

    @http.route('/api/nagaco_supplier/export/<int:id>', type='http', auth='public', methods=['GET'], csrf=False)
    def export_by_id(self, id, **data):
        try:
            columnlist = data.get('columnlist', None)
            return SupplierService().export_by_id(id, columnlist)
        except ErrorFormat as e:
            return e.get_response()
        except Exception as e:
            return ErrorFormat("K600", "Error", "Lỗi không xác định", str(e)).get_response()

    @http.route('/api/nagaco_supplier/export', type='http', auth='public', methods=['GET'], csrf=False)
    def mass_export(self, **data):
        try:
            idlist = data.get('idlist', None)
            columnlist = data.get('columnlist', None)
            file_type = data.get('file_type', 'csv')
            return SupplierService().mass_export(idlist, columnlist, file_type)
        except ErrorFormat as e:
            return e.get_response()
        except Exception as e:
            return ErrorFormat("L600", "Error", "Lỗi không xác định", str(e)).get_response()

    @http.route('/api/nagaco_supplier/import', type='http', auth='public', methods=['POST'], csrf=False)
    def import_data(self, **data):
        try:
            attachment = data.get('attachment', None)
            if not attachment:
                return ErrorFormat("J604", "Error", "Lỗi tệp chưa được tải lên", None).get_response()
            return get_response(SupplierService().import_data(attachment))

        except ErrorFormat as e:
            return e.get_response()

        except Exception as e:
            if 'duplicate key value' in str(e) and 'supplier_code_unique' in str(e):
                return ErrorFormat(
                    "J603", "Error", "Lỗi kiểm tra dữ liệu.", {'code': 'Trường này không được trùng nhau'}).get_response()

            return ErrorFormat("J600", "Error", "Lỗi không xác định", str(e)).get_response()

    @http.route('/api/nagaco_supplier/store', type='http', auth='public', methods=['POST'], csrf=False)
    def mass_create(self, **data):
        try:

            data = json.loads(request.httprequest.data)

            data = data.get('data', [])

            return get_response(SupplierService().mass_store(data))

        except ErrorFormat as e:
            return e.get_response()

        except Exception as e:
            if 'duplicate key value' in str(e) and 'supplier_code_unique' in str(e):
                return ErrorFormat(
                    "I603", "Error", "Lỗi kiểm tra dữ liệu.", {'code': 'Trường này không được trùng nhau'}).get_response()

            return ErrorFormat("L600", "Error", "Lỗi không xác định", str(e)).get_response()
