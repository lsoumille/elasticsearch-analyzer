# Elasticsearch-Analyzer
Elasticsearch Cortex analyzer implementation

### Use Case

Make Elasticsearch queries from extracted observables

### Done
* JSON configuration file
* Analyzer skeleton
* Elasticsearch functions
* Cortex input integration
* Support several Elasticsearch hosts to query
* Observable as query argument
* Template writing
* Elasticsearch query tuning (aggregations, based on timestamp...)

### To Be Tested
* Add proxy support
* Add Certificate verification

### To Be Done
* Make new flavors

## How to make a new flavor
. Copy paste Elasticsearch_base.json.template to Elasticsearch_NAME.json
. Fulfill Elasticsearch_NAME.json, replace XXXX vy values that are matching your environment
. Add Elasticsearch_NAME as name value
. Add your name as author value
. Add your Elasticsearch Query (make always an aggregation for matching TheHive template output)
. Add observable types on which users will launch your analyzer
. DO NOT CHANGE baseConfig and service
. Optional : Update Cortex configuration in order to use your own analyzers if it's already done
. Restart Cortex
. Make the analyzer configuration (set up ES URL, authentication settings ...)
. Upload the template in TheHive
. Analyze ! should be working