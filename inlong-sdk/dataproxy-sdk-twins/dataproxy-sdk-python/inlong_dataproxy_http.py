#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
InLong DataProxy Python SDK - HTTP Implementation

A pure Python implementation for HTTP reporting to InLong DataProxy.
Compatible API with the original C++ SDK.
"""

import json
import time
import os
import requests


class InLongApi:
    """
    HTTP-based InLong DataProxy SDK.
    Compatible API with the original C++ SDK.
    """
    
    def __init__(self):
        self.session = None
        self.http_url = None
        self.timeout = 10.0
        
    def init_api(self, config_path):
        """Initialize API with configuration file."""
            
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            init_param = config.get('init-param', {})
            
            # Get HTTP URL
            self.http_url = init_param.get('http_report_url')
            if not self.http_url:
                print("ERROR: http_report_url not configured")
                return -1
            
            # Set timeout
            timeout_ms = init_param.get('http_report_timeout', 10000)
            self.timeout = timeout_ms / 1000.0
            
            # Create session
            self.session = requests.Session()
            
            return 0
            
        except Exception as e:
            print(f"ERROR: Failed to initialize: {e}")
            return -1
    
    def send(self, group_id, stream_id, msg, msg_len, callback=None):
        """Send message to DataProxy via HTTP."""
        if not self.session or not self.http_url:
            return -1
            
        try:
            # Prepare data
            body = msg.decode('utf-8') if isinstance(msg, bytes) else str(msg)
                
            data = {
                'groupId': group_id,
                'streamId': stream_id,
                'dt': str(int(time.time() * 1000)),
                'cnt': '1',
                'body': body
            }
            
            # Send HTTP request
            response = self.session.post(self.http_url, data=data, timeout=self.timeout)
            
            # Check response
            success = response.status_code == 200
            if success and response.text:
                try:
                    result = response.json()
                    success = result.get('code') == 0
                except:
                    pass  # Assume success if no valid JSON
            
            # Call callback if provided
            if callback and success:
                callback(group_id, stream_id, msg, msg_len, int(time.time() * 1000), "")
            
            return 0 if success else -1
            
        except Exception as e:
            print(f"ERROR: Send failed: {e}")
            return -1
    
    def close_api(self, timeout_ms=1000):
        """Close API and clean up resources."""
        try:
            if self.session:
                self.session.close()
                self.session = None
            return 0
        except:
            return -1
