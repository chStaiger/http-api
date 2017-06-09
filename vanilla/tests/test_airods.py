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

    _main_endpoint = '/statics/metadata' # qui l'endpoint dichiarati in specs.yaml /statics/metadata
    _my_params = '?start="12-02-2017T00.00.00"&end="13-02-2017T00.00.00"&minlat=12.30&minlon=12.30&maxlat=12.30&maxlon=12.30&download=False'
    #_main_endpoint = '/airodsmongo' # qui l'endpoint dichiarati in specs.yaml /statics/metadata
   
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
        """ First test """

        log.info('*** Testing GET')
        endpoint = (self._api_uri + self._main_endpoint + self._my_params)
        r = self.app.get(endpoint)  # , headers=self.__class__.auth_header)
        print ("QUESTO!")
        print (r.data)
        self.assertEqual(r.status_code, self._hcodes.HTTP_OK_BASIC)
        log.info('*** Testing GET FAKE - OK')
        
        
