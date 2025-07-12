class BaseValidator:
    """
    Khởi tạo bộ Validator tổng quát
    - Danh sách các thuộc tính:
        +data: dictionary chứa dữ liệu cần kiểm tra
    - Các quy tắc kiểm tra:
        - required: Kiểm tra trường bắt buộc
        - max_length: Kiểm tra độ dài tối đa của trường
        - email: Kiểm tra định dạng email
        - url: Kiểm tra định dạng URL
        - number: Kiểm tra định dạng số
        - add_error: Thêm lỗi vào danh sách lỗi
        - errors: Lưu trữ các lỗi đã xảy ra trong quá trình kiểm tra
    """

    def __init__(self, data=None):
        self.data = data
        self.errors = {}

    def required(self, field):
        value = self.data.get(field)
        if not value:
            self.add_error(field, "Trường này bắt buộc phải có")

    def max_length(self, field, max_len):
        value = self.data.get(field)
        if value and len(str(value).strip()) > max_len:
            self.add_error(
                field, f"Trường này có dộ dài lớn hơn độ dài cho phép là {max_len}")

    def email(self, field):
        import re
        value = self.data.get(field, '')
        pattern = r"[^@]+@[^@]+\.[^@]+"
        if value and not re.match(pattern, value):
            self.add_error(field, "Trường này không đúng định dạng email")

    def url(self, field):
        import re
        value = self.data.get(field, '')
        pattern = r'^(https?|ftp)://[^\s/$.?#].[^\s]*$'
        if value and not re.match(pattern, value):
            self.add_error(field, "Trường này không đúng định dạng URL")

    def number(self, field):
        import re
        value = self.data.get(field, '')
        pattern = r'^\d+(\.\d+)?$'
        if value and not re.match(pattern, value):
            self.add_error(field, "Trường này không đúng định dạng số")

    def add_error(self, field, message):
        if field not in self.errors:
            self.errors[field] = []
        self.errors[field].append(message)
