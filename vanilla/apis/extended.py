# -*- coding: utf-8 -*-

"""
B2SAFE HTTP REST API endpoints.

Code to implement the extended endpoints

Note:
Endpoints list and behaviour are available at:
https://github.com/EUDAT-B2STAGE/http-api/blob/metadata_parser/docs/user/endpoints.md

"""

from __future__ import absolute_import

from ..rest.definition import EndpointResource
from commons import htmlcodes as hcodes
from commons.logs import get_logger

log = get_logger(__name__)


###############################
# Classes

class PIDEndpoint(EndpointResource):

    def get(self, pid=None):
        """ Download file from pid """
        if pid is None:
            return self.send_errors(
                message='Missing PID inside URI',
                code=hcodes.HTTP_BAD_REQUEST)

        ###################
        # Performe B2HANDLE request
        ###################

        return "Hello world!"
