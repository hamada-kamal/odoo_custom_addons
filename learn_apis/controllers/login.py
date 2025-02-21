import json
import logging
import functools
import werkzeug.wrappers
from odoo import http
from odoo.addons.learn_apis.models.common import invalid_response, valid_response
from odoo.exceptions import AccessDenied, AccessError
from odoo.http import request



_logger = logging.getLogger(__name__)

def validate_token(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        token = request.httprequest.headers.get('token')
        if not token:
            return invalid_response("access_token_not_found", "You don't have access to create a new project!")
        access_token = request.env['access.token'].sudo().search([('token', '=', token)], order='id DESC', limit=1)
        if access_token.find_or_create(user_id=access_token.user_id.id) !=  token:
            return invalid_response("access_token_error", "access token expired or invalid!")
        # request.session.uid = access_token.user_id.id
        # request.uid = access_token.user_id.id
        request.update_env(user=access_token.user_id)
        return func(self, *args, **kwargs)
    return wrapper


class AccessToken(http.Controller):


    @http.route("/api/login/token_api_key", methods=["GET"], type="http", auth="none", csrf=False)
    def api_login_api_key(self, **post):
        # The request post body is empty the credetials maybe passed via the headers.
        headers = request.httprequest.headers
        db = headers.get("db")
        api_key = headers.get("api_key")
        _credentials_includes_in_headers = all([db, api_key])
        if not _credentials_includes_in_headers:
            # Empty 'db' or 'username' or 'api_key:
            return invalid_response(
                "missing error", "either of the following are missing [db ,api_key]", 403,
            )
        # Login in odoo database:
        user_id = request.env["res.users.apikeys"]._check_credentials(scope="rpc", key=api_key)
        # request.session.authenticate(db, username, api_key)
        if not user_id:
            info = "authentication failed"
            error = "authentication failed"
            _logger.error(info)
            return invalid_response(401, error, info)

        uid = user_id
        user_obj = request.env['res.users'].sudo().browse(int(uid))

        # Generate tokens
        access_token = request.env["access.token"].find_or_create(user_id=uid, create=True)
        # Successful response:
        return werkzeug.wrappers.Response(
            status=200,
            content_type="application/json; charset=utf-8",
            headers=[("Cache-Control", "no-store"), ("Pragma", "no-cache")],
            response=json.dumps(
                {
                    "uid": uid,
                    # "user_context": request.session.get_context() if uid else {},
                    "company_id": user_obj.company_id.id if uid else None,
                    "company_ids": user_obj.company_ids.ids if uid else None,
                    "partner_id": user_obj.partner_id.id,
                    "access_token": access_token,
                    "company_name": user_obj.company_name,
                    "country": user_obj.country_id.name,
                    "contact_address": user_obj.contact_address,
                }
            ),
        )

    @validate_token
    @http.route("/api/project/create", methods=["POST"], type="http", auth="none", csrf=False)
    def create_project(self, **post):
        uid = request.uid
        user_id = request.env['res.users'].browse(uid)
        payload = request.httprequest.data.decode()
        payload = json.loads(payload)
        project_name = payload.get('project_name')
        project_obj = request.env['project.project']
        new_project = project_obj.with_user(user_id).create({
            'name':project_name,
        })
        if new_project:
            return valid_response([{'project_id': new_project.id, 'message': 'project created successfully'}], status=201)
