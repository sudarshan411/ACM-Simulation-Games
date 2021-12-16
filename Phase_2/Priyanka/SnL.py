import numpy as np
import random
import pandas as pd

#define a dictionary of 101 states ranging from 0 to 100 representing every possible square using for loop
state={ }
i=0
for i in range (0,100):
	state[i]=str(i)
	i=i+1
state[100]="Win..!!"

#define a 101x101 transition matrix using for loop
#it's not necessary to roll a dice such the player should land exactly on 100 to win 

#basic board without Snakes and Ladder
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
				T[row][col]=((6-(99-row))*(1/6))
			col+=1
	else:
		T[100][100]=1
	row+=1

print (T[0,:])
#snakes and ladder included in following form
#    Ladders        Snakes
#  from    to    from    to 
#   3      19      11     7
#   15     37      18     13
#   22     42      28     12
#   25     64      36     34 
#   41     73      77     16
#   53     74      47     26
#   63     86      83     39
#   76     91      92     75
#   84     98      99     70

ladder={
        3:19,
        15:37,
        22:42,
        25:64,
        41:73,
        53:74,
        63:86,
        76:91,
        84:98
        }
snakes= {
        11:7,
        18:13,
        28:12,
        36:34,
        77:16,
        47:26,
        83:39,
        92:75,
        99:70
        }
for i in range (0,101):
        for j in ladder.keys():
                if (T[i][j]!=0):
                        T[i][ladder[j]]+=(1.0/6)
                        T[i][j]=0
        i=i+1
        
for i in range (0,101):
         for j in snakes.keys():
                 if (T[i][j]!=0):
                         T[i][snakes[j]]+=(1.0/6)
                         T[i][j]=0
         i=i+1

print (T[0,:])
df = pd.DataFrame(T)
print (df)
#board with SnL
s=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100]
start_state=0
steps=0
print (state[start_state],"---->", end= " ")
prev_state=start_state
curr_state=prev_state
while (curr_state!=100):
	curr_state=np.random.choice(s,p=T[prev_state])
	if (curr_state<100):
		print (state[curr_state],"---->", end= " ")
	else:
		print (state[curr_state])
	prev_state=curr_state
	steps+=1
print ("\n\n",steps)
