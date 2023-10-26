import numpy as np
import matplotlib.pyplot as plt

class SNL_Board:
    """Just a regular Snakes and Ladders Board"""
    
    def __init__(self,dim):
        '''Initialize the SNL Board by entering the (dimension) of the board'''
        self.dim = dim
        self.transition_matrix = np.zeros((dim**2+1,dim**2+1))
        # Set transition_matrix[0][1] because first move is always to 
        # move the piece onto the board
        
        self.transition_matrix[0][1] = 1
        # Transition matrix is created and all the values are set for 
        # a board without any snakes or ladders
        
        for i in range(1,dim**2+1):
            remaining = 0
            number = 6

            # If number of spaces left ahead is less than 6, the higher rolls
            # become invalid, so the remaining probability the player stays 
            # on the same space itself
            if((dim**2)-i)<6:
                number = (dim**2)-i
                remaining = 1-(number/6)
            self.transition_matrix[i][i] = remaining
            
            # Set the 6 transition probabilities for the 6 dice values
            for j in range(1,number+1):
                self.transition_matrix[i][i+j] = 1/6
        # Initialize state vector with the player outside the board, i.e at 0
        self.state_vector = np.zeros(dim**2+1)
        self.state_vector[0] = 1
        self.number_of_moves=0
            
    def Add_Snake(self,Snakes):
        '''Add snakes to the board by entering the [[Start],[End]] locations 
        of the snakes throught a 2D array'''
        n = len(Snakes[0])
        i=0
        while i<n:
            x = Snakes[0][i]
            y = Snakes[1][i]
            i += 1
            # We add a snake only if valid start and end are input, i.e, end is 
            # below the start on the board
            if (y<=(x-x%10)):
                number = 6
                self.transition_matrix[x][x] = 0
                
                # We remove the normal transitions to x and change them to y
                for j in range(1,number+1):
                    self.transition_matrix[x-j][x] = 0
                    self.transition_matrix[x-j][y] = 1/6
            
    def Add_Ladder(self,Ladders):
        '''Add ladders to the board by entering the [[Start],[End]] locations 
        of the ladder throught a 2D array'''
        n = len(Ladders[0])
        i=0
        while i<n:
            x = Ladders[0][i]
            y = Ladders[1][i]
            i += 1
            # We add a ladder only if valid start and end are input, i.e, end is 
            # above the start on the board
            if (y>((x+10)-x%10)):
                number = 6
                if x<=6:
                    number = x-1
                    self.transition_matrix[x][x] = 0
            
                # We remove the normal transitions to x and change them to y
                for j in range(1,number+1):
                    self.transition_matrix[x-j][x] = 0
                    self.transition_matrix[x-j][y] = 1/6
            
    def Move_Player(self):
        '''Multiply state vector with transition matrix and increase the 
        number_of_moves value by 1'''
        self.state_vector = np.matmul(self.state_vector,self.transition_matrix)
        self.number_of_moves = self.number_of_moves + 1
    
# We crete an instance of the SNL_Board class with a 10X10 board dimensions
Board = SNL_Board(10)

# We create the 2D arrays storing the start and end point of all the snakes
# and ladders on the board
Snakes = np.array([[98,95,93,87,68,64,62,49,47,16],
                   [78,75,73,24,53,60,19,11,26,6]])
Ladders = np.array([[2,4,9,21,28,36,51,71,80],[38,14,31,42,84,44,67,91,100]])

# We add all the snakes and ladders to the board
Board.Add_Snake(Snakes)
Board.Add_Ladder(Ladders)

# Store the winning probability for each number of moves to be 
# able to plot later
win_probabilities = np.array([])   
average_to_win = 0
probability_sum = 0

# Calculate the average number of moves to win, as well as store all the
# winning probabilities in the same loop
for i in range(0,Board.dim**2):
    Board.Move_Player()
    average_to_win += Board.state_vector[Board.dim**2]*Board.number_of_moves
    probability_sum += Board.state_vector[Board.dim**2]
    win_probability = 100*Board.state_vector[Board.dim**2]
    win_probabilities = np.append(win_probabilities,win_probability)

average_to_win = average_to_win/probability_sum

# Plot the winning probabilities in percentage with the number of moves needed
print(f"The average number of moves needed to win is {average_to_win}")
plt.plot(win_probabilities)
plt.title("Probablity of winning")
plt.ylabel("Probability(in %)")
plt.xlabel("No. of Turns")
plt.xticks(range(0,101,10))
plt.yticks(range(0,101,10))
plt.show()

