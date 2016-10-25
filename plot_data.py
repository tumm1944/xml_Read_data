import numpy as np
import matplotlib.pyplot as plt
import sys

data = np.genfromtxt('data_coffee_icecream_GA.txt', delimiter = ' ')
zip_zip = data[:,1]
pop_zip = data[:,2]
coffee_results = data[:,3]
icecream_results = data[:,4]

for i in range(len(data)):
    if coffee_results[i]==0:
        coffee_results[i]=1
    if icecream_results[i]==0:
        icecream_results[i]=1

zip_zip          = np.array((zip_zip))
pop_zip          = np.array((pop_zip))
coffee_results   = np.array((coffee_results))
icecream_results = np.array((icecream_results))

coffee_stack  =  np.column_stack((zip_zip,pop_zip/coffee_results))
icecream_stack = np.column_stack((zip_zip,pop_zip/icecream_results))

sort_col=1
coffee_stack_sorted   = coffee_stack[coffee_stack[:,sort_col].argsort()]
icecream_stack_sorted = icecream_stack[icecream_stack[:,sort_col].argsort()]


#for i in range(len(data)):
    #print i,int(coffee_stack_sorted[i,0]),coffee_stack_sorted[i,1]
    #print int(icecream_stack_sorted[i,0]),icecream_stack_sorted[i,1]

#sys.exit(0)

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
