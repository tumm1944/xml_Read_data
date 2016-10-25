import numpy as NP
import foursquare as FS
from xlrd import open_workbook
import sys
import us
import re
import matplotlib.pyplot as plt
import operator

pop_zip = []
zip_zip = []
coffee_results = []
icecream_results = []
state='GA'
MY_API_KEY='b774ad247ad91ffd1f05bf996dc13d4f861a6b5f'

API_VERSION_YEAR  = '2015'
API_VERSION_MONTH = '05'
API_VERSION_DAY   = '26'
API_VERSION = '{year}{month}{day}'.format(year=API_VERSION_YEAR, month=API_VERSION_MONTH, day=API_VERSION_DAY)

# Construct the client object
FS_client = FS.Foursquare(client_id='W5LY0JEJHWMGO00GYZEBC1X2MNYXQEZDKELJ3SDCSWZDZGB4', client_secret='ZTAA51NH3L5CKHMVJNYGD2UTFRKMBYMIVOKRUZPGYXHE51PT', version=API_VERSION)

#getting population

State_id=us.states.GA.fips
get_population = 'http://api.census.gov/data/2010/sf1?key=b774ad247ad91ffd1f05bf996dc13d4f861a6b5f&get=P0010001&for=zip+code+tabulation+area:*&in=state:'+State_id

import urllib2
population = urllib2.urlopen(get_population)

population.readline()
count_line=0
for line in population:
    count_line=count_line+1
    tmp = line.strip()[1:-2]
    tmp = tmp.translate(None, '"')
    tmp = tmp.split(',')
    pop_zip.append(int(tmp[0]))
    zip_zip.append(int(tmp[-1]))
#    if count_line==10:
#break

#print pop_zip
#print zip_zip
#print population

#sys.exit(0)
book = open_workbook('zip_code_database.xls',on_demand=True)
sheet = book.sheet_by_name('zip_code_database')

for count in range(len(pop_zip)):
    row=0
    for cell in sheet.col(0):
        cell_value=cell.value
        row=row+1
        if cell_value==zip_zip[count]:
            l1=sheet.cell(row,9).value
            l2=sheet.cell(row,10).value
            break

    ll = str(l1)+", "+str(l2)
#ll='33.8,-84.3'
#print ll
    response_1=FS_client.venues.explore(params={'ll':ll, 'query': 'coffee'})
#print response_1.keys()
#print response_1['totalResults']
    response_2=FS_client.venues.explore(params={'ll':ll, 'query': 'Ice Cream'})
    if int(response_1['totalResults']) == 0:
        coffee_results.append(1)
    else:
        coffee_results.append(int(response_1['totalResults']))
    if int(response_2['totalResults']) == 0:
        icecream_results.append(1)
    else:
        icecream_results.append(int(response_2['totalResults']))
    #print count, zip_zip[count], pop_zip[count],coffee_results[count],icecream_results[count]
#sys.exit(0)
#print response_2['totalResults']

book.unload_sheet('zip_code_database')

zip_zip          = NP.array((zip_zip))
pop_zip          = NP.array((pop_zip))
coffee_results   = NP.array((coffee_results))
icecream_results = NP.array((icecream_results))

coffee_stack  =  NP.column_stack((zip_zip,pop_zip/coffee_results))
icecream_stack = NP.column_stack((zip_zip,pop_zip/icecream_results))

sort_col=1
coffee_stack_sorted   = coffee_stack[coffee_stack[:,sort_col].argsort()]
icecream_stack_sorted = icecream_stack[icecream_stack[:,sort_col].argsort()]

zips = coffee_stack_sorted[(len(data)-35):,0]
zips = [int(x) for x in zips]
plt.bar([x+1 for x in range(len(zips))], coffee_stack_sorted[(len(data)-35):,1], color='g', align='center')
plt.ylabel('People per Coffee Shop')
plt.xlabel('Zipcode')
plt.xticks([x+1 for x in range(len(zips))], zips, rotation=90)
plt.title('Coffee Shops')

plt.show()

zips = icecream_stack_sorted[(len(data)-35):,0]
zips = [int(x) for x in zips]
plt.bar([x+1 for x in range(len(zips))], icecream_stack_sorted[(len(data)-35):,1], color='b', align='center')
plt.ylabel('People per Ice cream Shop')
plt.xlabel('Zipcode')
plt.xticks([x+1 for x in range(len(zips))], zips, rotation=90)
plt.title('Ice cream Shops')
plt.show()

#print coffee_stack_sorted
#print icecream_stack_sorted

#print FS_client.venues('40a55d80f964a52020f31ee3')
#FS_client.api.venues.search(params={'ll':33.78,-84.38})
#Quandl API key #5pVgyb9jK7Jz2vZtSaXy
#Census Data API. Your API key is b774ad247ad91ffd1f05bf996dc13d4f861a6b5f
