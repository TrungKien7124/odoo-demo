class Serializer():
    def __init__(self):
        pass

    @staticmethod
    def serialize(data, columnlist, modelFields2Labels, endUser=False):
        def serialize_1_item(item, columnlist, modelFields2Labels=None, endUser=False):
            item = [(field, getattr(item, field)) for field in item._fields]
            res = {}
            for field, value in item:
                if field in columnlist:
                    if endUser:
                        field = modelFields2Labels[field].value
                    if hasattr(value, 'id'):
                        res[field] = getattr(value, 'id')
                    elif not value:
                        res[field] = None
                    else:
                        res[field] = str(value).strip()
            return res
        
        print(data)

        if isinstance(data, list):
            return [serialize_1_item(item, columnlist, modelFields2Labels, endUser) for item in data]
        return serialize_1_item(data, columnlist, modelFields2Labels, endUser)
