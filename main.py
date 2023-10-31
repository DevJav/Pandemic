import itertools
import random
import pandas as pd
from matplotlib import pyplot as plt

from city import City
from player import Player

class Card():
    def __init__(self, name, disease):
        self.__name = name
        self.__disease = disease

    def get_name(self):
        return self.__name

    def get_disease(self):
        return self.__disease
    
    def __str__(self):
        return self.__name + " (" + self.__disease + ")"
    
    def __repr__(self):
        return self.__name + " (" + self.__disease + ")"
        
class Pandemic():
    def __init__(self, n_players):
        prov_roles = ["Medic", "Analist", "Scientist", "Quarantine Specialist", "Researcher", "Dispatcher", "Operations Expert", "Contingency Planner"]
        self.players = [Player(prov_roles[i]) for i in range(n_players)]

        df = pd.read_csv('map.csv', sep=',', header=0)
        # df = pd.read_csv('test_map.csv', sep=',', header=0)

        cities = df['City'].tolist()
        diseases = df['Disease'].tolist()
        connections = df['Connections'].tolist()
        connections = [connection.split(',') for connection in connections]
        connections = [[city.strip() for city in connection] for connection in connections]

        self.cities = []
        self.cities.extend(City(cities[i], diseases[i], connections[i]) for i in range(len(cities)))

        self.cards_deck = []
        self.cards_deck.extend(Card(cities[i], diseases[i]) for i in range(len(cities)))
        random.shuffle(self.cards_deck)

        self.infection_deck = []
        self.infection_deck.extend(Card(cities[i], diseases[i]) for i in range(len(cities)))
        random.shuffle(self.infection_deck)

        self.cards_discard = []
        self.infection_discard = []

        self.outbreaks = 0
        self.infection_rate = 2
        self.infection_rate_track = [2,2,2,3,3,4,4]
        self.infection_rate_index = 0

        self.cubes = {"Blue":24, "Yellow":24, "Black":24, "Red":24}

        self.cure_status = {"Blue":False, "Yellow":False, "Black":False, "Red":False}
        self.erradicated = {"Blue":False, "Yellow":False, "Black":False, "Red":False}

        self.turn = 0
        self.actions = 4
        self.hand_limit = 7

        self.game_over = False
        self.game_won = False

        self.initial_infection()
        self.initial_cards()

        self.difficulty = 2
        self.difficulty_track = [4,5,6]
        self.n_epidemic_cards = self.difficulty_track[self.difficulty]

        self.divided_deck = [self.cards_deck[i::self.n_epidemic_cards] for i in range(self.n_epidemic_cards)]
        for i in range(self.n_epidemic_cards):
            self.divided_deck[i].append(Card("Epidemic", "Epidemic"))
            random.shuffle(self.divided_deck[i])

        self.cards_deck = []
        for i in range(self.n_epidemic_cards):
            self.cards_deck.extend(self.divided_deck[i])
        
        self.game_over = False
        self.game_won = False

        self.main_loop()

    def main_loop(self):
        while not self.game_over:
            self.turn += 1
            print("Turn", self.turn)
            self.turn_loop()
            # self.check_game_over()
            # self.check_game_won()
        print("Game over!")

    def turn_loop(self):
        for player in self.players:
            print("Player", self.players.index(player))
            self.actions = 4
            self.turn_player(player)
            # self.check_game_over()
            # self.check_game_won()
            if self.game_over or self.game_won:
                break
        self.infect_cities()

    def turn_player(self, player):
        print(f"Turn of {player.get_role()}. Location: {player.get_location()}")
        print("Hand:", player.get_hand())

        for _ in range(self.actions):
            print("1. Move")
            if self.check_build_research_station_available(player):
                print("2. Build research station")
            if self.check_treat_disease_available(player):
                print("3. Treat disease")
            if self.check_share_knowledge_available(player):
                print("4. Share knowledge")
            if self.check_discover_cure_available(player):
                print("5. Discover cure")
            print("6. Pass")
            action = int(input("Choose an action: "))
            if action == 1:
                self.move(player)
            elif action == 2:
                self.build_research_station(player)
            elif action == 3:
                self.treat_disease(player)
            elif action == 4:
                self.share_knowledge(player)
            elif action == 5:
                self.discover_cure(player)
            elif action == 6:
                break
            else:
                print("Invalid action")
        
        for _ in range(2):
            drawn_card = self.cards_deck.pop(0)
            self.cards_discard.append(drawn_card)
            player.add_card(drawn_card)
            print("Card drawn:", drawn_card)


    def move(self, player):
        available_moves = self.get_city(player.get_location()).get_connections()
        print("Available moves:")
        for idx, location in enumerate(available_moves):
            print(f"{idx}. {location}")
        selection = int(input("Choose an option: "))
        player.set_location(available_moves[selection])
        print(f"Moved to {player.get_location()}")

    def check_build_research_station_available(self, player):

        return (
            not self.get_city(player.get_location()).get_research_station()
            and player.get_location() in player.get_hand_names()
        )
        
    def build_research_station(self, player):
        if self.get_city(player.get_location()).get_research_station():
            print(f"There is already a research station in {player.get_location()}")
        elif player.get_location() not in player.get_hand():
            print(f"You don't have the card of {player.get_location()}")
        else:
            self.get_city(player.get_location()).set_research_station(True)
            player.get_hand().remove(player.get_location())
            print(f"Research station built in {player.get_location()}")

    def check_treat_disease_available(self, player):
        city = self.get_city(player.get_location())
        return (
            city.get_disease_cubes()[city.get_main_disease()] > 0
        )

    def treat_disease(self, player):
        city = self.get_city(player.get_location())
        if city.get_disease_cubes()[city.get_main_disease()] == 0:
            print(f"There are no disease cubes in {player.get_location()}")
        elif (player.get_role() == "Medic") or (self.cure_status[city.get_main_disease()]):
            city.set_disease_cubes(city.get_main_disease(), 0)
            print(f"All disease cubes removed from {player.get_location()}")
        else:
            city.set_disease_cubes(city.get_main_disease(), city.get_disease_cubes()[city.get_main_disease()] - 1)
            print(f"One disease cube removed from {player.get_location()}")

    def check_share_knowledge_available(self, player):
        available_players = [other_player for other_player in self.players 
                            if ((other_player.get_location() == player.get_location() and other_player != player))]
        player_hand = player.get_hand()
        cities_in_hand = [card.get_name() for card in player_hand]
        able_to_give = player.get_location() in cities_in_hand
        able_to_take = False
        if available_players:
            for other_player in available_players:
                cities_in_hand = other_player.get_hand_names()
                able_to_take = other_player.get_location() in cities_in_hand
                if able_to_take:
                    break

        return able_to_give or able_to_take

    def share_knowledge(self, player):
        available_players = [other_player for other_player in self.players 
                            if ((other_player.get_location() == player.get_location() and other_player != player))]
        player_hand = player.get_hand()
        cities_in_hand = [card.get_name() for card in player_hand]
        able_to_give = player.get_location() in cities_in_hand

        if able_to_give:
            print("You can give the card of your location to:")
            for idx, other_player in enumerate(available_players):
                print(f"{idx}. {other_player.get_role()}")
            selection = int(input("Choose an option: "))
            removed_card = player.remove_card(player.get_location())
            available_players[selection].add_card(removed_card)
            print(f"{player.get_location()} given to {available_players[selection].get_role()}")
        else:
            able_to_take = False
            if not available_players:
                print("There is no one else in your location")
            else:
                for other_player in available_players:
                    other_player_hand = other_player.get_hand()
                    cities_in_hand = [card.get_name() for card in other_player_hand]
                    able_to_take = other_player.get_location() in cities_in_hand
                    if able_to_take:
                        able_to_give_player = other_player
                        break

            if not able_to_take:
                print("You can't share knowledge with anyone")
            else:
                print(f"You received {able_to_give_player.get_location()} from {able_to_give_player.get_role()}")
                removed_card = able_to_give_player.remove_card(able_to_give_player.get_location())
                player.add_card(removed_card)

    def check_discover_cure_available(self, player):
        city = self.get_city(player.get_location())
        if not city.get_research_station():
            return False
        n_cards_per_disease = player.get_n_cards_per_disease()
        for disease in n_cards_per_disease:
            # this could be done better
            if n_cards_per_disease[disease] >= 5:
                return True
        return False

    def discover_cure(self, player):
        city = self.get_city(player.get_location())
        if city.get_research_station():
            n_cards_per_disease = player.get_n_cards_per_disease()
            for disease in n_cards_per_disease:
                # this could be done better
                if n_cards_per_disease[disease] >= 5:
                    print(f"You discovered a cure for {disease}")
                    self.cure_status[disease] = True
                    break
            else:
                print("You don't have enough cards of the same disease")
        else:
            print(f"There is no research station in {player.get_location()}")

    def initial_infection(self):
        for i, _ in itertools.product(range(3), range(3)):
            drawn_card = self.infection_deck.pop(0)
            self.infection_discard.append(drawn_card)
            self.infect(drawn_card.get_name(), drawn_card.get_disease(), 3-i)
        # self.print_cities_status()

    def initial_cards(self):
        for player in self.players:
            for _ in range(6 - len(self.players)):
                drawn_card = self.cards_deck.pop(0)
                self.cards_discard.append(drawn_card)
                player.add_card(drawn_card)
        print("Initial cards:")
        for player in self.players:
            print(player.get_hand())

    def infect(self, city_name, disease, n):
        city = self.get_city(city_name)
        if self.erradicated[disease]:
            print("Disease", disease, "is erradicated")
        elif city.get_disease_cubes()[disease] + n > 3:
            print("Outbreak in", city_name)
            # self.outbreak(city_name, disease)
        else:
            print("Infecting", city_name, "with", n, "cubes of", disease)
            city.set_disease_cubes(disease, n)
            self.cubes[disease] -= n

    def infect_cities(self):
        for _ in range(self.infection_rate):
            drawn_card = self.infection_deck.pop(0)
            self.infection_discard.append(drawn_card)
            self.infect(drawn_card.get_name(), drawn_card.get_disease(), 1)

    def get_city(self, city_name):
        for city in self.cities:
            if city.get_name() == city_name:
                return city
            
if __name__ == '__main__':
    game = Pandemic(4)