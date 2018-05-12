#!/usr/bin/env python
# encoding: utf-8

from cortexutils.analyzer import Analyzer
from elasticsearch import Elasticsearch
import warnings


class ElasticSearchAnalyzer(Analyzer):
#class ElasticSearchAnalyzer():

	#Handle configuration file options
	def __init__(self):
		#print("START INIT")
		Analyzer.__init__(self)
		#print("START INIT")
		self.service = self.get_param('config.service', None, 'Service parameter is missing')
		self.host = self.getParam('config.host', "localhost", 'Host parameter is missing')
		self.port = self.getParam('config.port', "9200", 'Port parameter is missing')
		self.https = self.getParam('config.https', False)
		self.username = self.getParam('config.username', 'elastic')
		self.password = self.getParam('config.password', 'changeme')
		self.index = self.getParam('config.index', "logstash-*")
		##DEBUG
		#self.https = True
		#self.service = "query"
		#self.host = "localhost"
		#self.port = "9200"
		#self.username = "elastic"
		#self.password = "changeme"
		#self.index = "logstash-*"
		##DEBUG
		

	#Initialize Elasticsearch session
	def elasticsearch_connect(self):
		#Setup user
		if self.username is not None:
			self.https_auth = (self.username, self.password)
		else:
			self.https_auth = None
		#Create Elasticsearch array
		elasticsearch_array = []
		for server in self.host:
			elasticsearch_array.append("{}:{}".format(server, self.port))
		#Create binding
		try:
			self.elasticsearch_api = Elasticsearch(elasticsearch_array, use_ssl=self.https, http_auth=self.https_auth, verify_certs=False)
		except Exception as e:
			self.error(e)
					
	#Query Elasticsearch
	def elasticsearch_search(self):
		#print("START SEARCH")
		try:
			self.res = self.elasticsearch_api.search(index=self.index, body={"query": {"match": {'user':'kimchy'}}})
			#print(self.res)
		except Exception as e:
			self.error(e)
			#print(e)

	#Generate Short report
	def summary(self, raw):
		taxonomies = []
		namespace = "ES"
		predicate = "Hits"
		value = "\"0\""
		result = {
			"has_result": True
		}
		#If no result then return an error
		if raw["hits"]["total"] == 0:
			result["has_result"] = False
		else:
			level = "info"
			value = "{}".format(raw["hits"]["total"])
		#Build taxonomy
		taxonomies.append(self.build_taxonomy(level, namespace, predicate, value))
		return {"taxonomies": taxonomies}

	def run(self):
		#print("START RUN")
		if self.service == 'es-query':
			#self.field = self.getParam('field', None, 'Field value is missing')
			self.elasticsearch_connect()
			self.elasticsearch_search()
			self.report(self.res)
		else:
			self.error('Invalid service')
			#print("Invalid service")

if __name__ == '__main__':
	warnings.filterwarnings("ignore")
	ElasticSearchAnalyzer().run()