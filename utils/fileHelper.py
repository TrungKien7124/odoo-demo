import pandas as pd
import io
from odoo.http import Response
from io import StringIO


def export_file(data, file_name, file_type='csv'):
    print(file_type)
    output = io.StringIO()

    if file_type == 'csv':
        pd.DataFrame(data).to_csv(output, index=False)
    elif file_type == 'xlsx':
        output = io.BytesIO()
        pd.DataFrame(data).to_excel(output, index=False)
    else:
        raise ValueError("Unsupported file type")

    return Response(
        output.getvalue(),
        headers={
            'Content-Disposition': f'attachment; filename={file_name}.{file_type}',
            'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' if file_type == 'xlsx' else 'text/csv'
        }
    )


def import_file(file):
    if not hasattr(file, 'read'):
        raise ValueError("File không hợp lệ")

    filename = file.filename.lower()

    try:
        file.seek(0)

        # Xử lý file CSV
        if filename.endswith('.csv'):
            content = file.read().decode('utf-8-sig')
            df = pd.read_csv(StringIO(content), encoding='utf-8-sig')

        # Xử lý file Excel (.xls hoặc .xlsx)
        elif filename.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(file, engine='openpyxl')

        else:
            raise ValueError("Chỉ hỗ trợ file .csv, .xls, .xlsx")

        df = df.where(pd.notnull(df), None)
        print(df)

        # Trả về dữ liệu dạng list[dict]
        return df.to_dict(orient='records')

    except Exception as e:
        raise ValueError(f"Lỗi đọc file: {str(e)}")
