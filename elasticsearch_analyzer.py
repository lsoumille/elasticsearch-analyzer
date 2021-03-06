#!/usr/bin/env python
# encoding: utf-8

from cortexutils.analyzer import Analyzer
from elasticsearch import Elasticsearch
import warnings
from elasticsearch import RequestsHttpConnection

#Class for adding proxy support to Elastic4py
class ProxiedConnection(RequestsHttpConnection):

	def __init__(self, *args, **kwargs):
		proxies = kwargs.pop('proxies', {})
		super(ProxiedConnection, self).__init__(*args, **kwargs)
		self.session.proxies = proxies

class ElasticSearchAnalyzer(Analyzer):

	#Handle configuration file options
	def __init__(self):
		Analyzer.__init__(self)
		self.service = self.get_param('config.service', None, 'Service parameter is missing')
		self.host = self.get_param('config.host', "localhost", 'Host parameter is missing')
		self.port = self.get_param('config.port', "9200", 'Port parameter is missing')
		self.https = self.get_param('config.https', False)
		self.username = self.get_param('config.username', 'elastic')
		self.password = self.get_param('config.password', 'changeme')
		self.index = self.get_param('config.index', "logstash-*")
		self.http_proxy = self.get_param('config.proxy_http', None)
		self.https_proxy = self.get_param('config.proxy_https', None)
		if self.https_proxy is not None:
			self.proxy = { 'https': self.https_proxy }
		else:
			self.proxy = { 'http': self.http_proxy }
		self.cert_check = self.get_param('config.cert_check', False)
		self.cert_path = self.get_param('config.cert_path', None)
		incomplete_query = self.get_param('config.query', None, 'Query is missing')
		if "%s" not in incomplete_query:
			self.query = incomplete_query
		else:
			self.query = incomplete_query % self.get_data()

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
			self.elasticsearch_api = Elasticsearch(elasticsearch_array, use_ssl=self.https, http_auth=self.https_auth, verify_certs=self.cert_check, ca_certs=self.cert_path, connection_class=ProxiedConnection, proxies=self.proxy)
		except Exception as e:
			self.error(e)

	#Query Elasticsearch
	def elasticsearch_search(self):
		try:
			self.res = self.elasticsearch_api.search(index=self.index, body=eval(self.query), request_timeout=120)
		except Exception as e:
			self.error(e)

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

	#Analyzer main function
	def run(self):
		if self.service == 'es-query':
			self.elasticsearch_connect()
			self.elasticsearch_search()
			self.report(self.res)
		else:
			self.error('Invalid service')

if __name__ == '__main__':
	#Remove warning if you don't use Certificate validation
	if self.cert_check == False:
		warnings.filterwarnings("ignore")
	ElasticSearchAnalyzer().run()
