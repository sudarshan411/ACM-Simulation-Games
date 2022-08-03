import pygame as pg
import random
import math
from pygame import mixer
import random
import time

fps = 60
playerid = 0
min_bid = 100
initial_money = 1000
tax_rate = 0.05
width = 900
height = 600
effect_multiplier = 1
stock_names = ["Cap", "Spaceship", "Train","Fan","Cycle","Car","Bike","Jet",
               "Headphones","Laptop","Clothes","Sofa","T.V","Bed","Teddy Bear"]
stock_image_dict = {"Cap":"cap.png", "Spaceship":"spaceship.png", "Train":"train.png",
                    "Fan":"fan.png","Cycle":"cycle.png","Car":"car.png",
                    "Bike":"bike.png","Jet":"jet.png","Headphones":"headphones.png",
                    "Laptop":"laptop.png","Clothes":"clothes.png","Sofa":"sofa.png",
                    "T.V":"TV.png","Bed":"bed.png","Teddy Bear":"teddy bear.png"}
buffs = [[2,"tax"], [3,"earning"], [3,"stock value"]]
debuffs = [[2,"tax"], [3,"earning"], [3,"stock value"]]
colors = ["red","green","blue","yellow","purple","brown"]
roll_effect_dict = {0:""}

class game_master:
    """Controls all the data of the game"""
    def __init__(self):
        self.players = []
        self.stock_names = stock_names
        self.buffs = buffs
        self.debuffs = debuffs
        self.stock = []
        self.state = "bidding"
        self.rounds = 1
        self.round_winners = []
        
    def create_stock(self):
        x = random.randint(0, len(self.stock_names) - 1)
        name = self.stock_names[x]
        x = random.randint(0, len(self.buffs) - 1)
        buff = self.buffs[x]
        y = random.randint(0, len(self.debuffs) - 1)
        while(y==x):
            y = random.randint(0, len(self.debuffs) - 1)
        debuff = self.debuffs[y]
        cost = min_bid*((100 + random.randint(-20, 20))/100)
        stock(name, buff, debuff, cost, self)
        return 1
    
    def increment_round(self):
            self.rounds = self.rounds + 1
            if (self.rounds % 3)==0:
                self.state = "announce"
            else:
                self.state = "announce"
            for pl in self.players:
                pl.money = int(pl.money*(1 - pl.tax_rate))
            return 1
    
    def distribute_stock(self):
        maximum = -1
        i = 0
        for pl in self.players:
            if pl.bid>maximum:
                maximum = pl.bid
                x = i
            i = i + 1
        count = 0
        for pl in self.players:
            if(pl.bid == maximum):
                count = count + 1
        if(maximum<self.stock[-1].cost):
            self.increment_round()
            return 1
        if(count>2):
            self.increment_round()
            """Here, i considered rounds increment even if allotment of stock fails"""
            return -1
        elif count == 2:
            for pl in self.players:
                if pl.bid == maximum:
                    pl.get_stock(maximum,maximum)
                    self.round_winners.append(pl)
            self.increment_round()
            return 1
        else:
            maximum2 = -1
            i = 0
            y = -1
            for pl in self.players:
                if(pl.bid>maximum2) and (i!=x):
                    y = i
                    maximum2 = pl.bid
            if (maximum2 != -1) and (maximum2>self.stock[-1].cost):
                maximum = maximum2
            self.players[x].get_stock(maximum,self.players[x].bid)
            self.round_winners.append(self.players[x])
            if (len(self.players)>=2) and (maximum2>self.stock[-1].cost):
                self.players[y].get_stock(maximum,self.players[y].bid)
                self.round_winners.append(self.players[y])
            self.increment_round()
            return 1
    def dice_roll_player_decide(self):
        minimum = initial_money*10
        x = -1
        i = 0
        for pl in self.players:
            net_worth = 0
            net_worth += pl.money
            for st in pl.stock:
                net_worth += st.cost
            if net_worth < minimum:
                minimum = net_worth
                x = i
            i += 1
        self.players[x].dice = 1
        return 1
    
    def dice_effect(self,pl,number,multiplier):
        #number = 5
        if number == 0:
            minimum = initial_money*10
            x = -1
            i = 0
            for st in pl.stock:
                if(st.cost<minimum):
                    minimum = st.cost
                    x = i
                i = i + 1
            if(x!=-1):
                pl.stock[x].update_price(pl.stock[x].cost * (1 + (0.25 * multiplier)))
            return ("Stimulating!!")
        elif number == 1:
            earn = 0
            for st in pl.stock:
                earn += st.cost * 0.1*multiplier
            pl.money = pl.money + earn
            return ("Oops! Capital Gains")
        elif number == 2:
            pl.tax_rate = pl.tax_rate * (0.5/multiplier)
            return ("Chicago Boys in da house")
        elif number == 3:
            return ("The Not So Great Depression")
        elif number == 4:
            maximum = -1
            x = -1
            i = 0
            for st in pl.stock:
                if(st.cost>maximum):
                    maximum = st.cost
                    x = i
                i = i + 1
            if(x!=-1):
                pl.stock[x].update_price(pl.stock[x].cost * (1 - (0.25 * multiplier)))
            return ("Trouble in paradise")
        elif number == 5:
            for st in pl.stock:
                st.update_price(st.cost * (1 - (0.1 * multiplier)))
            return ("Stock Market Crash")
        else:
            return ("Something went wrong with the dice roll")
    
    def get_winner(self):
        maximum = -1
        x = -1
        i = 0
        for pl in self.players:
            net_worth = 0
            net_worth += pl.money
            for st in pl.stock:
                net_worth += st.cost
            pl.net_worth = net_worth
            if net_worth > maximum:
                maximum = net_worth
                x = i
            i += 1
        winner = self.players[x].name
        i = 0
        for pl in self.players:
            if(pl.net_worth==maximum) and (i!=x):
                winner = winner + ', ' + pl.name 
            i = i+1
        return winner


class player:
    """The player object defines each player and their abilities"""
    def __init__(self, name, color, money, game_master):
        self.name = name
        self.color = color
        self.master = game_master
        self.money = money
        self.bid = -1
        self.stock = []
        self.master.players.append(self)
        self.tax_rate = tax_rate
        self.dice = 0
        self.net_worth = 0
        
    def get_stock(self,value,cost):
        self.stock.append(self.master.stock[-1])
        self.stock[-1].cost = value
        self.money = self.money - cost
        cost_text = self.stock[-1].detail_font.render(f"Value: {value}",True,(25,25,25))
        self.stock[-1].image.blit(cost_text,(self.stock[-1].rect_pos[0]+2,self.stock[-1].rect_pos[1]+33))
    
    def display_cards(self,screen):
        n = len(self.stock)
        if(n==0):
            return 1
        spacing = 10
        start = width/2
        sx, sy = self.stock[0].image.get_size()
        start = start - (sx/2)
        if(n>6):
            spacing = ((5*spacing) - ((n - 6)*sx))/(n - 1)
        
        
        increment = - ((spacing/2) + (sx/2))
        for st in self.stock:
            start = start + increment
        start = start - increment
        increment = (-2) * increment
        for st in self.stock:
            screen.blit(st.image,(start,height - sy - 5))
            start = start + increment
        
class stock:
    """defines everything about a stock"""
    def __init__(self, name, buff, debuff, cost, game_master):
        self.name = name
        self.buff = buff
        self.debuff = debuff
        self.cost = cost
        self.master = game_master
        self.image = pg.image.load("card_template_update.png")
        sx, sy = self.image.get_size() 
        self.image = pg.transform.scale(self.image, (int(sx*0.5),int(sy*0.5)))
        self.sx, self.sy = self.image.get_size()
        temp = pg.image.load(stock_image_dict[self.name])
        sx,sy = temp.get_size()
        self.image.blit(temp,((self.sx/2)-(sx/2),(self.sy/2)-(sy/2)-25))
        title_font = pg.font.Font('freesansbold.ttf',18)
        title = title_font.render(self.name,True,(50,209,206))
        sx,sy = title.get_size()
        self.image.blit(title,((self.sx/2)-(sx/2),20))
        self.master.stock.append(self)
        pg.draw.rect(self.image,(8, 200, 200),(self.sx*0.125,self.sy*0.75-15,self.sx*0.75,self.sy*0.25),0,8)
        rect_pos = (self.sx*0.125,self.sy*0.75-15)
        self.rect_pos = rect_pos
        detail_font = pg.font.Font('freesansbold.ttf',12)
        self.detail_font = detail_font
        if self.buff[1] == "tax":
            sign = "-"
        else:
            sign = "+"
        buff_text = detail_font.render(f"{sign}{self.buff[0]}% {self.buff[1]}",True,(38, 87, 26))
        if sign =="-":
            sign = "+"
        else:
            sign = "-"
        debuff_text = detail_font.render(f"{sign}{self.debuff[0]}% {self.debuff[1]}",True,(217, 32, 8))
        self.image.blit(buff_text, (rect_pos[0]+2,rect_pos[1]+3))
        self.image.blit(debuff_text, (rect_pos[0]+2,rect_pos[1]+18))
        
    def update_price(self,value):
        value = int(value)
        self.cost = value
        cost_text = self.detail_font.render(f"Value: {value}",True,(25,25,25))
        self.image.blit(cost_text,(self.rect_pos[0]+2,self.rect_pos[1]+33))
        pg.draw.rect(self.image,(8, 200, 200),(self.sx*0.125,self.sy*0.75-15,self.sx*0.75,self.sy*0.25),0,8)
        rect_pos = (self.sx*0.125,self.sy*0.75-15)
        self.rect_pos = rect_pos
        detail_font = pg.font.Font('freesansbold.ttf',12)
        self.detail_font = detail_font
        if self.buff[1] == "tax":
            sign = "-"
        else:
            sign = "+"
        buff_text = detail_font.render(f"{sign}{self.buff[0]}% {self.buff[1]}",True,(38, 87, 26))
        if sign =="-":
            sign = "+"
        else:
            sign = "-"
        debuff_text = detail_font.render(f"{sign}{self.debuff[0]}% {self.debuff[1]}",True,(217, 32, 8))
        self.image.blit(buff_text, (rect_pos[0]+2,rect_pos[1]+3))
        self.image.blit(debuff_text, (rect_pos[0]+2,rect_pos[1]+18))
        self.image.blit(cost_text,(self.rect_pos[0]+2,self.rect_pos[1]+33))
    
    

"""Deciding player names. Should change this to take only one name and
store player details on server i think"""
master = game_master()
#number_of_players = int(input("Enter the number of players: "))
#for i in range(0,number_of_players):
#    name = input(f"Enter the name of player{i}: ")
#    p = player(name, colors[i], initial_money, master)


#Initialize pygame first always to be able to use the stuff
pg.init()

#create the game screen
screen = pg.display.set_mode((width, height))
bg_image = pg.image.load("bg.jpg")
#Set the Game's Name
pg.display.set_caption("Bull Run")
#Set the game window icon
icon = pg.image.load("Bull Run.jpg")
pg.display.set_icon(icon)

#master.create_stock()#Turn this on to test the stock image thing




animating = 0
created = 0
created2 = 0
taking_input = 1
endgame = 0
p = player("Hari", colors[playerid], initial_money, master)

#Text Box stuff
input_box = pg.Rect(560, 180, 140, 32)
color_inactive = (63, 8, 105)
color_active = (129, 13, 217)
rect_color = color_inactive
color = (229, 63, 113)
active = False
text = ''
bid_message = ''
input_box_exists = 0
bid_font = pg.font.Font('freesansbold.ttf',25)

#Dice roll button stuff
dice_roll_box = pg.Rect(375,185,155,105)
dice_roll_color = (63, 8, 105)
dice_font = pg.font.Font('freesansbold.ttf',36)
dice_active = False
dice_box_exists = False


#Main game loop that determines what happens in the game
clock = pg.time.Clock()
running = True
while running:
    #BG color set
    screen.fill((77, 0, 153))
    screen.blit(bg_image,(0,0))
    '''
    sx = master.stock[-1].sx
    sy = master.stock[-1].sy
    screen.blit(master.stock[-1].image, (int((width/2)-(sx/2)),int((height/2)-(sy/2)+200)))
    #'''
    
    
    
    if master.state == "bidding":
        p.bid = -1
        if(created == 0):
            master.create_stock()
            created = 1
        sx = master.stock[-1].sx
        sy = master.stock[-1].sy
        stock_location = (int((width/2)-(sx/2)),int((height/2)-(sy/2)-125))
        screen.blit(master.stock[-1].image, stock_location)
        if p.money < master.stock[-1].cost:
            if(created2==0):
                not_enough_end_time = time.time() + 3
                created2 = 1
            if(time.time()<not_enough_end_time):
                not_enough_text = bid_font.render("Not enough money, skipping turn...",True, color)
                sx,sy = not_enough_text.get_size()
                screen.blit(not_enough_text,(450-(sx/2), 280))
            else:
                p.bid = 0
                created = 0
                created2 = 0
                bid_message = ""
                taking_input = 0
                input_box_exists = 0
                text = ''
                master.state = "wait"
        if taking_input==1:
            input_box_exists = 1
            # Render the current text.
            txt_surface = bid_font.render(text, True, color)
            bid_text = bid_font.render("Enter your bid: ",True, color)
            bid_message_render = bid_font.render(bid_message,True,color)
            minimum_bid1 = bid_font.render("Minimum bid amount:",True,color)
            minimum_bid2 = bid_font.render(f"{int(master.stock[-1].cost)}",True,color)
            # Resize the box if the text is too long.
            input_width = max(200, txt_surface.get_width()+10)
            input_box.w = input_width
            # Blit the input_box rect.
            pg.draw.rect(screen, rect_color, input_box, 0,8)
            # Blit the text.
            screen.blit(bid_text,(input_box.x+5, input_box.y-36))
            screen.blit(bid_message_render,(input_box.x+5, input_box.y+49))
            screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
            screen.blit(minimum_bid1, (input_box.x-500, input_box.y-36))
            screen.blit(minimum_bid2, (input_box.x-360, input_box.y))
    
    if master.state == "wait":
        created = 0
        taking_input = 1
        b = 1
        for pl in master.players:
            if(pl.bid==-1):
                b = 0
        if(b==0):
            waiting_text = bid_font.render("Waiting for other players to bid...",True, color)
            screen.blit(waiting_text,(225,250))
        else:
            master.distribute_stock()
            for pl in master.players:
                pl.bid = -1
        
    if master.state == "announce":
        if created==0:
            announcement_end_time = time.time() + 3
            created  = 1
        if(time.time()<announcement_end_time):
            start_announce_text_y = 225
            for pl in master.round_winners:
                got_stock_text = bid_font.render(f"{pl.name} got the stock at a value of {pl.stock[-1].cost}!!",True, color)
                screen.blit(got_stock_text,(225, start_announce_text_y))
                start_announce_text_y += 45
            if(len(master.round_winners)==0):
                got_stock_text = bid_font.render("No player could afford the stock!!",True, color)
                sx,sy = got_stock_text.get_size()
                screen.blit(got_stock_text,(450 - (sx/2), start_announce_text_y))
        else:
            created = 0
            master.round_winners = []
            if ((master.rounds % 3)==0):
                master.dice_roll_player_decide()
                master.state = "dice roll"
            else:
                master.state = "bidding"
    
    if master.state == "dice roll":
        if p.dice==0:
            waiting_text = bid_font.render("Waiting for other player to finish rolling the dice...",True, color)
            sx, sy = waiting_text.get_size()
            screen.blit(waiting_text,(450 - (sx/2),250))
        elif p.dice==1:
            end_dice_roll = 0
            dice_box_exists = True
            if not dice_active:
                # Blit the dice rol box rect.
                pg.draw.rect(screen, dice_roll_color, dice_roll_box, 0,8)
                roll_it_text = dice_font.render("Roll Dice",True,color)
                screen.blit(roll_it_text,(374,210))
            if dice_active:
                dice_box_exists = False
                if created == 0:
                    dice_roll_end_time = time.time() + 3
                    created = 1
                if(time.time() < dice_roll_end_time):
                    dice1 = random.randint(1,6)
                    dice2 = random.randint(1,6)
                    dice_text = dice_font.render(f"{dice1}  {dice2}",True,color)
                    screen.blit(dice_text,(415, 225))
                    created2 = 0
                else:
                    if(created2 == 0 ):
                        dice_display_end_time = time.time() + 4
                        created2 = 1
                        effect = master.dice_effect(p,abs(dice1 - dice2), effect_multiplier)
                        #effect = "Noice"
                    if(time.time()<dice_display_end_time):
                        dice_text = dice_font.render(f"{dice1}  {dice2}",True,color)
                        screen.blit(dice_text,(415, 200))
                        dice_text = dice_font.render(effect,True,color)
                        sx, sy = dice_text.get_size()
                        screen.blit(dice_text,(450 - (sx/2), 275))
                    else:
                        end_dice_roll = 1
            if(end_dice_roll == 1):
                created = 0
                created2 = 0
                dice_active = False
                dice_box_exists = False
                if(abs(dice1 - dice2)==3):
                    master.state = "dice roll"
                    effect_multiplier = effect_multiplier*1.5
                else:
                    p.dice = 0
                    effect_multiplier = 1
                    master.state = "bidding"

    if master.rounds==11:
        master.state = "endgame"
        
    if master.state=="endgame":
        endgame = 1
        winners_names = master.get_winner()
        winner_text = dice_font.render(f"{winners_names} Won the game!!!",True,color)
        sx,sy = winner_text.get_size()
        screen.blit(winner_text, (width/2 - sx/2, height/2 - 100))
        
    if endgame==0:
        p.display_cards(screen)
        money_render = bid_font.render(f"Money: {p.money}",True,color)
        screen.blit(money_render,(25,25))
        rounds_render = bid_font.render(f"Round {master.rounds}",True,color)
        screen.blit(rounds_render,(750,25))

    for event in pg.event.get():
        if event.type == pg.QUIT :
            running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            if(master.state=="bidding"):
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos) and (input_box_exists):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                # Change the current color of the input box.
                rect_color = color_active if active else color_inactive
            if(master.state=="dice roll"):
                if dice_roll_box.collidepoint(event.pos) and (dice_box_exists):
                    dice_active = True
                    dice_box_exists = False
        if event.type == pg.KEYDOWN:
            if active:
                if (event.key == pg.K_RETURN) or (event.key == pg.K_KP_ENTER):
                    try:
                        bid_amount = int(text)
                        if(bid_amount<master.stock[-1].cost):
                            bid_message = "Bid too low"
                        elif(bid_amount>p.money):
                            bid_message = "Not enough money"
                        else:
                            bid_message = ""
                            p.bid = bid_amount
                            taking_input = 0
                            input_box_exists = 0
                            text = ''
                            master.state = "wait"
                            
                    except:
                        bid_message = "Invalid input"
                    
                elif event.key == pg.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
    
    
    
    #just updates the display
    pg.display.update()
    #this sets the while loop rate to 60 fps
    clock.tick(fps)

'''
#Testing the functioning of the main attributes and their interlinking 
for i in range(0,number_of_players):
    master.create_stock()
    print(master.stock[-1].name)
    print(master.stock[-1].buff)
    print(master.stock[-1].debuff)
    print(master.stock[-1].cost)
    
    master.players[i].get_stock()
    print(master.players[i].name)
    print(master.players[i].color)
    print(master.players[i].money)
    print(master.players[i].stock[-1].name)
    print(master.players[i].stock[-1].buff)
    print(master.players[i].stock[-1].debuff)
    print(master.players[i].stock[-1].cost)
    print("\n\n\n")
'''

pg.quit()