"""
Write a python script to pull custom metrics  from a Linux instance (e.g. 
memory usage, disk usage, cpu usage, etc)  and submit them into Cloudwatch 
Collect memory usage metrics to submit to cloudwatch (leverage for a boto3 mocking) https://github.com/spulec/moto
"""

import boto3
from moto import mock_cloudwatch
import psutil

def fetch_disk_usage():
    return (psutil.disk_usage("/").percent)

def fetch_memory_usage():
    return (psutil.virtual_memory().percent)

def fetch_cpu_usage():
    return (psutil.cpu_percent())

@mock_cloudwatch
def send_to_cloudwatch(cpu_usage, memory_usage, disk_usage):
    cw_client = boto3.client("cloudwatch", region_name='us-east-1')
    response = cw_client.put_metric_data(
        Namespace='6sense',
        MetricData=[
            {
                'MetricName': 'CPU-Usage',
                'Values': cpu_usage,
                'Unit': '%',
                'StatisticValues': {
                    'SampleCount': len(cpu_usage),
                    'Sum': sum(cpu_usage),
                    'Minimum': min(cpu_usage),
                    'Maximum': max(cpu_usage)
                },
            },
            {
                'MetricName': 'Memory-Usage',
                'Values': memory_usage,
                'Unit': '%',
            },
            {
                'MetricName': 'Disk-Usage',
                'Values': disk_usage,
                'Unit': '%'
            }
        ]
    )
    print(response)

if __name__ == "__main__":
    cpu_usage_list = []
    memory_usage_list = []
    disk_usage_list = []

    for i in range(0, 60):
        cpu_usage = fetch_cpu_usage()
        cpu_usage_list.append(cpu_usage)

        memory_usage = fetch_memory_usage()
        memory_usage_list.append(memory_usage)

        disk_usage = fetch_disk_usage()
        disk_usage_list.append(disk_usage)

    send_to_cloudwatch(cpu_usage_list, memory_usage_list, disk_usage_list)

