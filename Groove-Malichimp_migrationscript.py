import sys
import sqlite3
import json
import pprint
import requests

#email,name,href
pp = pprint.PrettyPrinter(indent=4)

conn = sqlite3.connect('local.db')
c = conn.cursor()
c.execute('''CREATE TABLE groove_table
             (email text, name text, href text)''')

url = 'https://api.groovehq.com/v1/me?'
header = {'Authorization': ________________}
request = requests.get(url, headers=header)
#print(request.url)
data = request.json()
print(request.status_code)
#pp.pprint(data)

url = 'https://api.groovehq.com/v1/customers?'
customers = requests.get(url, headers=header)
customer_data = customers.json()
print(customers.status_code)
#pp.pprint(customer_data)

meta = customer_data['meta']
pagination = meta['pagination']

meta_value_dict = dict()

i = 0
for value in pagination.itervalues():
	meta_value_dict[i] = value
	i+=1

total_count = meta_value_dict[0]
next_page = meta_value_dict[1]
current_page = meta_value_dict[2]
total_pages = meta_value_dict[3]
last_page_count = total_count - (50 * (total_pages - 1))
int(total_pages)

#print(total_count)
#print(next_page)
#print(current_page)
#print(total_pages)
#print(last_page_count)

i=0
data = customer_data['customers']
url = 'https://api.groovehq.com/v1/customers?'
for i in range(0, total_pages):
	for j in range(0, len(data)):
 		data_value = data[j]
 		email = data_value['email']
 		name = data_value['name']
 		href = data_value['href']
 		c.execute("INSERT INTO groove_table VALUES (?, ?, ?)", (email, name, href))
 		#print(name)
 		#print(email)
 		#print(href)
   		#pp.pprint(data_value)
   	i+=1
   	#print(i)	
   	payload = { 'page': i }
	customers = requests.get(url, headers=header, params=payload)
	#print(customers.url)
	#print(customers.status_code)
	customer_data = customers.json()
	data = customer_data['customers']


print(total_pages)
def get_posts():
    c.execute("SELECT * FROM groove_table")
    pp.pprint(c.fetchall())

#get_posts()


url = 'https://us8.api.mailchimp.com/3.0/lists/'
mailchimp = requests.get(url, auth=('apikey', 'a199977272cb8c8809cc4967397a9fc9'))
mailchimp_data = mailchimp.json()
#pp.pprint(mailchimp_data)
total_items = mailchimp_data['total_items']
int(total_items)
lists = mailchimp_data['lists']
for i in range(0, total_items):
	mailing_list = lists[i]
	name = mailing_list['name']
	if (name == 'Terbium Labs Newsletter'):
		print(name)
		list_id = mailing_list['id']
		url = 'https://us8.api.mailchimp.com/3.0/lists/%s/members/' %list_id
		#print(url)
		#print(list_id)
		c.execute("SELECT * FROM groove_table")
		for i in range(0,total_count):
			row = c.fetchone()
			val1 = (row[0])
			val2 = (row[1])
			val3 = ""
			data = json.dumps({ "email_address": "%s" %val1, "status": "subscribed", 
				"merge_fields": { "FNAME": "%s" %val2, "LNAME": "%s" %val3 }})
			pp.pprint(data)
			requests.post(url, auth=('apikey', 'a199977272cb8c8809cc4967397a9fc9'), data=data)
		print("success")	









