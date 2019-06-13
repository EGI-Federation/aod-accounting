#!/usr/bin/env python
#
#  Copyright 2019 EGI Foundation
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
#

from datetime import date
from requests_pkcs12 import get
import json, os

__author__    = "Giuseppe LA ROCCA"
__email__     = "giuseppe.larocca@egi.eu"
__version__   = "$Revision: 0.0.1"
__date__      = "$Date: 12/06/2019 14:39:22"
__copyright__ = "Copyright (c) 2019 EGI Foundation"
__license__   = "Apache Licence v2.0"

SERVER_URL = "https://accounting.egi.eu"
VO_NAME = "vo.access.egi.eu"

DATE_FROM = "2015/6"
DATE_TO = "2019/6"

USER_DN = "/C=IT/O=INFN/OU=Robot/L=Catania/CN=Robot: Catania Science Gateway - Roberto Barbera/CN=eToken:025166931789a0f57793a6092726c2ad89387a4cc167e7c63c5d85fc91021d18"

# This array contains the list of unique Per-User Sub-Proxy DNs.
# For each DN it will be extracted the accounting record using 
# one of the available metric (see below).
DNs_list = []

# This array will contain the list of Per-User Sub-Proxy DNs 
# to be banned since they have overused the allocated service grant.
ban_list = []

# Available metrics	:
# 'vm_num'		: Total number of VM run by User DN and Month
# 'sumelap'		: Total elapsed time (hours) by User DN and Month
# 'sum_elap_processors'	: Elapsed time * Number of Processors (hours) by User DN and Month
# 'cost'		: Monetary Cost (euros) by User DN and Month
# 'net_in'		: Inbound Network Traffic (b) by User DN and Month
# 'net_out'		: Outbound Network Traffic (b) by User DN and Month
# 'mem-GByte'		: Memory Used (GBytes) by User DN and Month
# 'disk'		: Disk Used (b) by User DN and Month
METRIC_NAME = "sum_elap_processors"

# Cores allocated to each authorized user of the EGI AoDs
GRANTED_CORES = 4

def getDetails(metric):
	''' Define banner and metric unit '''

	if (METRIC_NAME == "vm_num"):
		banner = "Total number of VM run by User DN and Month"
		unit = "num"
	
	if (METRIC_NAME == "sumelap"):
		banner = "Total elapsed time (hours) by User DN and Month"
		unit = "hours"

        if (METRIC_NAME == "sum_elap_processors"):
                banner = "Elapsed time * Number of Processors (hours) by User DN and Month"
                unit = "hours"

	if (METRIC_NAME == "cost"):
		banner = "Monetary Cost (\u20ac35) by User DN and Month"
		unit = "\u20ac35"

	if (METRIC_NAME == "net_in"):
		banner = "Inbound Network Traffic (b) by User DN and Month"
		unit = "bandwidth"
	
	if (METRIC_NAME == "net_out"):
		banner = "Outbound Network Traffic (b) by User DN and Month"
		unit = "bandwidth"
	
	if (METRIC_NAME == "mem-GBytes"):
		banner = "Memory Used (GBytes) by User DN and Month"
		unit = "GBytes"
	
	if (METRIC_NAME == "disk"):
		banner = "Disk Used (b) by User DN and Month"
		unit = "bandwidth"

	return banner, unit


def getServiceGrant(date_from, date_to):
	''' Get the service grant for the given period '''

	_from = date(int(date_from[:4]), int(date_from[5:]), 1)
	_to = date(int(date_to[:4]), int(date_to[5:]), 1)
	delta = (_to - _from)
	
	return (GRANTED_CORES * delta.days * 24)


def connect(server_url, vo_name, date_from, date_to, metric):
	''' Connecting to the EGI Accounting Portal '''

	request = "%s/vo_admin/cloud/%s/%s/UserDN/DATE/%s/%s/JSON" %(server_url, vo_name, metric, date_from, date_to)
	print ("[ Request ] = %s" %request)
	
	curl = get(request, 
                   pkcs12_filename="%s/.globus/INFN.p12" %os.environ['HOME'], 
                   pkcs12_password='giuseppelarocca')

	data = curl.json()

	return data


def getDNs(server_url, vo_name, date_from, date_to, metric):
	''' Get the list of unique DNs '''

	print ("\n[.] Get list of DNs from the EGI Accounting portal")
	data = connect(server_url, vo_name, date_from, date_to, metric)

	for record in data:
		if "CN=Robot:" in record['id']:
			if record['id'] not in DNs_list:
				DNs_list.append(record['id'])
	
	return DNs_list



def getMetrics(server_url, vo_name, date_from, date_to, DNs_list, metric, max_service_grant):
	''' Retrieve accounting usage from the Accounting Portal records '''
	
	print ("\n[.] Get accounting records from the EGI Accounting portal")
	data = connect(server_url, vo_name, date_from, date_to, metric)

	print ("\n[ Response ]")
	print ("- %s" %json.dumps(data))

	print ("\n[+] Metric: %s " %getDetails(metric)[0])

	for user_id in DNs_list:
		total = 0
		for record in data:
			if (user_id in record['id']):
				if (int(record['Total']) > total):
					total = int(record['Total'])
					metric = json.dumps(record)
		
		print ("\n[ Accounting record ]")
		print ("[-] %s" %metric)
		print ("[-] user_id = %s" %user_id)
		print ("[-] Total %s = %d %s" %(getDetails(metric)[0], total, getDetails(metric)[1]))
		if (total > max_service_grant):
			print ("[ WARNING ] The user DN exceeded the allocated service grant!")
			if user_id not in ban_list:
				ban_list.append(user_id + " [%s] " %total)


def main():

	# Calculate the service grant from the given dates
	MAX_SERVICE_GRANT = getServiceGrant(DATE_FROM, DATE_TO)

	# Configure the array with the list of PUSP DNs of which accounting records 
	# will be calculated from the EGI Accounting portal

	#DNs_list.append(USER_DN)
	DNs_list = getDNs(SERVER_URL, VO_NAME, DATE_FROM, DATE_TO, METRIC_NAME)
	
	# Get the accounting records from the EGI Accounting portal
	getMetrics(SERVER_URL, VO_NAME, DATE_FROM, DATE_TO, DNs_list, METRIC_NAME, MAX_SERVICE_GRANT)
	
	if len(ban_list) != 0:
		print ("\n=========================== [ Report ] ========================== ")
		print ("[-] EGI AoDs service grant for the given period: %s - %s " %(DATE_FROM, DATE_TO))
		print ("[-] Max service grant (vCPU cores * days * 24h) = %s" %MAX_SERVICE_GRANT)
		print ("[-] The following DN(s) exceeded the EGI AoDs resource usage limit:")
		print ("\n". join(ban_list))
		print ("================================================================== ")

if __name__ == "__main__":
        main()


