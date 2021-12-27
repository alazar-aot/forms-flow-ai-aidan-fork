"""API endpoints for managing process resource."""

from http import HTTPStatus

from flask import current_app, request
from flask_restx import Namespace, Resource

from formsflow_api.services import ProcessService
from formsflow_api.utils import auth, cors_preflight, profiletime


API = Namespace("Process", description="Process")


@cors_preflight("GET,OPTIONS")
@API.route("", methods=["GET", "OPTIONS"])
class ProcessResource(Resource):
    """Resource for managing process."""

    @staticmethod
    @auth.require
    @profiletime
    def get():
        """Get all process."""
        try:
            return (
                (
                    {
                        "process": ProcessService.get_all_processes(
                            token=request.headers["Authorization"]
                        )
                    }
                ),
                HTTPStatus.OK,
            )
        except BaseException as err:
            response, status = {
                "type": "Bad request error",
                "message": "Invalid request data object",
            }

            current_app.logger.warning(response)
            current_app.logger.warning(err)
            return response, status


# API for getting process diagram xml -for displaying bpmn diagram in UI
@cors_preflight("GET,OPTIONS")
@API.route("/<string:process_key>/xml", methods=["GET", "OPTIONS"])
class ProcessDefinitionResource(Resource):
    """Resource for managing process details."""

    @staticmethod
    @auth.require
    @profiletime
    def get(process_key):
        """Get process detailsXML."""
        try:
            return (
                ProcessService.get_process_definition_xml(
                    process_key, request.headers["Authorization"]
                ),
                HTTPStatus.OK,
            )
        except BaseException as err:
            response, status = {
                "type": "Bad request error",
                "message": "Invalid request data object",
            }, HTTPStatus.BAD_REQUEST

            current_app.logger.warning(response)
            current_app.logger.warning(err)
            return response, status
