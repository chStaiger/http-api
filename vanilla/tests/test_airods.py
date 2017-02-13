# -*- coding: utf-8 -*-

from __future__ import absolute_import

import io
# import logging
from restapi.jsonify import json
from .. import RestTestsAuthenticatedBase
from commons.logs import get_logger

__author__ = 'Massimo Fares (massimo.fares@ingv.it)'

log = get_logger(__name__)


class TestSomething(RestTestsAuthenticatedBase):

    _main_endpoint = '/airodsmongo'
    # _irods_test_name = 'test'
    # _irods_home = '/tempZone/home/guest'
    # _irods_path = '/tempZone/home/guest/test'
    # _invalid_irods_path = '/tempZone/home/x/guest/test'
    # _test_filename = 'test.pdf'

    # def tearDown(self):

    #     log.debug('### Cleaning custom data ###\n')
    #     # Clean all test data
    #     endpoint = self._api_uri + self._main_endpoint
    #     r = self.app.delete(endpoint, data=dict(debugclean='True'),
    #                         headers=self.__class__.auth_header)
    #     self.assertEqual(r.status_code, self._hcodes.HTTP_OK_BASIC)

    #     super().tearDown()

    def test_01_GET_justatest(self):
        """ Test directory creation: POST """

        log.info('*** Testing GET')
        # GET non existing entity
        endpoint = (self._api_uri + self._main_endpoint)
        r = self.app.get(endpoint)  # , headers=self.__class__.auth_header)
        self.assertEqual(r.status_code, self._hcodes.HTTP_OK_BASIC)
