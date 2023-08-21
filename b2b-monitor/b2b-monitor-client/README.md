This "b2b-monitor-client" app is used for "MSSQL POC" project which using application on cloud and connecto to onprem MSSQL DB

#What this app does
It will continuously call 4 APIs of the POC App which is "b2b-projectnet-admin".
The 4 apis: B2B_DETAIL_FAQS, B2B_FIND_FAQS, B2B_SAVE_FAQS & B2B_ADD_FAQS
Each time, this call will call 4 above api and then sleep an INTERVAL
For each API Call, it logs the response detail and expose to the histogram metrics named "http_server_duration"
The label "exported_job"  is set by "EXPORTED_JOB_NAME" env

The endpoint of "b2b-projectnet-admin" app is set by env "DOMAIN".

#Build this app
docker build -t [your-repo:tag] .

#how to deploy this app
This app can be deploy with the manifest including a deployment, a service and a servicemonitor (to help its metrics to be collected by prometheus)

kubeclt apply -f manifest/deployment.yaml
kubeclt apply -f manifest/service.yaml
kubeclt apply -f manifest/servicemonitor.yaml

#Metrics
This app expose metrics at default port and at "/metrics" path
Using servicemonitor to apply a new target in prometheus collecting these metrics. 