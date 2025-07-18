# -*- coding: utf-8 -*-
import json
from odoo import http
from psycopg2 import errors
from psycopg2 import IntegrityError
from odoo.http import request

# local package
from ..controllers.country_controller import CountryController


class CountryRoute(http.Controller):

    @http.route(
        "/api/nagaco_country/<int:id>",
        type="http",
        auth="public",
        methods=["DELETE"],
        csrf=False,
    )
    def delete(self, id):
        return CountryController().delete(id)
