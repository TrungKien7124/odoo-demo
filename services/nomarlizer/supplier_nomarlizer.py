from .base_nomarlizer import BaseNomarlizer


class SupplierNomarlizer(BaseNomarlizer):
    """
    Class chuyển đổi kiểu dữ liệu từ dictionary sang định dạng chuẩn của model
    - Danh sách các thuộc tính:
        + data: dữ liệu cần chuyển đổi
    - Các phương thức:
        + normalize_data: Chuyển đổi dữ liệu thành định dạng chuẩn
    """

    def __init__(self, data):
        super().__init__(data)

    def normalize_1_item(self, item):
        result = {}
        for field, value in item.items():
            if isinstance(value, str):
                value = self.normalize_string(value)
            result[field] = value
        return result

    def normalize_all(self):
        if not isinstance(self.data, list):
            self.data = [self.data]
        return [self.normalize_1_item(item) for item in self.data]
