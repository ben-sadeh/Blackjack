#########################################
# Programmer: Ben Sadeh
# Date: January 19, 2022
# File Name: blackjackGame5.py
# Description: Blackjack Game
#########################################
import pygame
pygame.init()
import random

#Lists of suit names and card symbols to be used to create a deck
suitNames  =  ['club', 'diamond', 'heart', 'spade']
cardSymbol  =  ['2','3','4','5','6','7','8','9','10','A','J','Q','K']

class Card(object):
    """A standard playing card from a deck of 52 cards
    """

    def __init__(self, suit='', symbol=''):
        self.suit = suit
        self.card = symbol + " " + suit
        self.symbol = symbol
 
        if self.symbol in ['K', 'Q', 'J']: #Royals have a value of 10
            self.value = 10
        elif self.symbol == 'A': #Aces starting value is 11
            self.value = 11
        else:
            self.value = int(symbol) #Number cards have a value of their number


        # Download the front and back pictures of each card
        self.front = pygame.image.load('cardsPictures/' + self.suit.lower() + '_' + self.symbol.lower() + '.png')
        self.back = pygame.image.load('cardsPictures/back.png')
        
        self.face_up = True #Determines if card is face up or down

    def draw(self, surface, position): #Draw the card on the screen
        if self.face_up:
            surface.blit(self.front, position)
        else:
            surface.blit(self.back, position)
            
    def show(self): #Make the card face up
        self.face_up = True

    def hide(self): #Make the card face down
        self.face_up = False

#---------------------------------------#
class Player():
    def __init__(self):
        self.hand = []
        self.chips = 100 #Everyone starts with $100
        self.bet_amount = 0

    def hit(self, deck): #Hit the deck
        self.hand.append(deck.pop())

    def hand_value(self): #Determines the total value of the player's hand
        card_sum = 0
        for card in self.hand:
            card_sum += card.value
        return card_sum

    def clearHand(self): #Resets the player's hand
        self.hand = []

    def bust(self): #Determines if the player busted
        card_sum = 0
        for card in self.hand:
            card_sum += card.value
        for card in self.hand:
            if card.symbol == 'A': #Changes the ace value from 11 to 1
                card_sum -= 10
        if card_sum > 21:
            return True
        else:
            return False
        
    def blackjack(self): #Checks if the player got blackjack
        if len(self.hand)==2 and self.hand_value()==21:
            return True
        else:
            return False

#---------------------------------------#
class Dealer():
    def __init__(self):
        self.hand = []

    def shuffleDeck(self, deck): #Shuffles the deck
        random.shuffle(deck)
        return (deck)

    def printNumCards(self, deck): #Determines the length of the deck to check if a new deck needs to be generated
        return len(deck)

    def drawCard(self, deck): #Hits the deck for the dealer's hand
        self.hand.append(deck.pop())
        return deck

    def myTurn(self, deck): #Runs through the dealer's turn once the player has passed
        while self.hand_value() < 17:
            self.drawCard(deck)
            i = 0
            for card in self.hand:
                if self.bust() and card.symbol == 'A': #Checks if the ace value needs to change from 11 to 1
                    self.hand[i].value = 1
                i += 1

        if self.bust(): #Checks if the dealer busted
            return True
        else:
            return False

    def clearHand(self):
        self.hand = []

    def hand_value(self): #Determines the number value of the dealer's hand
        card_sum = 0
        for card in self.hand:
            card_sum += card.value
        return card_sum

    def bust(self): #Checks if the dealer busted
        card_sum = 0
        for card in self.hand:
            card_sum += card.value
        for card in self.hand:
            if card_sum > 21 and card == "A": #Does the ace value need to change from 11 to 1?
                card_sum -= 10
        if card_sum > 21:
            return True
        else:
            return False

#####################################################
## Classes end here
#####################################################

#Set the game screen
HEIGHT = 600
WIDTH  = 800
gameWindow=pygame.display.set_mode((WIDTH,HEIGHT))

#Download the background picture
backgroundPic=pygame.image.load("Images/blackjackTable.png")
backgroundPic=pygame.transform.scale(backgroundPic,(WIDTH,HEIGHT))
bakgroundPic=backgroundPic.convert_alpha()

#Download the intro background picture
intBackgroundPic=pygame.image.load("Images/intBlackjack.png")
intBackgroundPic=pygame.transform.scale(intBackgroundPic,(WIDTH,HEIGHT))
intBakgroundPic=backgroundPic.convert_alpha()

#Download the exit background picture
gameOverPic=pygame.image.load("Images/gameOver.png")
gameOverPic=pygame.transform.scale(gameOverPic,(400,200))
gameOverPic=gameOverPic.convert_alpha()

#Intro screen buttons
rectX, rectY, rectW, rectH = WIDTH//2-100, 460, 200, 50
rectX1, rectY1, rectW1, rectH1 = WIDTH//2-100, 520, 200, 50

#Betting button
rectX2, rectY2, rectW2, rectH2 = WIDTH//2-100, HEIGHT//2-200, 200, 50

#Game results text
resultX,resultY=0,50

#Colours
darkgreen =(   0, 128,  64)
BLACK=(0,0,0)
WHITE=(255,255,255)

#Download fonts
font = pygame.font.SysFont("Ariel Black",60)
bigFont = pygame.font.SysFont("Ariel Black",150)
smallFont = pygame.font.SysFont("Ariel Black",30)


#---------------------------------------#
#   functions                           #
#---------------------------------------#
def redrawGameWindow(): #Redraws the game screen
    #Player cards coordinates on the screen
    pCardX = 0
    pCardY = 50
    
    #Dealer cards coordinates on the screen
    dCardX = 0
    dCardY = 400
    gameWindow.blit(backgroundPic,(0,0)) #Draw the background picture
    for card in player.hand: #Draw the player's cards on the screen
        card.draw(gameWindow, (pCardX,pCardY))
        pCardX+=100
    for card in dealer.hand: #Draw the dealer's cards on the screen
        card.draw(gameWindow, (dCardX,dCardY))
        dCardX+=100
        
    #Draw the player's score on the screen
    scorePrint = font.render("You have $"+ str(player.chips)+" left",1, BLACK)
    gameWindow.blit(scorePrint,(0, 250))
    
    #Draw the word player on top of the player's hand
    playerTxt = font.render("PLAYER",1, BLACK)
    gameWindow.blit(playerTxt,(0, 0))
    
    #Draw the word dealer on top of the dealer's hand
    dealerTxt = font.render("DEALER",1, BLACK)
    gameWindow.blit(dealerTxt,(0, 350))
    pygame.display.update()

def endGameScreen():        #Draws the end game screen
    gameWindow.fill(BLACK)
    gameWindow.blit(gameOverPic,(200,200))  #Draw the game over picture
    
    #Draw the buttons on the screen
    pygame.draw.rect(gameWindow, darkgreen, (rectX, rectY, rectW, rectH), 0)
    pygame.draw.rect(gameWindow, darkgreen, (rectX1, rectY1, rectW1, rectH1), 0)
    
    #Draw the text of the buttons on the screen
    startTxt1=smallFont.render('PLAY AGAIN',1,WHITE)
    startTxt2=font.render('QUIT',1,WHITE)
    gameWindow.blit(startTxt1,(WIDTH//2-70,465))
    gameWindow.blit(startTxt2,(WIDTH//2-70,530))
    pygame.display.update()

def startGameScreen():      #Draws the start game screen
    gameWindow.blit(intBackgroundPic,(0,0)) #Draw the bckground picture
    
    #Draw the buttons on the screen
    pygame.draw.rect(gameWindow, BLACK, (rectX, rectY, rectW, rectH), 0)
    pygame.draw.rect(gameWindow, BLACK, (rectX1, rectY1, rectW1, rectH1), 0)
    
    #Draw the text of the buttons on the screen
    startTxt1=font.render('GUIDE',1,WHITE)
    startTxt2=font.render('START',1,WHITE)
    gameWindow.blit(startTxt1,(WIDTH//2-70,465))
    gameWindow.blit(startTxt2,(WIDTH//2-70,530))
    pygame.display.update()

def instructionsScreen():       #Draws the instructions screen
    gameWindow.blit(backgroundPic,(0,0)) #Draws the background picture
    #Print the intructions text on the screen
    instructionTxt=font.render('Goal of the game is to get 21 points',1,WHITE)
    instructionTxt1=font.render('Royals are 10 points',0.5,WHITE)
    instructionTxt2=font.render('Number cards are their own value',0.5, WHITE)
    instructionTxt2a=font.render('Ace is 1 or 11 points',0.5, WHITE)
    instructionTxt3=font.render('Over 21 points is a bust',0.5,WHITE)
    instructionTxt3a=font.render('Up arrow key is hit',0.5,WHITE)
    instructionTxt4=font.render('Down arrow key is pass',0.5,WHITE)
    instructionTxt5=font.render('Minimum bet is $10',0.5,WHITE)
    gameWindow.blit(instructionTxt,(20,0))
    gameWindow.blit(instructionTxt1,(20,100))
    gameWindow.blit(instructionTxt2,(20,150))
    gameWindow.blit(instructionTxt2a,(20,200))
    gameWindow.blit(instructionTxt3,(20,300))
    gameWindow.blit(instructionTxt3a,(20,400))
    gameWindow.blit(instructionTxt4,(20,450))
    gameWindow.blit(instructionTxt5,(20,550))
    pygame.display.update()

def new_deck(dealer): #Creates a new deck
    deck = []
    for suit in suitNames:
        for symbol in cardSymbol:
            card = Card(suit, symbol)
            deck.append(card)
    dealer.shuffleDeck(deck) #Shuffles the deck
    return deck

#---------------------------------------#
#   main program                        #
#---------------------------------------#

#intro screen
introScreen = True
showRules=False
while introScreen: #Start the intro screen
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN: #If the mouse is pressed
            (mouseX,mouseY) = pygame.mouse.get_pos() #Get the coordinates of the mouse
            if mouseX > rectX and mouseX < rectX+rectW and mouseY > rectY and mouseY < rectY+rectH: #If the mouse is in the "guide" button
                showRules=True
                while showRules:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN: #If the mouse is pressed on the guide screen, go back to intro screen
                            showRules = False
                    instructionsScreen()
            (mouseX,mouseY) = pygame.mouse.get_pos()
            if mouseX > rectX1 and mouseX < rectX1+rectW1 and mouseY > rectY1 and mouseY < rectY1+rectH1: #If the mouse is in the "start" button
                introScreen = False
    startGameScreen()

#Main loop
repeatGame = True
while repeatGame: #Loop to keep playing the game until player decides to end it
    in_game = True
    dealer = Dealer() #Set a new dealer
    player = Player() #Set a new player
    
    #While the player still has enough chips to play
    while in_game: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_game = False
        deck = new_deck(dealer) #Creates a new deck to use
        inPlay=True
        betScreen=True
        
        while inPlay:
            if player.chips<10: #Minimum bet is $10
                inPlay=False
                inRound=False
                in_game=False
                morePlay=False
                endGameScreenON=True
            else:
                inRound = True

            #Replays each round    
            while inRound:
                #Creates a new deck when the deck has less than 20 cards
                if len(deck) < 20: 
                    deck = new_deck(dealer)

                #Replays until a bet is placed   
                while betScreen: 
                    for event in pygame.event.get(): 
                        if event.type == pygame.MOUSEBUTTONDOWN: #If the mouse is clicked
                            (mouseX,mouseY) = pygame.mouse.get_pos()
                            yDown=0
                            #Checks if betting buttons are pressed
                            for i in range(10,60,10):
                                if player.chips>=i and mouseX > rectX2 and mouseX < rectX2+rectW2 and mouseY > rectY2+yDown and mouseY < rectY2+rectH2+yDown: #If mouse is clicked in $10 button
                                    player.bet_amount=i
                                    betScreen=False
                                    newRound=True
                                yDown+=50
                    gameWindow.blit(backgroundPic,(0,0)) #Draws background picture
                    
                    #Draws betting text instructions
                    betTxt=font.render('Place your bet',1,WHITE)
                    gameWindow.blit(betTxt,(WIDTH//2-120,50))
                    
                    #Draws betting buttons
                    bettingVariables=['bet10','bet20','bet30','bet40','bet50']
                    bettingText=["10","20","30","40","50"]
                    yDown=0
                    for i in range(5):
                        pygame.draw.rect(gameWindow, BLACK, (rectX2, rectY2+yDown, rectW2, rectH2), 0)
                        bettingVariables[i]=font.render(bettingText[i],1,WHITE)
                        gameWindow.blit(bettingVariables[i],(rectX2+80,rectY2+yDown))
                        yDown+=50
                    pygame.display.update()
                #If its a new round, reset the game screen 
                if newRound: 
                    dealer.clearHand()
                    player.clearHand()
                    dealer.drawCard(deck)
                    dealer.drawCard(deck)
                    player.hit(deck)
                    player.hit(deck)
                    dealer.hand[0].hide()
                    redrawGameWindow()
                    morePlay = True
                    newRound=False

                #Replays until there is a winner or a tie is determined    
                while morePlay:
                    
                    #If the player gets blackjack
                    if player.blackjack(): 
                        player.chips += int(1.5*player.bet_amount)
                        redrawGameWindow()
                        blkjkTxT=bigFont.render('BLACKJACK!!!',20,BLACK)
                        gameWindow.blit(blkjkTxT,(resultX,resultY))
                        pygame.display.update()
                        pygame.time.delay(2000)
                        morePlay=False
                        
                    else:
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN: #If keys are pressed
                                
                                #If player hits
                                if event.key == pygame.K_UP and not dealer.hand[0].face_up: #If up arrow key is pressed (hit) and the player has not passed their turn yet
                                    player.hit(deck)
                                    if player.bust(): #If the player busts
                                        morePlay = False
                                        player.chips -= player.bet_amount
                                        redrawGameWindow()
                                        bustedTxt=bigFont.render('YOU BUSTED!',20,BLACK)
                                        gameWindow.blit(bustedTxt,(resultX,resultY))
                                        pygame.display.update()
                                        pygame.time.delay(2000)

                                #If player passes        
                                elif event.key == pygame.K_DOWN: #If down arrow key is pressed (pass)
                                    dealer.hand[0].show()
                                    dealerBust = dealer.myTurn(deck)
                                    #If the player wins
                                    if dealerBust or player.hand_value() > dealer.hand_value(): # i.e., dealer busted
                                        player.chips += player.bet_amount
                                        redrawGameWindow()
                                        bustedTxt=bigFont.render('PLAYER WINS!',20,BLACK)
                                    #If there is a tie
                                    elif player.hand_value() == dealer.hand_value(): #Player and dealer tie
                                        bustedTxt=bigFont.render('TIE!',20,BLACK)
                                    #If dealer wins
                                    else:   
                                        player.chips -= player.bet_amount
                                        if player.chips>10:
                                            in_game=False
                                            endGameScreenON=True
                                        redrawGameWindow()
                                        bustedTxt=bigFont.render('DEALER WINS!',20,BLACK)
                                    #Print results on the screen
                                    gameWindow.blit(bustedTxt,(resultX,resultY))
                                    pygame.display.update()
                                    pygame.time.delay(2000)
                                    morePlay = False
                                    
                    redrawGameWindow() #Redraws the screen if player gets blackjack

                #Return to betting screen    
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        inRound = False
                        betScreen=True
                        
            pygame.time.delay(30)
            
    #End game screen
    while endGameScreenON:  
        endGameScreen()  #Prints the end game screen
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN: #If the mouse is pressed
                (mouseX,mouseY) = pygame.mouse.get_pos() #Get the coordinates of the mouse
                #If the mouse is in the "play again" button
                if mouseX > rectX and mouseX < rectX+rectW and mouseY > rectY and mouseY < rectY+rectH: 
                    endGameScreenON=False
                #If the mouse is in the "quit" button
                if mouseX > rectX1 and mouseX < rectX1+rectW1 and mouseY > rectY1 and mouseY < rectY1+rectH1: 
                    repeatGame=False
                    endGameScreenON=False
                    
pygame.quit()
