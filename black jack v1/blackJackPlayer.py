import socket
import threading
import singlePlayer


class player:
    def __init__(self, ip: str, funds: int, hand: list, total: int, playing: bool, in_for: int, ace_high:bool):
        self.funds = funds
        self.ip = ip
        self.hand = hand
        self.total = total
        self.playing = playing
        self.in_for = in_for

    def give_player_hand(self):
        singlePlayer.give_card(self.hand, self.total)
        singlePlayer.give_card(self.hand, self.total)
