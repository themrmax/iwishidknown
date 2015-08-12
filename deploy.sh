aws s3 mb s3://iwishidknown-log
aws s3 mb s3://iwishidknown
aws s3 cp iwishidknown.sh s3://iwishidknown/
aws s3 cp iwishidknown.py s3://iwishidknown/
aws s3 cp watchlist.txt s3://iwishidknown/

response=`aws datapipeline create-pipeline --name iwishidknown --unique-id iwishidknown`
# response is of the form { "pipelineId": "df-05033941C83LSDPT0B42" }
# parse this using substring extraction
id=${response:21:23}
aws datapipeline put-pipeline-definition --pipeline-id $id --pipeline-definition file://pipelinedef.json
aws datapipeline activate-pipeline --pipeline-id $id
