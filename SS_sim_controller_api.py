import requests
import math, json

'''
three parts
1. GUI - simple, just triggering sim situations
2. logic - processing the sim starts, through SS API
3. settings - just through API as well

functions so far
	set and pull props from SS
'''

smsp_ip_addr = ["localhost"]
# smsp_ip_addr = ["3.144.25.48"]
def set_ip(ip):
	# print(ip)
	smsp_ip_addr.clear()
	smsp_ip_addr.append(ip)
	# print("IP Address set to " + smsp_ip_addr)


def get_object_property(type_name, object_name, property_name):
	if "http" in smsp_ip_addr[0]:
		url = smsp_ip_addr[0] + "/SmartSpaceApi/api/ObjectProperties/" + type_name + "/" + object_name + "/" + property_name
	else:
		url = "http://" + smsp_ip_addr[0] + "/SmartSpaceApi/api/ObjectProperties/" + type_name + "/" + object_name + "/" + property_name
	# print(url)
	res = requests.get(url, verify=False)
	data = res.json()
	result = str(data.get("PropertyValue"))
	# strip off the leading path if exists
	if "/" in result:
		split_result = result.split("/")
		result = split_result[1]
	# print(result)
	return result


def set_object_property(type_name, object_name, property_name, new_prop_val):
	print("Setting " + property_name + " for " + object_name + " to " + new_prop_val)
	if "http" in smsp_ip_addr[0]:
		url = smsp_ip_addr[0] + "/SmartSpaceApi/api/ObjectProperties/" + type_name + '/' + object_name + '/' + property_name
	else:
		url = "http://" + smsp_ip_addr[0] + "/SmartSpaceApi/api/ObjectProperties/" + type_name + '/' + object_name + '/' + property_name
	# print(url)
	request_body = '"' + new_prop_val + '"'
	headers = {"Content-Type": "application/json"}
	response_code = requests.put(url, data=request_body, headers=headers, verify=False)
	print(response_code)  # response code: 200=success, 400=prop could not be set
	return response_code


def get_object_location(type_name, object_name):
	if "http" in smsp_ip_addr[0]:
		url = smsp_ip_addr[0] + "/SmartSpaceApi/api/ObjectLocations/" + type_name + "/" + object_name
	else:
		url = "http://" + smsp_ip_addr[0] + "/SmartSpaceApi/api/ObjectLocations/" + type_name + "/" + object_name
	# print(url)
	res = requests.get(url, verify=False)
	data = res.json()
	object_name = str(data.get("Object"))
	# strip off the leading path if exists
	if "/" in object_name:
		split_name = object_name.split("/")
		object_name = split_name[1]
	result = {object_name: (str(data.get("X")), str(data.get("Y")), str(data.get("Z")), str(data.get("Theta")))}
	# print(result)
	return result


def set_object_location(type_name, object_name, x, y, z, theta):
	print("Setting location for " + object_name + " to " + str(x) + ", " + str(y) + ", " + str(z) + ", " + str(theta))
	if "http" in smsp_ip_addr[0]:
		url = smsp_ip_addr[0] + "/SmartSpaceApi/api/ObjectLocations/" + type_name
	else:
		url = "http://" + smsp_ip_addr[0] + "/SmartSpaceApi/api/ObjectLocations/" + type_name
	# print(url)
	request_body = json.dumps([{"Object":type_name+'/'+object_name, "X":x, "Y":y, "Z":z, "Theta":theta}])
	headers = {"Content-Type": "application/json"}
	response_code = requests.put(url, data=request_body, headers=headers, verify=False)
	print(response_code)  # response code: 200=success, 400=loc could not be set
	return response_code


def tag_button_out_in(type_name, object_name, out_x, out_y, out_z, in_x, in_y, in_z, theta):
	set_object_location(type_name, object_name, out_x, out_y, out_z, theta)
	set_object_location(type_name, object_name, in_x, in_y, in_z, theta)


def reset_obj_to_loc(type_name, object_name, x, y, z, theta, new_sim_target):
	set_object_property(type_name, object_name, "sim_target_null_flag", "true")
	set_object_location(type_name, object_name, x, y, z, theta)
	# set_object_property(type_name, object_name, "simulation_target", new_sim_target)

