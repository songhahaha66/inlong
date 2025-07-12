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

#ifndef INLONG_SDK_HTTP_CLIENT_H
#define INLONG_SDK_HTTP_CLIENT_H

#include <curl/curl.h>
#include <string>
#include <memory>
#include <cstdint>
#include "../utils/capi_constant.h"

namespace inlong {

class HttpClient {
public:
    HttpClient(std::string url, uint64_t timeout);
    ~HttpClient();

    int32_t Send(const std::string& group_id, const std::string& stream_id, const std::string& msg);
    bool Init();
    void Close();

private:
    static size_t WriteCallback(void* contents, size_t size, size_t nmemb, void* userp);

    std::string url_;
    uint64_t timeout_;
    CURL* curl_;
};

} // namespace inlong

#endif //INLONG_SDK_HTTP_CLIENT_H
