#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Licensed to the Apache Software Foundation (ASF) under one or more
contributor license agreements. See the NOTICE file distributed with
this work for additional information regarding copyright ownership.
The ASF licenses this file to You under the Apache License, Version 2.0
(the "License"); you may not use this file except in compliance with
the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import json
import time
import inlong_dataproxy

def create_http_config():
    """Create configuration with HTTP reporting enabled"""
    config = {
        "init-param": {
            "inlong_group_ids": "test_group",
            "manager_url": "http://127.0.0.1:8083/inlong/manager/openapi/dataproxy/getIpList",
            "manager_update_interval": 2,
            "manager_url_timeout": 5,
            "msg_type": 7,
            "max_proxy_num": 8,
            "per_groupid_thread_nums": 1,
            "dispatch_interval_zip": 8,
            "dispatch_interval_send": 10,
            "recv_buf_size": 10240000,
            "send_buf_size": 10240000,
            "enable_pack": True,
            "pack_size": 409600,
            "pack_timeout": 3000,
            "ext_pack_size": 409600,
            "enable_zip": True,
            "min_zip_len": 512,
            "tcp_detection_interval": 60000,
            "tcp_idle_time": 600000,
            "log_num": 10,
            "log_size": 104857600,
            "log_level": 3,
            "log_path": "./",
            "enable_http_report": True,  # Enable HTTP reporting
            "http_report_url": "http://127.0.0.1:46802/dataproxy/message",
            "http_report_timeout": 10000,
            "need_auth": False,
            "auth_id": "",
            "auth_key": ""
        }
    }
    
    # Save config to file
    with open("http_config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    return "http_config.json"

def send_http_demo():
    """Demo for sending data via HTTP"""
    # Create HTTP configuration
    config_file = create_http_config()
    
    # Initialize API
    api = inlong_dataproxy.InLongApi()
    
    # Initialize with HTTP configuration
    ret = api.init_api(config_file)
    if ret != 0:
        print(f"Failed to initialize API: {ret}")
        return
    
    print("API initialized successfully with HTTP reporting enabled")
    
    # Send data
    group_id = "test_group"
    stream_id = "test_stream"
    message = "Hello, InLong HTTP!"
    
    try:
        for i in range(5):
            msg = f"{message} - Message {i+1}"
            ret = api.send(group_id, stream_id, msg.encode('utf-8'), len(msg.encode('utf-8')))
            if ret == 0:
                print(f"Message {i+1} sent successfully via HTTP")
            else:
                print(f"Failed to send message {i+1}: {ret}")
            time.sleep(1)
    
    except Exception as e:
        print(f"Error during sending: {e}")
    
    finally:
        # Close API
        api.close_api(1000)
        print("API closed")

if __name__ == "__main__":
    print("InLong DataProxy SDK - HTTP Sending Demo")
    print("=" * 50)
    send_http_demo()
