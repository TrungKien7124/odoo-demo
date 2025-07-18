from .base_controller import BaseController

from ..models.country_model import CountryAlias2Fields, CountryFields2Labels

class CountryController(BaseController):
    def __init__(self):
        super().__init__('country', None)
        self.modelAlias2Fields = CountryAlias2Fields
        self.modelFields2Labels = CountryFields2Labels
        self.fieldList = [field.name for field in self.modelFields2Labels]
        self.labelList = [field.value for field in self.modelFields2Labels]
        self.uniqueFields = ['code']
        self.foreignFields = {'country_id': 'country'}