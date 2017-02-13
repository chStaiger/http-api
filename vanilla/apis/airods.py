# -*- coding: utf-8 -*-

""" Testing API code """

from ..rest.definition import EndpointResource
from commons.logs import get_logger

log = get_logger(__name__)


class TestMongo(EndpointResource):

    def get(self):
        log.info("just a test")
        mongohd = self.global_get_service('mongo', dbname='mytest')
        mongohd.Testing(onefield='justatest').save()
        # log.pp(mongohd)
        print(mongohd)
        return "it works!"
