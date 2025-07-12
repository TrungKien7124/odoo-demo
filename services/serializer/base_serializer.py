class BaseSerializer:
    """
        Class chuyển đổi kiểu dữ liệu model thành dictionary
    """

    def __init__(self, data, columnlist=None):
        self.data = data
        if not columnlist:
            self.columnlist = data.fields_get().keys() if hasattr(data, 'fields_get') else None
        else:
            self.columnlist = columnlist

    def serialize_one(self, item):
        """
            ...
        """
        result = {}
        if isinstance(item, dict):
            item = item.items()
        elif hasattr(item, '_fields'):
            item = [(field, getattr(item, field)) for field in item._fields]
        else:
            raise ValueError("Không thể serialize dữ liệu này")
        for field, value in item:
            if field in self.columnlist:
                if isinstance(value, (list, tuple)):
                    result[field] = str(value[0]).strip() if value else None
                elif isinstance(value, dict):
                    result[field] = {k: str(v).strip()
                                     for k, v in value.items()} if value else None
                elif hasattr(value, 'id'):
                    result[field] = value.id if value else None
                else:
                    result[field] = str(value).strip() if value else None
        return result

    def serialize_all(self):
        if isinstance(self.data, list):
            return [self.serialize_one(item) for item in self.data]
        return self.serialize_one(self.data)
