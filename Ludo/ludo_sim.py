import numpy as np
import matplotlib.pyplot as plt
import random


class ludo_board:
    """Just a ludo board"""
    def __init__(self):
        self.players = []
        self.available_colors = {"Red":39,"Green":26,"Yellow":13,"Blue":0}
        self.board = []
        self.roll = 0 
        for i in range(0,52):
            self.board.append("n")
        self.capture_dict = {"capturing player":[], "captured player": [], 
                             "capture spot":[], "capture roll": []}
        
class player:
    """Just a regular player"""
    def __init__(self,name,color,ludo_board):
        name = name.title()
        color = color.title()
        self.start = ludo_board.available_colors[color]
        self.name = name
        self.color = color
        ludo_board.players.append(self)
        self.ludo_board = ludo_board
        self.initial = []
        for i in range(1,5):
            self.initial.append(color[0] + str(i))
        self.inner = []
        for i in range(0,5):
            self.inner.append("n")
        self.end = []
        self.moves = 0
        self.rolls = 0

    def move_greed(self,x,strategy,risk_location,attack_opportunities):
        
        self.rolls += 1
        #print(x)
        before = self.moves
        if (strategy=="careless") and (len(attack_opportunities)!=0):
            start_range = attack_opportunities[0]
            end_range = attack_opportunities[0]+1
        elif (risk_location!=-1):
            start_range = risk_location
            end_range = risk_location+1
        elif (strategy=="careful") and (len(attack_opportunities)!=0):
            start_range = attack_opportunities[0]
            end_range = attack_opportunities[0]+1
        else:
            start_range = self.start+0
            end_range = self.start+52
        if (x==6) and (self.ludo_board.board[self.start][0]!=self.color[0]) and (self.initial):
            '''Check here for a capture function '''
            if self.ludo_board.board[self.start][0]!= 'n':
                self.capture(self.start)
            s = self.initial[0]
            del self.initial[0]
            self.ludo_board.board[self.start] = s
            self.moves += 1
        else:
            
            for i in range(start_range,end_range):
                i = i%52
                if self.ludo_board.board[i][0]!=self.color[0]:
                    continue
                if ((i+x) > ((self.start+50)%52)) and (i<=((self.start+50)%52)):
                    if (i==(self.start+50)%52) and (x==6):
                        s = self.ludo_board.board[i]
                        self.ludo_board.board[i] = 'n'
                        self.end.append(s)
                        self.moves += 1
                        break
                    else:
                        y = ((i+x)%52)%((self.start+50)%52)
                        y = y-1
                        if self.inner[y] == 'n':
                            s = self.ludo_board.board[i]
                            self.ludo_board.board[i] = 'n'
                            self.inner[y] = s
                            self.moves += 1
                            break
                elif self.ludo_board.board[i][0] == self.color[0]:
                    if self.ludo_board.board[(i+x)%52][0] != self.color[0]:
                        '''Check here for a capture function'''
                        if self.ludo_board.board[(i+x)%52][0] != 'n':
                            self.capture((i+x)%52)
                        s = self.ludo_board.board[i]
                        self.ludo_board.board[i] = 'n'
                        self.ludo_board.board[(i+x)%52] = s
                        self.moves += 1
                        break
        if before == self.moves:
            for i in range(0,5):
                if self.inner[i][0] != self.color[0]:
                    continue
                else:
                    if i+x==5:
                        s = self.inner[i]
                        self.inner[i] = 'n'
                        self.end.append(s)
                        self.moves += 1
                        break
                    elif i+x<5:
                        if self.inner[i+x]=='n':
                            s = self.inner[i]
                            self.inner[i] = 'n'
                            self.inner[i+x] = s
                            self.moves += 1
                            break

    def move_cautious(self, x):
        
        self.rolls += 1
        #print(x)
        before = self.moves
        for i in range(self.start+0,self.start+52):
            i = i%52
            if self.ludo_board.board[i][0]!=self.color[0]:
                continue
            if ((i+x) > ((self.start+50)%52)) and (i<=((self.start+50)%52)):
                if (i==(self.start+50)%52) and (x==6):
                    s = self.ludo_board.board[i]
                    self.ludo_board.board[i] = 'n'
                    self.end.append(s)
                    self.moves += 1
                    break
                else:
                    y = ((i+x)%52)%((self.start+50)%52)
                    y = y-1
                    if self.inner[y] == 'n':
                        s = self.ludo_board.board[i]
                        self.ludo_board.board[i] = 'n'
                        self.inner[y] = s
                        self.moves += 1
                        break
            elif self.ludo_board.board[i][0] == self.color[0]:
                if self.ludo_board.board[(i+x)%52][0] != self.color[0]:
                    '''Check here for a capture function'''
                    if self.ludo_board.board[(i+x)%52][0] != 'n':
                        self.capture((i+x)%52)
                    s = self.ludo_board.board[i]
                    self.ludo_board.board[i] = 'n'
                    self.ludo_board.board[(i+x)%52] = s
                    self.moves += 1
                    break
        if before == self.moves:
            if (x==6) and (self.ludo_board.board[self.start][0]!=self.color[0]) and (self.initial):
                '''Check here for a capture function'''
                if self.ludo_board.board[self.start][0]!= 'n':
                    self.capture(self.start)
                s = self.initial[0]
                del self.initial[0]
                self.ludo_board.board[self.start] = s
                self.moves += 1
            for i in range(0,5):
                if self.inner[i][0] != self.color[0]:
                    continue
                else:
                    if i+x==5:
                        s = self.inner[i]
                        self.inner[i] = 'n'
                        self.end.append(s)
                        self.moves += 1
                        break
                    elif i+x<5:
                        if self.inner[i+x]=='n':
                            s = self.inner[i]
                            self.inner[i] = 'n'
                            self.inner[i+x] = s
                            self.moves += 1
                            break
        
    def risk(self):
        max_risk = 0
        position = -1
        risk = 0
        for i in range(0,52):
            if self.ludo_board.board[i][0] == self.color[0]:
                risk = 0
                for j in range(1,7):
                    if self.ludo_board.board[(i-j)%52][0] != self.color[0]:
                        risk = risk + 1
                if(risk>max_risk):
                    max_risk = risk
                    position = i
        return position
    
    def attack_opportunity(self, x):
        positions = []
        for i in range(self.start+0,self.start+52):
            i = i%52
            if self.ludo_board.board[i][0] == self.color[0]:
                if(self.ludo_board.board[(i+x)%52][0] != 'n') and (self.ludo_board.board[(i+x)%52][0] != self.color[0]):
                    positions.append(i)
        return positions
    
    def move(self,choice):
        x = random.randint(1,6)
        self.ludo_board.roll = self.ludo_board.roll + 1
        risk_location = self.risk()
        attack_opportunities = self.attack_opportunity(x)
        if choice==1:
            self.move_greed(x,"careful",risk_location, attack_opportunities)
        if choice==2:
            self.move_cautious(x)
        if choice==3:
            self.move_greed(x,"careless",risk_location, attack_opportunities)
        if choice==4:
            y = random.randint(0,2)
            if y==0:
                self.move_greed(x,"careful",risk_location, attack_opportunities)
            elif y==1:
                self.move_greed(x,"careless",risk_location, attack_opportunities)
            else:
                self.move_cautious(x)
        
    def is_done(self):
        if len(self.end) == 4:
            return 1
        else:
            return 0
        
    def capture(self, capture_spot):
        s = self.ludo_board.board[capture_spot]
        for p in self.ludo_board.players:
            if p.color[0] == s[0]:
                enemy = p
                break
        enemy.initial.append(s)
        self.ludo_board.capture_dict["capturing player"].append(self.color)
        self.ludo_board.capture_dict["captured player"].append(enemy.color)
        self.ludo_board.capture_dict["capture spot"].append(capture_spot)
        self.ludo_board.capture_dict["capture roll"].append(self.ludo_board.roll)
        


choice = 2
winner = []
winner_rolls = []
capture_dicts = []
#choice = int(input("Choice: "))

sim_number = 1000
for ii in range(0,sim_number):
    
    ludo = ludo_board()
    player1 = player("Mark","red",ludo)
    player2 = player("Hari","blue",ludo)
    player3 = player("Wade","green",ludo)
    player4 = player("Bob", "yellow", ludo)
    
    #'''
    #print(player1.initial)
    #print(ludo.board)
    
    
    while (player1.is_done()==0) and (player2.is_done()==0) and (player3.is_done()==0) and (player4.is_done()==0):
        player1.move(1)
        player2.move(2)
        player3.move(3)
        player4.move(4)
        '''
        #print(f"player1.initial = {player1.initial}")
        #print(f"player2.initial = {player2.initial}")
        print(ludo.board)
        #print(f"player1.inner = {player1.inner}")
        print(f"player1.end = {player1.end}")
        #print(f"player2.inner = {player2.inner}")
        print(f"player2.end = {player2.end}")
        print(f"player3.end = {player3.end}")
        print(f"player4.end = {player4.end}")
        #print(player1.rolls)
        #'''
        
    #print(ludo.capture_dict)
    
    print(f"\r{(ii/sim_number)*100}",end="")
    
    capture_dicts.append(ludo.capture_dict)
    winner_rolls.append(player1.rolls + player2.rolls + player3.rolls + player4.rolls)
    
    if player1.is_done()==1:
        #print(f"{player1.name} wins!!!")
        #print(player1.rolls)
        winner.append(1)
        #winner_rolls.append(player1.rolls)
        
    elif player2.is_done()==1:
        #print(f"{player2.name} wins!!!")
        #print(player2.rolls)
        winner.append(2)
        #winner_rolls.append(player2.rolls)
    elif player3.is_done()==1:
        #print(f"{player3.name} wins!!!")
        #print(player3.rolls)
        winner.append(3)
        #winner_rolls.append(player3.rolls)
    elif player4.is_done()==1:
        #print(f"{player4.name} wins!!!")
        #print(player4.rolls)
        winner.append(4)
        #winner_rolls.append(player4.rolls)


careful_greed = 0
careful_greed_rolls = 0
careful_greed_captures = 0
careful_greed_captured = 0
cautious = 0
cautious_rolls = 0
cautious_captures = 0
cautious_captured = 0
careless_greed = 0
careless_greed_rolls = 0
careless_greed_captures = 0
careless_greed_captured = 0
rando = 0
rando_rolls = 0
rando_captures = 0
rando_captured = 0

for ii in range(0,sim_number):
    if(winner[ii]==1):
        careful_greed = careful_greed + 1
        careful_greed_rolls = careful_greed_rolls + winner_rolls[ii]
    elif(winner[ii]==2):
        cautious = cautious + 1
        cautious_rolls = cautious_rolls + winner_rolls[ii]
    elif(winner[ii]==3):
        careless_greed = careless_greed + 1
        careless_greed_rolls = careless_greed_rolls + winner_rolls[ii]
    elif(winner[ii]==4):
        rando = rando + 1
        rando_rolls = rando_rolls + winner_rolls[ii]
        
    dic = capture_dicts[ii]
    for color in dic["capturing player"]:
        if(color == "Red"):
            careful_greed_captures = careful_greed_captures + 1
        elif(color == "Blue"):
            cautious_captures = cautious_captures + 1
        elif(color == "Green"):
            careless_greed_captures = careless_greed_captures + 1
        elif(color == "Yellow"):
            rando_captures = rando_captures + 1
    
    for color in dic["captured player"]:
        if(color == "Red"):
            careful_greed_captured = careful_greed_captured + 1
        elif(color == "Blue"):
            cautious_captured = cautious_captured + 1
        elif(color == "Green"):
            careless_greed_captured = careless_greed_captured + 1
        elif(color == "Yellow"):
            rando_captured = rando_captured + 1


labels = ["Cautious Greedy", "Cautious", "Careless Greedy", "Random"]
careful_greed = (careful_greed/sim_number)*100
cautious = (cautious/sim_number)*100
careless_greed = (careless_greed/sim_number)*100
rando = (rando/sim_number)*100

wins = [careful_greed, cautious, careless_greed, rando]
for w in wins:
    print(w)
print("\n\n")
fig = plt.figure(figsize = (10, 5))
plt.bar(labels, wins, color ='green', width = 0.4)
plt.xlabel("Player Strategy")
plt.ylabel("Percentage of wins")
plt.title("Winning chances for different playstyles")
plt.show()

careful_greed_rolls = (careful_greed_rolls/sim_number)
cautious_rolls = (cautious_rolls/sim_number)
careless_greed_rolls = (careless_greed_rolls/sim_number)
rando_rolls = (rando_rolls/sim_number)
roll_list = [careful_greed_rolls, cautious_rolls, careless_greed_rolls, rando_rolls]
for w in roll_list:
    print(w)
print("\n\n")
fig = plt.figure(figsize = (10, 5))
plt.bar(labels, roll_list, color ='maroon', width = 0.4)
plt.xlabel("Player Strategy")
plt.ylabel("Number of rolls to win")
plt.title("Average rolls to win for different playstyles")
plt.show()

careful_greed_captures = (careful_greed_captures/sim_number)
cautious_captures = (cautious_captures/sim_number)
careless_greed_captures = (careless_greed_captures/sim_number)
rando_captures = (rando_captures/sim_number)
captures_list = [careful_greed_captures, cautious_captures, careless_greed_captures, rando_captures]
for w in captures_list:
    print(w)
print("\n\n")

careful_greed_captured = (careful_greed_captured/sim_number)
cautious_captured = (cautious_captured/sim_number)
careless_greed_captured = (careless_greed_captured/sim_number)
rando_captured = (rando_captured/sim_number)
captured_list = [careful_greed_captured, cautious_captured, careless_greed_captured, rando_captured]
for w in captured_list:
    print(w)
print("\n\n")


fig = plt.figure(figsize = (10, 5))

barWidth = 0.25

X_axis = np.arange(len(labels))

plt.bar(X_axis - barWidth/2, captures_list, color ='g', width = barWidth,
        edgecolor ='grey', label ='Captured')
plt.bar(X_axis + barWidth/2, captured_list, color ='r', width = barWidth,
        edgecolor ='grey', label ='Lost')

plt.xticks(X_axis, labels)

#plt.bar(labels, captures_list, color ='blue', width = 0.4)
plt.xlabel("Player Strategy")
plt.ylabel("Number of pawns")
plt.title("Average number of timespawns captured or lost per game for different playstyles")
plt.legend()
plt.show()


'''
fig = plt.figure(figsize = (10, 5))
plt.bar(labels, captured_list, color ='red', width = 0.4)
plt.xlabel("Player Strategy")
plt.ylabel("Number of times pawns lost per game")
plt.title("Average number of times pawns lost per game for different playstyles")
plt.show()
#'''





