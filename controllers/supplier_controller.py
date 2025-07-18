from .base_controller import BaseController

from ..helper.validator.supplier_validator import SupplierValidator
from ..models.supplier_model import SupplierAlias2Field, SupplerFields2Labels


class SupplierController(BaseController):

    def __init__(self):
        validator = SupplierValidator()                             
        super().__init__('supplier', validator)
        self.modelAlias2Fields = SupplierAlias2Field
        self.modelFields2Labels = SupplerFields2Labels
        self.fieldList = [field.name for field in self.modelFields2Labels]
        self.labelList = [field.value for field in self.modelFields2Labels]
        self.uniqueFields = ['code']
        self.foreignFields = {'country_id': 'country'}
