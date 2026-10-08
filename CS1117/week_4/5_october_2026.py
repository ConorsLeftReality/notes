## Card deck

def createDeck():
    deck = []
    
    suits = ["s","h","d","c"]
    special_cards = ["J","Q","K","A"]
    
    for suit in suits:
        for i in range (2,11):
            deck.append(f"{i}{suit}")
        for special_card in special_cards:
            deck.append(f"{special_card}{suit}")
    
    return deck

deck_of_cards = createDeck()

for card in deck_of_cards:
    if "h" in card or "d" in card:
        if "A" in card:
            print(f"\033[0;31m{card}")
        else:
            print(f"\033[0;31m{card}",end=" | ")
    else: 
        if "A" in card:
            print(f"\033[0;30m{card}")
        else:
            print(f"\033[0;30m{card}",end=" | ")
            
number_of_bags                  = int(input("Number of bags >>> "))
number_of_chips_per_bag         = int(input("Number of chips per bag >>> "))

bags_consumed = 0
for bags_consumed in range(0,number_of_bags):
    chips_consumed = 0
    for chips_consumed in range(0,number_of_chips_per_bag):
        print("Nom Nom Nom, nice chip")
        chips_consumed += 1
    print("BAG DONE")
    bags_consumed += 1