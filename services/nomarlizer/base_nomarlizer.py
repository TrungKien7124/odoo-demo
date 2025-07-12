class BaseNomarlizer:
    def __init__(self, data):
        self.data = data

    def normalize_1_item(self, item):
        result = {}
        for field, value in item.items():
            if isinstance(value, str):
                value = value.strip() if value else ""
            else:
                value = str(value).strip() if value else ""
            result[field] = value
        return result

    def normalize_all(self):
        if not isinstance(self.data, list):
            self.data = [self.data]
        return [self.normalize_1_item(item) for item in self.data]
