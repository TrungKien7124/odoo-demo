class Normalizer():
    def __init__(self):
        pass

    @staticmethod
    def getColumnFromAlias(columnlist, ModelAlias2Fields):
        if not columnlist:
            return None, [item.value for item in ModelAlias2Fields] 
        if isinstance(columnlist, str):
            columnlist = columnlist.strip()
            if not columnlist:
                return None, [item.value for item in ModelAlias2Fields] 
            columnlist = columnlist.split(",")

        result = []

        for item in columnlist:
            if not item in ModelAlias2Fields.__members__:
                return "Danh sach cot khong hop le", None
            else:
                result.append(ModelAlias2Fields[item].value)
        return None, result
    
    @staticmethod
    def getLabelsFromFields(columnlist, modelLabels2Fields):
        if not columnlist:
            return None, [item.value for item in modelLabels2Fields] 
        if isinstance(columnlist, str):
            columnlist = columnlist.strip()
            if not columnlist:
                return None, [item.value for item in modelLabels2Fields] 
            columnlist = columnlist.split(",")

        result = []

        for item in columnlist:
            if not item in modelLabels2Fields.__members__:
                return "Danh sach cot khong hop le", None
            else:
                result.append(modelLabels2Fields[item].value)
        return None, result
    
    @staticmethod
    def getOrderString(order, ModelAlias2Fields):
        result = None

        if not order or str(order).strip() == "":
            return "id asc"

        if len(order.split(":")) != 2:
            return errMessage, result
        
        alias, direction = order.split(":")

        [errMessage, field] = Normalizer.getColumnFromAlias(alias, ModelAlias2Fields)

        if (errMessage):
            return "Order khong hop le", None
        else:
            direction = int(direction)
            if direction == 0:
                return None, f"{field[0]} asc"
            elif direction == 1:
                return None, f"{field[0]} desc"
            else:
                return "Order khong hop le", None


    @staticmethod
    def getModelFromJsonData(data, fieldList):
        def helper(item, fieldList):
            for field, value in item.items():
                if field not in fieldList:
                    return "Danh sách cột không hợp lệ", None
                item[field] = str(value).strip()
            return None, item

        cleaned_data = []
        for item in list(data):
            err, valid_item = helper(item, fieldList)
            if err:
                return err, None
            cleaned_data.append(valid_item)

        return None, cleaned_data
    
    @staticmethod
    def getModelDataFromLabels(data, modelFields2Labels):
        def helper(item, labels2Fields):
            res = {}
            for field, value in item.items():
                if field not in labels2Fields.keys():
                    return "Danh sach cot khong hop le", None
                res[labels2Fields[field]] = value
            return None, res
        
        labelList = [e.value for e in modelFields2Labels]
        fieldList = [e.name for e in modelFields2Labels]
        labels2Fields = dict(zip(labelList, fieldList))

        cleaned_data = []
        for item in list(data):
            err, valid_item = helper(item, labels2Fields)
            if err:
                return err, None
            cleaned_data.append(valid_item)

        return None, cleaned_data

    



        