import random
from time import sleep

spade = '\u2660'
heart = '\u2665'
diamond = '\u2666'
club = '\u2663'

class Deck():
    def __init__(self):
        suits = [spade, heart, diamond, club]
        self.deck = []
        for suit in range(4):
            for number in range(1, 14):
                if number == 1:
                    self.deck.append(f'A{suits[suit]}')
                elif number == 11:
                    self.deck.append(f'J{suits[suit]}')
                elif number == 12:
                    self.deck.append(f'Q{suits[suit]}')
                elif number == 13:
                    self.deck.append(f'K{suits[suit]}')
                else:
                    self.deck.append(f'{number}{suits[suit]}')

    def shuffle(self):
        newDeck = [] 
        while len(self.deck) > 0:
            newDeck.append(self.deck.pop(random.randint(0, len(self.deck) - 1)))
        self.deck = newDeck

    def draw_card(self):
        return self.deck.pop()
    
    def return_card(self, card):
        self.deck.append(card)

    def deal_cards(self, players):
        for player in players:
            player.return_cards(self)
        self.shuffle()
        for player in players:
            player.hit(self)
            player.hit(self)

class Hand():
    def __init__(self):
        self.cards = []

    def return_cards(self, deck):
        while len(self.cards) > 0:
            deck.return_card(self.cards.pop())

    def hit(self, deck):
        self.cards.append(deck.draw_card())
        
    def count(self):
        count = 0
        aces_present = 0
        for card in self.cards:
            if card[0] == 'A':
                count += 11
                aces_present += 1
            elif card[0] == 'J' or card[0] == 'Q' or card[0] == 'K' or card[0] == '1':
                count += 10
            else:
                count += int(card[0])
        while count > 21 and aces_present > 0:
            count -= 10
            aces_present -= 1
        return count
    
    def show_hand(self):
        for card in self.cards:
            print(card)
        print('Total: ', self.count())

    def show_hand_opponent(self, name):
        print(name)
        for card in self.cards:
            if card == self.cards[0]:
                print('???')
            else:
                print(card)
        print('')
            
popular_name_list = ['Michael','Christopher','Matthew','Joshua','Jacob','Jessica','Ashley','Emily','Sarah','Samantha'] 

deck = Deck()
while True:
    print("LET'S PLAY SOME BLACKJACK!")
    name = input("Enter your name ")
    num_computer = input('How many computer players would you like to play with(1-6) ')

    # Make sure valid input
    try:
        num_computer = int(num_computer)
        if num_computer < 0 or num_computer > 6:
            num_computer = 0
            print('Please select 1 - 6 opponents')
    except:
        num_computer = 0
        print('INVALID INPUT')

    if num_computer > 0:
        # Initialize Game
        players = []
        scores = [0] * (num_computer + 1)
        for i in range(num_computer + 1):
            players.append(Hand())
        # Give players names
        player_names = [name]
        for i in range(num_computer):
            random_name = popular_name_list[random.randint(0, len(popular_name_list) - 1)]
            name_selected = False
            while not name_selected:
                if random_name not in player_names:
                    player_names.append(random_name)
                    name_selected = True
                else:
                    random_name = popular_name_list[random.randint(0, len(popular_name_list) - 1)]
        while True:
            print('')
            deck.deal_cards(players)
            for i in range(1,len(players)):
                players[i].show_hand_opponent(player_names[i])
            print(player_names[0])
            while True:
                players[0].show_hand()
                print('')
                action = input('Hit? (Y/N)')
                if action.upper() == 'Y':
                    players[0].hit(deck)
                    if players[0].count() > 21:
                        players[0].show_hand()
                        print('BUST!')
                        break
                else:
                    break
            for i in range(1,len(players)):
                while True:
                    print('')
                    print(player_names[i])
                    players[i].show_hand()
                    sleep(1)
                    hit = random.randint(10,18) > players[i].count()
                    if hit:
                        print(player_names[i], "Hits!")
                        players[i].hit(deck)
                        sleep(1)
                        if players[i].count() > 21:
                           print('')
                           print(player_names[i])
                           players[i].show_hand()
                           print(player_names[i], "Busts!") 
                           break
                    else:
                        print(player_names[i], "Stands!")
                        sleep(1)
                        break
            print('')
            print("The Winner Is...")
            sleep(2)
            # Calculate Winner
            winner = ''
            blackjack_found = False
            for player in range(len(players)):
                if players[player].count() == 21 and len(players[player].cards) == 2:
                    blackjack_found = True
                    scores[player] += 42
                    winner += player_names[player] + "! "
            if not blackjack_found:
                winning_score = 0
                for player in range(len(players)):
                    if players[player].count() <= 21 and players[player].count() > winning_score:
                        winning_score = players[player].count()
                for player in range(len(players)):
                    if players[player].count() == winning_score:
                        scores[player] += winning_score
                        winner += player_names[player] + "! "
            if winner == '':
                winner = "Everyone Busted!"  
            elif blackjack_found:
                winner += "With a BlackJack!"
            else:
                winner += f"With {winning_score} points!"
            print(winner,'\n')
            sleep(2)
            print("Scores:\n")
            for player in range(len(players)):
                print(f"{player_names[player]}: {scores[player]}")
            print('')
            sleep(2)
            if input("Continue? (Y/N)").upper() != 'Y':
                break
        print("Good Game!")
        break



            







