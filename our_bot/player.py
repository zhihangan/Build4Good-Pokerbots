from skeleton.actions import FoldAction, CallAction, CheckAction, RaiseAction
from skeleton.states import GameState, TerminalState, RoundState
from skeleton.states import NUM_ROUNDS, STARTING_STACK, BIG_BLIND, SMALL_BLIND
from skeleton.bot import Bot
from skeleton.runner import parse_args, run_bot
from skeleton.equity import simulate_equity
import random


class Player(Bot):
    def __init__(self):
        # Initialize persistent variables here
        self.total_bankroll = 0
        self.round_num = 0

    def handle_new_round(self, game_state, round_state, active):
        self.round_num = game_state.round_num
        self.my_bankroll = game_state.bankroll
        self.my_cards = round_state.hands[active]
        self.is_big_blind = bool(active)

    def handle_round_over(self, game_state, terminal_state, active):
        self.total_bankroll += terminal_state.deltas[active]

    def get_action(self, game_state, round_state, active):
        legal_actions = round_state.legal_actions()
        street = round_state.street
        my_cards = round_state.hands[active]
        board_cards = round_state.deck[:street]
        my_pip = round_state.pips[active]
        opp_pip = round_state.pips[1 - active]
        my_stack = round_state.stacks[active]
        opp_stack = round_state.stacks[1 - active]
        continue_cost = opp_pip - my_pip
        my_contribution = STARTING_STACK - my_stack
        opp_contribution = STARTING_STACK - opp_stack

        hand_equity = simulate_equity(my_cards, board_cards)

        if RaiseAction in legal_actions:
            min_raise, max_raise = round_state.raise_bounds()
            min_cost = min_raise - my_pip
            max_cost = max_raise - my_pip

            if street == 0:  # Pre-flop
                if my_contribution == SMALL_BLIND:
                    if hand_equity < 0.6:
                        return CallAction()
                    elif hand_equity < 0.8:
                        return RaiseAction(int(min_raise * 1.5))
                    else:
                        return RaiseAction(max_raise)
                elif my_contribution == BIG_BLIND:
                    if opp_contribution == 10:
                        if hand_equity > 0.6:
                            return RaiseAction(max_raise)
                        else:
                            return CheckAction()
                    else:
                        if hand_equity > 0.63:
                            return RaiseAction(max_raise)
                        else:
                            return FoldAction()
                else:
                    if hand_equity > 0.63:
                        return RaiseAction(max_raise)
                    else:
                        return FoldAction()

            else:  # Post-flop
                if opp_pip == 0:
                    if hand_equity < 0.4:
                        return CheckAction()
                    elif hand_equity < 0.65:
                        return RaiseAction(int(min_raise * 1.5))
                    else:
                        return RaiseAction(int(min_raise * 2.5))
                else:
                    if hand_equity < 0.55:
                        return FoldAction()
                    elif hand_equity < 0.65 and opp_pip < my_contribution:
                        return CheckAction()
                    elif hand_equity < 0.65 and opp_pip > my_contribution:
                        return FoldAction()
                    elif hand_equity >= 0.65 and opp_pip > my_contribution:
                        return RaiseAction(max_raise)

        if CheckAction in legal_actions:
            return CheckAction()

        if hand_equity < 0.6:
            return FoldAction()
        else:
            return CallAction()


if __name__ == '__main__':
    run_bot(Player(), parse_args())
