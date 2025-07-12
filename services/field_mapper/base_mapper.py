from odoo.http import request

from ...utils.error_format import ErrorFormat


class BaseMapper:

    def __init__(self, modelName):
        model = request.env[modelName].sudo()
        self.alias_to_column = getattr(model, 'alias_dict', {})
        self.column_to_label = getattr(model, 'label_dict', {})

    def handle_input_data(self, data, error_code, type="column"):
        columnlist = None
        value = None
        if not data:
            if type == "alias":
                columnlist = list(self.alias_to_column.keys())
            elif type == "label":
                columnlist = list(self.column_to_label.values())
            else:
                columnlist = list(self.alias_to_column.values())
        elif isinstance(data, str):
            columnlist = data.split(',')
        elif isinstance(data, list):
            columnlist = data
        elif isinstance(data, dict):
            columnlist = list(data.keys())
            value = list(data.values())
        else:
            raise ErrorFormat(
                f"{error_code}600", "error", "Columnlist khong hop le",
                None)
        return [columnlist, value]

    def get_columns(self, data, error_code):
        valid_columns = []
        errors = []

        columnlist, value = self.handle_input_data(data, error_code)

        for column in columnlist:
            if column not in self.alias_to_column.values():
                errors.append(column)

        if errors:
            raise ErrorFormat(
                f"{error_code}607", "error", "columnlist khong hop le",
                errors)
        if value:
            valid_columns = dict(zip(columnlist, value))

        return valid_columns

    def get_column_from_alias(self, data, error_code):
        valid_columns = []
        errors = []

        if not data:
            return list(self.alias_to_column.values())

        columnlist, value = self.handle_input_data(data, error_code, "alias")

        for alias in columnlist:
            column = self.alias_to_column.get(alias)
            if column:
                valid_columns.append(column)
            else:
                errors.append(alias)

        if errors:
            raise ErrorFormat(
                f"{error_code}607", "error", "columnlist khong hop le",
                errors)
        if value:
            valid_columns = dict(zip(valid_columns, value))
        return valid_columns

    def get_label_from_column(self, data, error_code):
        valid_labels = []
        errors = []

        if not data:
            return list(self.column_to_label.values())

        columnlist, value = self.handle_input_data(data, error_code)

        for column in columnlist:
            label = self.column_to_label.get(column)
            if label:
                valid_labels.append(label)
            else:
                errors.append(column)

        if errors:
            raise ErrorFormat(
                f"{error_code}607", "error", "columnlist khong hop le",
                errors)
        if value:
            valid_labels = dict(zip(valid_labels, value))
        return valid_labels

    def get_column_from_label(self, data, error_code):
        valid_columns = []
        errors = []

        if not data:
            return list(self.column_to_label.keys())

        columnlist, value = self.handle_input_data(data, error_code, "label")

        for label in columnlist:
            column = next(
                (col for col, lbl in self.column_to_label.items() if lbl == label), None)
            if column:
                valid_columns.append(column)
            else:
                errors.append(label)

        if errors:
            raise ErrorFormat(
                f"{error_code}607", "error", "columnlist khong hop le",
                errors)

        if value:
            valid_columns = dict(zip(valid_columns, value))

        return valid_columns

    def get_order_by(self, order, error_code):
        if not order:
            return ['id', 'asc']
        order_part = order.split(':')
        if len(order_part) > 2 or len(order_part) < 2:
            raise ErrorFormat(f"{error_code}600", "Error", "Order khong hop le",
                              None)
        column = self.get_column_from_alias(order_part[0], error_code)
        direction = None
        if order_part[1] == '0':
            direction = "asc"
        elif order_part[1] == '1':
            direction = "desc"
        else:
            raise ErrorFormat(f"{error_code}600", "Error", "Order khong hop le",
                              None)
        return f"{column[0]} {direction}"
