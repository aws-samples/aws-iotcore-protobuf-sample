# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import boto3
from botocore.config import Config
from datetime import datetime
import os
from random import random
import time

from google.protobuf.json_format import MessageToJson
from msg_pb2 import Telemetry

AWS_REGION = os.environ['AWS_REGION'] or 'us-west-2'
IOT_ENDPOINT = os.environ['IOT_ENDPOINT']
TOPIC = 'test/telemetry_all'

config = Config(region_name=AWS_REGION)

c_iot_data = boto3.client('iot-data', config=config, endpoint_url='https://{}'.format(IOT_ENDPOINT))

while True:
    m = Telemetry()
    m.msgType = Telemetry.MSGTYPE_NORMAL

    m.instrumentTag = 'Temperature-001'
    m.timestamp.FromDatetime(datetime.now())
    m.value = random() * 100

    if m.value >= 80: # 20% of the messages will be MSGTYPE_ALERT
        m.msgType = Telemetry.MSGTYPE_ALERT

    serialized = m.SerializeToString()
    
    try:
        res = c_iot_data.publish(topic=TOPIC, qos=1, payload=serialized)
        print(f"Published message {MessageToJson(m)} to AWS IoT")
        time.sleep(5)
    except KeyboardInterrupt:
      print("Exiting")
      break
    except Exception as e:
        print(e)
        break
