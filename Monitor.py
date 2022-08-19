import boto3
from datetime import datetime, timedelta

# creating  session with AWS Credential:
session = boto3.session.Session(aws_access_key_id="####################",
                                aws_secret_access_key='########################################',
                                region_name='us-east-1')
print(session)
# Getting details of logs group:
cloudwatch_obj = session.client('logs')
response = cloudwatch_obj.describe_log_groups()

status_msg = ''
status = "Success"
start_timestamp = None
end_timestamp = None
i = 1
st = 0
mg = 0
ed = 0


# Function for printing details of event:
def event_detail():
    global status, i, status_msg, start_timestamp, end_timestamp, st, mg, ed
    start_time = datetime.fromtimestamp(start_timestamp / 1000)
    end_time = datetime.fromtimestamp(end_timestamp / 1000)
    print("Details of Event number: {}".format(i))
    print("Stating Time: {} and Ending Time: {}".format(start_time, end_time))
    print("Status: {} And Message:{}".format(status, status_msg))
    start_timestamp = None
    end_timestamp = None
    status = "Success"
    status_msg = ''
    i += 1
    st = 0
    mg = 0
    ed = 0


# Extracting the events of every log streams of every log groups:
for log in response['logGroups']:
    logs_group = log['logGroupName']
    print("Details of Lambda Function: {}".format(logs_group))
    logStream_per_function = cloudwatch_obj.describe_log_streams(logGroupName=logs_group, orderBy='LastEventTime',
                                                                 descending=True)
    for logstream in logStream_per_function['logStreams']:
        stream_name = logstream['logStreamName']
        events_per_stream = cloudwatch_obj.get_log_events(logGroupName=logs_group, logStreamName=stream_name,
                                                          startTime=int(((datetime.now() - timedelta(
                                                              hours=90)).timestamp()) * 1000),
                                                          endTime=int((datetime.now().timestamp()) * 1000))
        print("LogStream_Name: {}".format(stream_name))
        for event in events_per_stream['events']:
            msg = event['message']
            if st == 0 and mg == 0 and ed == 0:
                if msg[0:5] == 'START':
                    start_timestamp = event['timestamp']
                    st = 1
            elif st == 1 and mg == 0 and ed == 0:
                if msg[1:6] == 'ERROR':
                    status = "Failed"
                    status_msg = status_msg + msg
                    mg = 1
                elif msg[0:3] == 'END':
                    end_timestamp = event['timestamp']
                    event_detail()
            elif st == 1 and mg == 1 and ed == 0:
                if msg[0:3] == 'END':
                    end_timestamp = event['timestamp']
                    event_detail()
        print('\n')
    i = 1
    print('\n')
