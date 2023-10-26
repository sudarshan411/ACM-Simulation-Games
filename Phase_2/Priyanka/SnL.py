import numpy as np
import random
import pandas as pd

#defining an initial matrix
init_matrix=np.zeros((1, 101))
init_matrix[0][0]=1

#defining a 101 x 101 transition matrix using for loop
#it's not necessary to roll the dice such that the the token lands exactly on 100 to win

#basic board without Snakes and Ladders
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


#snakes and ladder included in following form
#    Ladders        Snakes
#  from    to     from    to 
#   3      19      11     7
#   15     37      18     13
#   22     42      28     12
#   25     64      36     34 
#   41     73      77     16
#   53     74      47     26
#   63     86      83     39
#   76     91      92     75
#   84     98      99     70

#defining ladder and snakes as dictionaries
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

#Changing T matrix with respect to Snakes and Ladder
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

#Calculating Probability distribution

#Calculating n-step transition matrix

n=int (input("Enter no. of steps : "))
T_n=T

i=0
while i<n:
    T_n=np.matmul(T_n,T)
    i+=1
#A_n is the n step transition matrix

#to find the probability of finishing the game in n steps

P=np.matmul(init_matrix,T_n)

print ("The Probability of finishing game in ", n, "steps is : \n",P[0][100])
