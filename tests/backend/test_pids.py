# -*- coding: utf-8 -*-

"""
Test pids endpoints

Run single test:
nose2 test.custom.test_dataobjects.TestDataObjects.test_07_delete_dataobjects
"""

import io
import json
from test import RestTestsAuthenticatedBase
from rapydo.utils.logs import get_logger

__authors__ = [
    'Roberto Mucci (r.mucci@cineca.it)'
]

log = get_logger(__name__)


class TestPids(RestTestsAuthenticatedBase):

    _main_endpoint = '/pids'

    def tearDown(self):

        log.debug('### Cleaning custom data ###\n')
        super().tearDown()

    def test_01_GET_public_PID(self):
        """ Test directory creation: POST """

        log.info('*** Testing GET public PID')

        pid = '11100/33ac01fc-6850-11e5-b66e-e41f13eb32b2'
        worng_pid = '11100/33ac01fc-6850-11e5-XXXX-e41f13eb3212'
        
        # GET URL from PID
        endpoint = (self._api_uri + self._main_endpoint +
                    '/' + pid)
        r = self.app.get(endpoint, headers=self.__class__.auth_header)
        self.assertEqual(r.status_code, self._hcodes.HTTP_OK_BASIC)
        data = json.loads(r.get_data(as_text=True))

        # To be fixed
        self.assertEqual(
            data['Response']['data']['URL'],
             'irods://data.repo.cineca.it:1247/CINECA01/home/cin_staff/rmucci00/DSI_Test/test.txt')

        # GET URL from non existing PID
        endpoint = (self._api_uri + self._main_endpoint +
                    '/' + worng_pid)
        r = self.app.get(endpoint, headers=self.__class__.auth_header)
        self.assertEqual(r.status_code, self._hcodes.HTTP_BAD_NOTFOUND)
