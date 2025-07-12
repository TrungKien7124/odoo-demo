import re
from odoo.http import request

from ..services.field_mapper.base_mapper import BaseMapper
from .serializer.base_serializer import BaseSerializer
from ..utils.error_format import ErrorFormat
from .nomarlizer.base_nomarlizer import BaseNomarlizer
from ..utils.fileHelper import export_file, import_file


class BaseService():
    def __init__(self, modelName, validator):
        self.modelName = modelName
        self.model = request.env[modelName].sudo()
        self.mapper = BaseMapper(modelName)
        self.validator = validator

    def get_all(self, columnlist=None):
        columnlist = self.mapper.get_column_from_alias(
            columnlist, "B")
        data = list(self.model.search([]))
        return BaseSerializer(data, columnlist).serialize_all()

    def get_by_page(self, page, size, order, search=None, columnlist=None, toplist=None):
        """
            Phương thức này xử lý phân trang dữ liệu ở server
            Tham số:
                - page: số trang hiện tại, bắt đầu từ 1
                - size: số lượng bản ghi trên mỗi trang
                - order: chuỗi định dạng sắp xếp
                - search: chuỗi tìm kiếm, nếu có sẽ lọc theo code, name, alias
                - columnlist: danh sách các cột cần lấy dữ liệu, nếu không có sẽ lấy tất cả
                - toplist: danh sách các id của các bản ghi cần lấy ra
            Kiểu trả về:
                - danh sách các bản ghi đã được phân trang và lọc theo các tham số truyền vào
            Ngoại lệ:
                - C601: Lỗi định dạng số trang, nếu page < 1
                - C602: Lỗi định dạng số lượng bản ghi trên mỗi trang, nếu size < 1
                - C607: Lỗi định dạng cột, nếu columnlist không hợp lệ
                - C600: Lỗi định dạng order, nếu order không hợp lệ
        """
        page = int(page)
        size = int(size)

        if (page < 1):
            raise ErrorFormat("C601", "error", "Lỗi định dạng số trang", None)

        if (size < 1):
            raise ErrorFormat(
                "C602", "error", "Lỗi định dạng số lượng trang", None)

        order = self.mapper.get_order_by(order, "C")

        domain = []

        if search:
            domain = ['|', ('code', 'ilike', search), ('name',
                                                       'ilike', search), ('alias', 'ilike', search)]

        columnlist = self.mapper.get_column_from_alias(
            columnlist, "C")

        offset = (page - 1) * size
        limit = size

        top_records = []
        if toplist:
            top_records = self.model.search([('id', 'in', toplist.split(','))])

        total_records = list(self.model.search(
            domain, order=order, limit=limit, offset=offset))

        count_records = len(total_records)

        data = BaseSerializer(top_records + total_records,
                              columnlist).serialize_all()

        return {
            'page_info': {
                'total_items': count_records,
                'toal_pages': (count_records + int(size) - 1) // int(size),
                'current': page,
                'size': size
            },
            'records': data
        }

    def store(self, data):
        """
            Phương thức này để thêm mới một bản ghi mới vào database
            Tham số:
                - data: dictionary chứa dữ liệu, ví dụ: {'code': 'value', 'alias': 'value'}
            Kiểu trả về:
                - id của bản ghi mới
            Ngoại lệ:
                - E603: Lỗi kiểm tra dữ liệu, nếu dữ liệu không hợp lệ
                - E600: Lỗi không xác định
        """

        valid_data = self.mapper.get_column_from_alias(data, "E")

        valid_data = BaseNomarlizer(valid_data).normalize_all()[0]

        validation_errors = self.validator.validate_create_data(valid_data)

        if validation_errors:
            raise ErrorFormat(
                "E603", "error", "Lỗi kiểm tra dữ liệu", validation_errors, valid_data)

        data = self.model.create(valid_data)

        return data.id

    def mass_store(self, data):
        """
            Phương thức này dùng để thêm mới nhiều bản ghi vào database
            Tham số:
                - data: danh sách các dictionary chứa dữ liệu, ví dụ: [{'code': 'value1', 'alias': 'value1'}, {'code': 'value2', 'alias': 'value2'}]
            Kiểu trả về:
                - danh sách các id của các bản ghi mới
            Ngoại lệ:
                - E603: Lỗi kiểm tra dữ liệu, nếu dữ liệu không hợp lệ
                - E600: Lỗi không xác định
        """
        if not data:
            raise ErrorFormat("E603", "error", "Lỗi kiểm tra dữ liệu",
                              "Danh sách dữ liệu không được để trống", None)

        valid_data = [self.mapper.get_column_from_alias(
            item, "E") for item in data]

        validation_errors = []
        for index, item in enumerate(valid_data, start=1):
            errors = self.validator.validate_create_data(item)
            if errors:
                validation_errors.append({f"item {index}": errors})
                self.validator.errors = {}

        if validation_errors:
            raise ErrorFormat(
                "E603", "error", "Lỗi kiểm tra dữ liệu", validation_errors, valid_data)

        valid_data = BaseNomarlizer(valid_data).normalize_all()

        result = self.model.create(valid_data)

        return result.ids

    def get_by_id(self, id, columnlist=None):
        """
            Phương thức này trả về thông tin của một nhà cung cấp theo id
            Tham số:
                - id: id của nhà cung cấp cần lấy thông tin
                - columnlist: danh sách các cột cần lấy dữ liệu, nếu không có sẽ lấy tất cả
            Kiểu trả về:
                - dictionary chứa thông tin của nhà cung cấp đã được chuyển đổi
            Ngoại lệ:
                - D604: Lỗi không tìm thấy bản ghi, nếu không tìm thấy nhà cung cấp
                - D607: Lỗi định dạng cột, nếu columnlist không hợp lệ
        """
        columnlist = self.mapper.get_column_from_alias(
            columnlist, "D")

        data = self.model.browse(id)

        if not data.exists():
            raise ErrorFormat("D604", "error", "Bản ghi không tồn tại")
        return BaseSerializer(data, columnlist).serialize_all()

    def update(self, id, data):
        """
            Phương thức này dùng để update dữ liệu trên database theo id
            Tham số:
                - id: id của nhà cung cấp cần cập nhật
                - data: dictionary chứa dữ liệu cần cập nhật, ví dụ: {'code': 'new_value', 'alias': 'new_value'}
            Kiểu trả về:
                - id của nhà cung cấp đã được cập nhật
            Ngoại lệ:
                - F603: Lỗi kiểm tra dữ liệu, nếu dữ liệu không hợp lệ
                - F604: Lỗi không tìm thấy bản ghi, nếu không tìm thấy nhà cung cấp
                - F605: Lỗi vi phạm khóa ngoại, nếu có liên kết khóa ngoại
                - F600: Lỗi không xác định, nếu có lỗi không xác định xảy ra
        """
        valid_data = self.mapper.get_column_from_alias(data, "F")

        validation_errors = self.validator.validate_update_data(valid_data)

        if validation_errors:
            raise ErrorFormat(
                "F603", "error", "Lỗi kiểm tra dữ liệu", validation_errors, valid_data)

        data = self.model.browse(id)

        if not data.exists():
            raise ErrorFormat("F604", "error", "Bản ghi không tồn tại")

        try:
            data.write(valid_data)
        except Exception as e:
            raise ErrorFormat("F600", "error", "Lỗi không xác định", str(e))

        return data.id

    def delete(self, id):
        """
            Phương thức này dùng để xóa một bản ghi theo id
            Tham số:
                - id: id của bản ghi cần xóa
            Kiểu trả về:
                - id của bản ghi đã được xóa
            Ngoại lệ:
                - G604: Lỗi không tìm thấy bản ghi, nếu không tìm thấy nhà cung cấp
                - G605: Lỗi vi phạm khóa ngoại, nếu có liên kết khóa ngoại
                - G600: Lỗi không xác định, nếu có lỗi không xác định xảy ra
        """
        data = self.model.browse(id)

        if not data.exists():
            raise ErrorFormat("G604", "error", "Bản ghi không tồn tại")

        try:
            data.unlink()
        except Exception as e:
            raise ErrorFormat("G600", "error", "Lỗi không xác định", str(e))

        return data.id

    def copy(self, id):
        """
            Phương thức này dùng để sao chép một bản ghi theo id
            Tham số:
                - id: id của bản ghi cần sao chép
            Kiểu trả về:
                - id của bản ghi đã được sao chép
            Ngoại lệ:
                - H604: Lỗi không tìm thấy bản ghi, nếu không tìm thấy nhà cung cấp
                - H600: Lỗi không xác định, nếu có lỗi không xác định xảy ra
        """
        data = self.model.browse(id)

        if not data.exists():
            raise ErrorFormat("H604", "error", "Bản ghi không tồn tại")

        max_id = self.model.search([], order='id desc', limit=1 or 0)
        new_id = max_id.id + 1
        old_code = data.code

        match = re.match(r"^(.*)\s\(\d+\)$", old_code)
        if match:
            base_code = match.group(1)
        else:
            base_code = old_code

        base_code = f"{base_code} ({new_id})"

        new_data = data.copy(default={'code': base_code})

        return new_data.id

    def mass_copy(self, idlist):
        """
            Phương thức này dùng để sao chép nhiều bản ghi theo id
            Tham số:
                - idlist: danh sách các id của bản ghi cần sao chép, ví dụ: [1, 2, 3]
            Kiểu trả về:
                - danh sách các id của bản ghi đã được sao chép
            Ngoại lệ:
                - H600: Lỗi không xác định, nếu có lỗi không xác định xảy ra
        """
        if not idlist:
            raise ErrorFormat("H603", "Error", "Lỗi kiểm tra dữ liệu",
                              "Danh sach id không được để trống", None)

        idlist = list(map(int, idlist.split(',')))

        data = list(self.model.browse(idlist))
        if len(data) != len(idlist):
            raise ErrorFormat(
                "H604", "error", "Danh sách chứa id không tồn tại")

        new_ids = []
        for id in idlist:
            new_id = self.copy(id)
            new_ids.append(new_id)

        return new_ids

    def mass_delete(self, idlist):
        """
            Phương thức này dùng để xóa nhiều bản ghi theo id
            Tham số:
                - idlist: danh sách các id của bản ghi cần xóa, ví dụ: [1, 2, 3]
            Kiểu trả về:
                - danh sách các id của bản ghi đã được xóa
            Ngoại lệ:
                - G600: Lỗi không xác định, nếu có lỗi không xác định xảy ra
        """
        if not idlist:
            raise ErrorFormat("G603", "Error", "Lỗi kiểm tra dữ liệu",
                              "Danh sach id không được để trống", None)

        idlist = list(map(int, idlist.split(',')))

        data = list(self.model.browse(idlist))
        if len(data) != len(idlist):
            raise ErrorFormat(
                "G604", "error", "Danh sách chứa id không tồn tại")

        deleted_ids = []
        for id in idlist:
            deleted_ids.append(self.delete(id))

        return deleted_ids

    def export_by_id(self, id, columnlist=None, file_type='xlsx'):
        """
            Phương thức này dùng để xuất dữ liệu của một bản ghi theo id
            Tham số:
                - id: id của bản ghi cần xuất
                - columnlist: danh sách các cột cần lấy dữ liệu, nếu không có sẽ lấy tất cả
            Kiểu trả về:
                - file chứa dữ liệu đã được xuất
            Ngoại lệ:
                - K604: Lỗi không tìm thấy bản ghi, nếu không tìm thấy nhà cung cấp
                - K607: Lỗi định dạng cột, nếu columnlist không hợp lệ
        """
        data = self.get_by_id(id, columnlist)

        data = self.mapper.get_label_from_column(data, "K")

        return export_file([data], self.modelName, file_type)

    def mass_export(self, idlist=None, columnlist=None, file_type='csv'):
        """
            Phương thức này dùng để xuất dữ liệu của nhiều bản ghi theo id
            Tham số:
                - idlist: danh sách các id của bản ghi cần xuất, nếu không có sẽ lấy tất cả
                - columnlist: danh sách các cột cần lấy dữ liệu, nếu không có sẽ lấy tất cả
            Kiểu trả về:
                - file chứa dữ liệu đã được xuất
            Ngoại lệ:
                - L600: Lỗi không xác định, nếu có lỗi không xác định xảy ra
        """
        if not idlist:
            raise ErrorFormat("L603", "Error", "Lỗi kiểm tra dữ liệu",
                              "Danh sach id không được để trống", None)

        idlist = list(map(int, idlist.split(',')))

        columnlist = self.mapper.get_column_from_alias(
            columnlist, "L")

        data = list(self.model.browse(idlist))

        if len(data) != len(idlist):
            raise ErrorFormat(
                "L604", "error", "Danh sách chứa id không tồn tại")

        data = BaseSerializer(data, columnlist).serialize_all()

        data = [self.mapper.get_label_from_column(item, "L") for item in data]

        return export_file(data, self.modelName, file_type)

    def import_data(self, attachment):
        """
            Phương thức này dùng để nhập dữ liệu từ file
            Tham số:
                - attachment: tệp đính kèm chứa dữ liệu cần nhập
            Kiểu trả về:
                - danh sách các id của bản ghi đã được nhập
            Ngoại lệ:
                - J600: Lỗi không xác định, nếu có lỗi không xác định xảy ra
        """
        data = import_file(attachment)

        if not data:
            raise ErrorFormat("J604", "error", "Tệp không chứa dữ liệu")

        data = [self.mapper.get_column_from_alias(item, "J") for item in data]

        data = BaseNomarlizer(data).normalize_all()

        validation_errors = []

        for index, item in enumerate(data, start=1):
            errors = self.validator.validate_create_data(item)
            if errors:
                validation_errors.append({f"line{index}": errors})

        if validation_errors:
            raise ErrorFormat(
                "J603", "Error", "Lỗi kiểm tra dữ liệu", validation_errors, data)

        data = self.model.create(data)

        return data.ids
