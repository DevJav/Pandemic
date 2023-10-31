class Player():
    def __init__(self, role):
        self.hand = []
        self.role = role
        self.location = "Atlanta"
        self.n_cards_per_disease = {"Blue":0, "Yellow":0, "Black":0, "Red":0}

    def get_hand(self):
        return self.hand
    
    def get_hand_names(self):
        return [card.get_name() for card in self.hand]
    
    def add_card(self, card):
        self.hand.append(card)
        self.n_cards_per_disease[card.get_disease()] += 1
        return self.hand
    
    def remove_card(self, card_name):
        for i, c in enumerate(self.hand):
            if c.get_name() == card_name:
                self.n_cards_per_disease[c.get_disease()] -= 1
                return self.hand.pop(i)
        return self.hand
    
    def get_n_cards_per_disease(self):
        return self.n_cards_per_disease

    def get_role(self):
        return self.role
    
    def set_role(self, role):
        self.role = role
        return self.role
    
    def get_location(self):
        return self.location
    
    def set_location(self, location):
        self.location = location
        return self.location