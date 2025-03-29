import eval7 

def simulate_equity(hole_cards, board , num_simulations=10000):
    # Convert our hole cards from string format to eval7 card objects.
    our_hand = [eval7.Card(card) for card in hole_cards]
    b = [eval7.Card(card) for card in board]
    wins, ties, losses = 0, 0, 0

    for _ in range(num_simulations):
        # Create a new deck and remove our hole cards.
        deck = eval7.Deck()
        for card in our_hand:
            deck.cards.remove(card)

        for card in b:
            deck.cards.remove(card)

        deck.shuffle()

        # Deal opponent's three cards.
        opp_hand = deck.deal(3)
        
        
        # print(opp_hand)
        
        
        # Deal 2 board cards.
        test_board = deck.deal(4-len(board))
        # print(board)
        
        
        # Evaluate the strength of both hands.
        our_score = eval7.evaluate(our_hand + b + test_board)
        opp_score = eval7.evaluate(opp_hand + b + test_board)

        if our_score > opp_score:
            wins += 1
        elif our_score == opp_score:
            ties += 1
        else:
            losses += 1

    # Calculate equity: wins + half the ties divided by total simulations.
    equity = (wins + ties / 2) / num_simulations
    return equity
