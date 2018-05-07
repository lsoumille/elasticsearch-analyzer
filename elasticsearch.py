#!/usr/bin/env python
# encoding: utf-8

from cortexutils.analyzer import Analyzer
from elasticsearch import Elasticsearch

class ElasticSearchAnalyzer(Analyzer):

	#Handle configuration file options
	def __init__(self):
		Analyzer.__init__(self)
		self.service = self.get_param('config.service', None, 'Service parameter is missing')
		self.host = self.getParam('config.host', None, 'Host parameter is missing')
	    self.port = self.getParam('config.port', None, 'Port parameter is missing')
	    self.https = self.getParam('config.https', False)
        self.username = self.getParam('config.username', None)
        self.password = self.getParam('config.password', None)

    #Initialize Elasticsearch session
    def elasticsearch_connect():
    	try:
    		self.elasticsearch_api = Elasticsearch(["{}:{}".format(self.host, self.port)], use_ssl=self.https) 
    	except Exception, e:
    		self.error(e)

    #Generate Short report
    def summary(self, raw):
    	taxonomies = []
	    predicate = "Hits"
	    value = "\"0\""
        result = {
            "has_result": True
        }
        #If no result then return an error
        if raw["results"] == 0:
        	result["has_result"] = False
        else:
        	level = "info"
        	value = "{}".format(raw["results"])
        #Build taxonomy
        taxonomies.append(self.build_taxonomy(level, namespace, predicate, value))
		return {"taxonomies": taxonomies}

	def run(self):
		if self.service == 'query':
			field = self.getParam('field', None, 'Field value is missing')
			self.elasticsearch_connect()
		else:
			self.error('Invalid service')