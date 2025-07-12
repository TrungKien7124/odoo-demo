from .base_service import BaseService

from .validator.supplier_validator import SupplierValidator


class SupplierService(BaseService):

    def __init__(self):
        validator = SupplierValidator()
        super().__init__('supplier', validator)
