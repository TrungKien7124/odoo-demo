import re
from odoo.http import request
import json

from ..helper.fileHelper import export_file, import_file
from ..helper.normalizer import Normalizer
from ..helper.response_format import responseFormat
from ..helper.serializer import Serializer


class BaseController():
    def __init__(self, modelName, validator):
        self.modelName = modelName
        self.model = request.env[modelName].sudo()
        self.validator = validator

    def get_all(self, kw):
        try:
            columnlist = kw.get("columnlist", "")
            errorMessage, columnlist = Normalizer.getColumnFromAlias(columnlist, self.modelAlias2Fields)
            if errorMessage:
                return responseFormat(code="B607", message=errorMessage)
            data = list(self.model.search([]))

            data = Serializer.serialize(data, columnlist, self.modelFields2Labels)

            return responseFormat(code=200, data=data)
        
        except Exception as e:
            return responseFormat(code="B600", message=str(e))

    def get_by_page(self, page, kw):
        """
            Phương thức này xử lý phân trang dữ liệu ở server
            Tham số:
                - kw
            Kiểu trả về:
                - danh sách các bản ghi đã được phân trang và lọc theo các tham số truyền vào
            Ngoại lệ:
                - C601: Lỗi định dạng số trang, nếu page < 1
                - C602: Lỗi định dạng số lượng bản ghi trên mỗi trang, nếu size < 1
                - C607: Lỗi định dạng cột, nếu columnlist không hợp lệ
                - C600: Lỗi định dạng order, nếu order không hợp lệ
        """
        try:
            page = int(page)
            size = int(kw.get('size', 10))

            if (page < 1):
                return responseFormat(code="C601", message="Loi dinh dang so trang")

            if (size < 1):
                return responseFormat(code="C602", message="Loi dinh dang co trang")
            
            order = kw.get('order', None)

            errMessgae, order = Normalizer.getOrderString(order, self.modelAlias2Fields)
            if errMessgae:
                return responseFormat(code="C607", message=errMessgae)

            domain = []

            search = kw.get('search', None)

            if search:
                domain = ['|', ('code', 'ilike', search), ('name',
                                                        'ilike', search), ('alias', 'ilike', search)]

            columnlist = kw.get('columnlist', None)
            errMessage, columnlist = Normalizer.getColumnFromAlias(columnlist, self.modelAlias2Fields)
            if errMessage:
                return responseFormat(code="C607", message=errMessage)

            offset = (page - 1) * size
            limit = size

            top_records = []

            toplist = kw.get('toplist', None)

            if toplist:
                top_records = list(self.model.search([('id', 'in', toplist.split(','))]))

            total_records = list(self.model.search(
                domain, order=order, limit=limit, offset=offset))
            

            count_records = len(total_records)

            data = Serializer.serialize(top_records + total_records, columnlist, self.modelFields2Labels)

            result =  {
                'page_info': {
                    'total_items': count_records,
                    'toal_pages': (count_records + int(size) - 1) // int(size),
                    'current': page,
                    'size': size
                },
                'records': data
            }

            return responseFormat(code = 200, data = result)
        except Exception as e:
            return responseFormat("C600", str(e))

    def store(self):
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
        try:
            data = json.loads(request.httprequest.data)

            errMessage, data = Normalizer.getModelFromJsonData(data, self.fieldList)

            if errMessage:
                return responseFormat(code = "E607", message=errMessage)

            validation_errors = {}

            index = 1
            
            uniqueValue = {}

            # kiem tra tat ca cac item trong data
            for item in list(data):
                errors = self.validator.validate_create_data(item)

                for field, value in item.items():
                    if field in self.uniqueFields:
                        exist = self.model.search([(field, '=', value)])

                        if field not in uniqueValue:
                            uniqueValue[field] = []

                        # Neu trung gia tri trong database hoac trung voi nhung gia tri khac trong mang data thi them loi vao mang
                        if exist or value in uniqueValue[field]:
                            self.validator.add_error(field, "Truong nay khong duoc trung nhau")
                        else:
                            # Them gia tri cua item vao mang de kiem tra voi cac item sau
                            uniqueValue[field].append(value)
                            
                    if field in self.foreignFields.keys():
                        if not request.env[self.foreignFields[field]].browse(int(value)).exists():
                            self.validator.add_error(field, "Khoa ngoai khong ton tai")
                
                if errors:
                    validation_errors[index] = errors
                
                index += 1
                self.validator.clear_errors()

            if validation_errors:
                return responseFormat(code="E603", message="Loi kiem tra du lieu", data=validation_errors, oldData=data)

            result = self.model.create(data)

            return responseFormat(code=200, data=result.ids)
        except Exception as e:
            return responseFormat(code="E600", message=str(e))

    def get_by_id(self, id, kw):
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
        try:
            columnlist = kw.get('columnlist', None)

            errMessage, columnlist = Normalizer.getColumnFromAlias(columnlist, self.modelAlias2Fields)

            if errMessage:
                return responseFormat(code="D607", message=errMessage)

            data = self.model.browse(id)

            if not data.exists():
                return responseFormat("D604", message="Ban ghi khong ton tai", oldData=id)
            
            data = Serializer.serialize(data, columnlist, self.modelFields2Labels)

            return responseFormat(code=200, data=data)
        except Exception as e:
            return responseFormat(code="D600", message=str(e))

    def update(self, id):
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
        try:
            data = json.loads(request.httprequest.data)

            errMessage, validData = Normalizer.getModelFromJsonData(data, self.fieldList)

            if errMessage:
                return responseFormat(code = "F607", message=errMessage, oldData=data)

            validation_errors = self.validator.validate_update_data(validData)

            if validation_errors:
                return responseFormat(code="F603", message="Loi kiem tra du lieu", data=validation_errors, oldData=validData)

            result = self.model.browse(id)

            if not result.exists():
                return responseFormat("F604", message="Ban ghi khong ton tai")

            result.write(validData)

            return responseFormat(code=200, data=id)
        except Exception as e:
            return responseFormat(code="E600", message=str(e))

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
        try:
            data = self.model.browse(id)

            if not data.exists():
                return responseFormat("G604", message="Ban ghi khong ton tai")

            is_deleted = False

            try:
                data.unlink()
                is_deleted = True
            except:
                is_deleted = False
            
            if is_deleted == False:
                return responseFormat("G603", message="Ban ghi co lien ket khoa ngoai")

            return responseFormat(code=200, data=id)
        except Exception as e:
            return responseFormat(code="G600", message=str(e))

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
        try:
            data = self.model.browse(id)

            if not data.exists():
                return responseFormat("H604", message="Ban ghi khong ton tai")

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

            return responseFormat(code=200, data=new_data.ids)
        except Exception as e:
            return responseFormat(code="H600", message=str(e))

    def mass_copy(self, kw):
        """
            Phương thức này dùng để sao chép nhiều bản ghi theo id
            Tham số:
                - idlist: danh sách các id của bản ghi cần sao chép, ví dụ: [1, 2, 3]
            Kiểu trả về:
                - danh sách các id của bản ghi đã được sao chép
            Ngoại lệ:
                - H600: Lỗi không xác định, nếu có lỗi không xác định xảy ra
        """
        try:
            idlist = kw.get('idlist', None)
            if not idlist:
                return responseFormat("H604", message="Danh sach id khong duoc de trong")

            idlist = list(map(int, idlist.split(',')))

            data = list(self.model.browse(idlist))
            if len(data) != len(idlist):
                return responseFormat("H604", message="Danh sach chua ban ghi khong ton tai")

            new_ids = []
            for id in idlist:

                data = self.model.browse(id)

                max_id = self.model.search([], order='id desc', limit=1 or 0)
                new_id = max_id.id + 1
                old_code = data.code

                match = re.match(r"^(.*)\s\(\d+\)$", old_code)
                if match:
                    base_code = match.group(1)
                else:
                    base_code = old_code

                base_code = f"{base_code} ({new_id})"

                new_id = data.copy(default={'code': base_code}).ids
                new_ids.append(new_id)

            return responseFormat(200, data=new_ids)
        except Exception as e:
            return responseFormat("H600", message=str(e))

    def mass_delete(self, kw):
        """
            Phương thức này dùng để xóa nhiều bản ghi theo id
            Tham số:
                - idlist: danh sách các id của bản ghi cần xóa, ví dụ: [1, 2, 3]
            Kiểu trả về:
                - danh sách các id của bản ghi đã được xóa
            Ngoại lệ:
                - G600: Lỗi không xác định, nếu có lỗi không xác định xảy ra
        """
        try:
            idlist = kw.get('idlist', None)
            if not idlist:
                return responseFormat("G603", message="Danh sach id khong duoc de trong")

            idlist = list(map(int, idlist.split(',')))

            data = list(self.model.browse(idlist))
            for item in data:
                if not item.exists():
                    return responseFormat("G604", message="Danh sach chua id khong ton tai")
            for item in data:
                item.unlink()

            return responseFormat(200, data=idlist)
        except Exception as e:
            return responseFormat("G600", message=str(e))

    def export_by_id(self, id, kw):
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
        try:
            columnlist = kw.get("columnlist", None)

            errMessage, columnlist = Normalizer.getColumnFromAlias(columnlist, self.modelAlias2Fields)
            if errMessage:
                return responseFormat("K607", message=errMessage)

            file_type = kw.get("file_type", 'csv')

            data = self.model.browse(id)
            if not data.exists():
                return responseFormat("K604", message="Ban ghi khong ton tai")

            data = Serializer.serialize(data, columnlist, self.modelFields2Labels, True)

            return export_file([data], self.modelName, file_type)
        except Exception as e:
            return responseFormat("K600", message=str(e))

    def mass_export(self, kw):
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
        try:
            idlist = kw.get("idlist", None)
            if not idlist:
                return responseFormat("L604", "Danh sach ban ghi khong hop le")

            idlist = list(map(int, idlist.split(',')))

            columnlist = kw.get("columnlist", None)
            errMessage, columnlist = Normalizer.getColumnFromAlias(columnlist, self.modelAlias2Fields)
            if errMessage:
                return responseFormat("L607", message=errMessage)

            data = list(self.model.browse(idlist))

            if len(data) != len(idlist):
                return responseFormat("L604", "Danh sach chua ban ghi khong ton tai")

            data = Serializer.serialize(data, columnlist, self.modelFields2Labels, True)

            file_type = kw.get("file_type", "csv")

            return export_file(data, self.modelName, file_type)
        except Exception as e:
            return responseFormat("L600", message=str(e))

    def import_data(self, kw):
        """
            Phương thức này dùng để nhập dữ liệu từ file
            Tham số:
                - attachment: tệp đính kèm chứa dữ liệu cần nhập
            Kiểu trả về:
                - danh sách các id của bản ghi đã được nhập
            Ngoại lệ:
                - J600: Lỗi không xác định, nếu có lỗi không xác định xảy ra
        """
        try: 
            attachment = kw.get("attachment", None)

            if not attachment:
                return responseFormat("J604", "Tai tep du lieu khong thanh cong")

            data = import_file(attachment)

            if not data:
                return responseFormat("J604", "Khong the doc tep du lieu")
            
            errMessage, data = Normalizer.getModelDataFromLabels(data, self.modelFields2Labels)

            return responseFormat(200, data = data)
        except Exception as e:
            return responseFormat("J600", str(e))
