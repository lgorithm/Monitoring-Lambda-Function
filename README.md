# Monitoring-Lambda-Function
As we know, in AWS everytime when Lambda-function is invoked, all the logs of every Lambda-function is automatically gets stored in CloudWatch. And every lambda-function(log-group) create several log-streams as they are invoked. And in every log-streams, there could be several events for every invocation as every invocation create several events.
This program will fetch every invocation details (starting time, ending time, status, etc.) of every lambda function in your AWS.
