import numpy as np
import random

#define a dictionary of 101 states ranging from 0 to 100 representing every possible square using for loop
state={ }
i=0
for i in range (0,101):
	state[i]=str(i)
	i=i+1

#define a 101x101 transition matrix using for loop

T=np.zeros((101,101),dtype=float)
row=0
col=0
for row in range(0,101):
	if (row<95):
		for col in range(0,101):
			if ((col<(row+7)) and (col>(row))):
				T[row][col]=(1.0/6)
			col+=1
	elif ((row>94) and (row!=100)):
		for col in range(0,101):
			if ((col != (100 ) and (col>(row)))):
				T[row][col]=(1.0/6)
			elif (col==100):
				T[row][col]=((6-(100-col))*(1.0/6))
			col+=1
	row+=1
print (T)
