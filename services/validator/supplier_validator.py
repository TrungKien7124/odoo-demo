from .base_validator import BaseValidator


class SupplierValidator(BaseValidator):
    """
    Khởi tạo bộ Validator cho Supplier model
    - Danh sách các thuộc tính:
        + data: dictionary chứa dữ liệu cần kiểm tra
    - Các thương thức:
        + constrain_validate: Kiểm tra các trường bắt buộc
        + validate_data: Kiểm tra các trường dữ liệu khác
        + get_errors: Lấy ra tất cả các lỗi
    """

    def __init__(self):
        super().__init__()

    def constrain_validate(self):
        self.required('code')
        self.required('alias')
        self.required('country_id')

    def validate_data(self):
        # Code
        self.max_length('code', 100)

        # Alias
        self.max_length('alias', 500)

        # Name
        self.max_length('name', 500)

        # Address
        self.max_length('address', 500)

        # Area code
        self.max_length('area_code', 100)

        # Area name
        self.max_length('area_name', 100)

        # City code
        self.max_length('city_code', 100)

        # City name
        self.max_length('city_name', 100)

        # Phone number
        self.max_length('phone_number', 40)
        self.number('phone_number')

        # Email
        self.max_length('email', 100)
        self.email('email')

        # Website
        self.max_length('website', 500)
        self.url('website')

        # Tax code
        self.max_length('tax_code', 100)

        # Post code
        self.max_length('post_code', 100)

        # Fax number
        self.max_length('fax_number', 40)

    def validate_create_data(self, data):
        self.data = data
        self.constrain_validate()
        self.validate_data()
        return self.get_errors()

    def validate_update_data(self, data):
        self.data = data
        self.validate_data()
        return self.get_errors()

    def get_errors(self):
        return self.errors
