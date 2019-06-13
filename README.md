# aod-accounting

This repository contains the REST API for extracting accounting record about the `EGI Applications on Demand (AoD)` service from the `EGI Accounting portal`.

## Requirements

* Be manager of the `vo.access.egi.eu` VO
* Install the `requests_pkcs12` python library
* Basic knowledge of the `json`, `os` and the `[PKCS#12 requests_pkcs12]` python libraries are requested
* Python v2.7.12+

## Installation of the PKCS#12 support for requests

This library is available as PyPI package:

<pre>
]$ pip install requests_pkcs12
</pre>

Alternatively, you can retrieve the latest development version via git:

<pre>
]$ git clone https://github.com/m-click/requests_pkcs12
</pre>


## Usage 

For simple one-off requests you can use this library as a drop-in replacement for the requests library:

<pre>
from requests_pkcs12 import get

r = get('https://example.com/test', 
         pkcs12_filename='clientcert.p12', 
         pkcs12_password='your_secret_password_here')
</pre>

## Reference
* [PKCS#12 support for requests] (https://github.com/m-click/requests_pkcs12)

## License
Licensed under the Apache License, Version 2.0 (the "License"); you may not use this project except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0.

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.



