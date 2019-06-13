# aod-accounting

This repository contains the REST API for extracting accounting record about the `EGI Applications on Demand (AoD)` service from the `EGI Accounting portal`.

## Requirements

* Be manager of the `vo.access.egi.eu` VO
* Install the `requests_pkcs12` python library
* Basic knowledge of the `json`, `os` and the `PKCS#12 requests_pkcs12` python libraries are requested
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

<pre>
]$ python aod-accounting.py 

[.] Get accounting records from the EGI Accounting portal
[ Request ] = https://accounting.egi.eu/vo_admin/cloud/vo.access.egi.eu/sum_elap_processors/UserDN/DATE/2015/6/2019/6/JSON

[ Response ]
[..]

[+] Metric: Elapsed time * Number of Processors (hours) by User DN and Month 

[ Accounting record ]
[-] {"2018-02": 0, "2018-05": 48960.3822, "Percent": 44.37, "2017-05": 0, "2018-12": 71328.3711, "2018-07": 35711.0244, "2018-10": 35760.2244, "2018-11": 459075.7156, "2018-06": 34560.7622, "id": "/C=IT/O=INFN/OU=Robot/L=Catania/CN=Robot: Catania Science Gateway - Roberto Barbera/CN=eToken:025166931789a0f57793a6092726c2ad89387a4cc167e7c63c5d85fc91021d18@egi.eu", "2019-02": 64511.8978, "2019-03": 67058.0378, "2019-01": 71519.5444, "2019-06": 0, "2019-04": 5074.5222, "2019-05": 0, "2017-12": 32064.0667, "2017-11": 83360.2533, "2017-10": 74875.2114, "2016-10": 0, "2016-11": 0, "2016-12": 0, "2018-09": 34655.2556, "2018-08": 35616.3311, "2017-08": 0, "2017-09": 380.08, "2018-01": 22752.6994, "2017-01": 0, "2017-02": 0, "2017-03": 0, "2017-04": 0, "2018-04": 21311.72, "2017-06": 0.19, "2017-07": 0, "2016-04": 0, "Total": 1284353, "2018-03": 85776.2311, "2016-09": 0}
[-] user_id = /C=IT/O=INFN/OU=Robot/L=Catania/CN=Robot: Catania Science Gateway - Roberto Barbera/CN=eToken:025166931789a0f57793a6092726c2ad89387a4cc167e7c63c5d85fc91021d18
[-] Total Elapsed time * Number of Processors (hours) by User DN and Month = 1284353 hours
[ WARNING ] The user DN exceeded the allocated service grant!

=========================== [ Report ] ========================== 
[-] EGI AoDs service grant for the given period: 2015/6 - 2019/6 
[-] Max service grant (vCPU cores * days * 24h) = 140256
[-] The following DN(s) exceeded the EGI AoDs resource usage limit:
/C=IT/O=INFN/OU=Robot/L=Catania/CN=Robot: Catania Science Gateway - Roberto Barbera/CN=eToken:025166931789a0f57793a6092726c2ad89387a4cc167e7c63c5d85fc91021d18 [1284353] 
==================================================================
</pre>

For simple one-off requests you can use this library as a drop-in replacement for the requests library:

<pre>
from requests_pkcs12 import get

r = get('https://example.com/test', 
         pkcs12_filename='clientcert.p12', 
         pkcs12_password='your_secret_password_here')
</pre>



## License
Licensed under the Apache License, Version 2.0 (the "License"); you may not use this project except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0.

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.



## References
[PKCS#12 support for requests](https://github.com/m-click/requests_pkcs12)

[EGI Applications on Demand (AoD) service](https://www.egi.eu/services/applications-on-demand/)

[EGI Accounting portal](https://www.accounting.egi.eu/)

