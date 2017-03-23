# -*- coding: utf-8 -*-

""" Testing API code """

from ..rest.definition import EndpointResource
from commons.logs import get_logger
import json

log = get_logger(__name__)

RESPONSE1 = [{'pid' : '11099/qwoprerc-343536ssdfjs-34500-asdpwe94383' ,'network' :  { 'name' : 'NN', 'links' : { 'self' : 'webservices/networks/...' }},'station' : {'name' : 'SSSS','links' : {'self' : 'webservices/stations/...'}},'channel' : {'name' : 'CCC','links' : {'self' : 'webservices/channel/...'}}},{"others" : "......."}]
            
RESPONSE2 = [{"pid" : "11099/qwoprerc-343536ssdfjs-34500-asdpwe94383" ,"metadata": {"dc:contributor" : "network operator","dcterms:dateAccepted" : "2017-03-06T11:35:07.114Z","dc:identifier" : "test/f2c3ea40-0260-11e7-9f93-0242ac110008","dc:type" : "seismic waveform","dc:subject" : "mSEED, waveform, quality","dcterms:isPartOf" : "wfmetadata_catalog","dc:title" : "INGV_Repository","dc:rights" : "open access","dc:format" : "MSEED","dcterms:available" : "available from now","dc:date" : "2017-03-06T11:35:07.114Z","dc:coverage:x" : "LAT_val","dc:publisher" : "INGV EIDA NODE","dc:creator" : "INGV EIDA NODE","dc:coverage:t:min" : "time_start_val","dc:coverage:t:max" : "time_end_val","dc:coverage:x" : "LAT_val","dc:coverage:y" : "LON_val","dc:coverage:z" : "ELE_val","fileId" : "IV.ARCI..HHN.D.2015.011","smean" : 587.6017203352374,"stdev" : 25154.453024673716,"rms" : 25161.315203149203,"fileId" : "IV.ARCI..HHN.D.2015.011","type" : "seismic","status" : "open","glen" : 27054.59,"enc" : "STEIM2","srate" : 100,"gmax" : 27054.59,"sta" : "ARCI","net" : "IV","cha" : "HHN","loc" : ""}}]

class TestMongo(EndpointResource):

    def get(self):
        log.info("just a test")
        mongohd = self.global_get_service('mongo', dbname='mytest')
        
        # 	"_cls" : "commons.models.custom.mongo.Testing"
        mongohd.Testing(onefield='justatest').save()
        # log.pp(mongohd)
        print(mongohd)
        myargs= self.get_input()
        print(myargs)
        
        if myargs.get('download') == 'true':
            # TO FIX: problem with swagger-ui boolean?
            #return("TEST! download ok")
            return RESPONSE1
        else:
            #n = json.dumps(RESPONSE1)  
            #o = json.loads(n)
            return  RESPONSE2
        
        #"it works! - no download" str.replace(RESPONSE1, '\n', '\r\n')
    
class TestMongo1(EndpointResource):

    def get(self):
        log.info("just a test")
        mongohd = self.global_get_service('mongo', dbname='mytest')
        mongohd.Testing(onefield='justatest').save()
        # log.pp(mongohd)
        print(mongohd)
        return "it works!"
