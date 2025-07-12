import json
from odoo.http import Response


def get_response(data):
    return Response(json.dumps({
        'code': '200',
        'status': 'success',
        'message': 'Thành công',
        'data': data
    }),
        status=200,
        content_type='application/json'
    )
