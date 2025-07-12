/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements. See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License. You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include "http_client.h"
#include "../core/api_code.h"
#include <sstream>
#include <iostream>
#include <cstdint>

namespace inlong {

HttpClient::HttpClient(std::string url, uint64_t timeout)
    : url_(url), timeout_(timeout), curl_(nullptr) {}

HttpClient::~HttpClient() {
    Close();
}

bool HttpClient::Init() {
    curl_global_init(CURL_GLOBAL_ALL);
    curl_ = curl_easy_init();
    if (curl_) {
        return true;
    }
    return false;
}

void HttpClient::Close() {
    if (curl_) {
        curl_easy_cleanup(curl_);
    }
    curl_global_cleanup();
}

size_t HttpClient::WriteCallback(void* contents, size_t size, size_t nmemb, void* userp) {
    ((std::string*)userp)->append((char*)contents, size * nmemb);
    return size * nmemb;
}

int32_t HttpClient::Send(const std::string& group_id, const std::string& stream_id, const std::string& msg) {
    if (!curl_) {
        return SdkCode::kErrorInit;
    }

    std::string full_url = url_ + "?group_id=" + group_id + "&stream_id=" + stream_id;
    std::string read_buffer;

    curl_easy_setopt(curl_, CURLOPT_URL, full_url.c_str());
    curl_easy_setopt(curl_, CURLOPT_POSTFIELDS, msg.c_str());
    curl_easy_setopt(curl_, CURLOPT_WRITEFUNCTION, WriteCallback);
    curl_easy_setopt(curl_, CURLOPT_WRITEDATA, &read_buffer);
    curl_easy_setopt(curl_, CURLOPT_TIMEOUT_MS, timeout_);

    CURLcode res = curl_easy_perform(curl_);
    if (res != CURLE_OK) {
        std::cerr << "curl_easy_perform() failed: " << curl_easy_strerror(res) << std::endl;
        return SdkCode::kErrorCURL;
    }

    long http_code = 0;
    curl_easy_getinfo(curl_, CURLINFO_RESPONSE_CODE, &http_code);
    if (http_code != 200) {
        std::cerr << "HTTP request failed with code " << http_code << ", response: " << read_buffer << std::endl;
        return SdkCode::kFailSendProxy;
    }

    return SdkCode::kSuccess;
}

} // namespace inlong
