import random

class Game:
    def __init__(self):
        self.players = ['Player 1', 'Player 2']
        self.scores = [0, 0]  
        self.round_winner = None
        self.current_player = 0
        self.boxes = {player: [] for player in self.players}
        self.hammers = {player: False for player in self.players}  # Track  Hammer
        self.hammer_used = {player: False for player in self.players}  # hammer used

    def setup_boxes(self):
        for player in self.players:
            self.boxes[player] = [0, 0, 1, 1, 0]  
            random.shuffle(self.boxes[player])  

    def reveal_box(self, player, box_index):
        if self.boxes[player][box_index] == -1:
            print(f'{player} tried to open box {box_index + 1}: This box has been destroyed!')
            return False
        elif self.boxes[player][box_index] == 1:
            print(f'{player} opened box {box_index + 1}: Received a coin!')
            return True
        else:
            print(f'{player} opened box {box_index + 1}: The box is empty.')
            return False

    def use_hammer(self, player):
        if self.hammer_used[player]:
            print(f"{player}, you have already used your Hammer this round.")
            return False
        
        print(f"{player}, you have a Hammer!")
        action = input('Do you want to use the Hammer? (y/n): ')
        if action.lower() == 'y':
            target_player = 1 - self.current_player
            box_index = int(input(f'Choose a box to destroy (1-5) from {self.players[target_player]}: ')) - 1
            self.boxes[self.players[target_player]][box_index] = -1  # box destroyed
            print(f'Box {box_index + 1} of {self.players[target_player]} has been destroyed!')
            self.hammer_used[player] = True  
            return True
        return False

    def get_valid_box_index(self):
        while True:
            action = input('Choose a box (1-5): ')
            if action.isdigit() and 1 <= int(action) <= 5:
                return int(action) - 1
            else:
                print("Invalid input. Please enter a number between 1 and 5.")

    def play_round(self):
        self.setup_boxes()
        gold_count = [0, 0]

        while max(gold_count) < 2:
            print(f"\nIt's {self.players[self.current_player]}'s turn.")
            if self.hammers[self.players[self.current_player]] and not self.hammer_used[self.players[self.current_player]]:
                self.use_hammer(self.players[self.current_player])

            box_index = self.get_valid_box_index()

            if self.reveal_box(self.players[self.current_player], box_index):
                gold_count[self.current_player] += 1

            if gold_count[self.current_player] >= 2:
                print(f'{self.players[self.current_player]} wins this round!')
                self.scores[self.current_player] += 1
                self.round_winner = self.players[self.current_player]
                break

            self.current_player = 1 - self.current_player  

        return gold_count

    def next_round(self):
        if self.round_winner:
            self.hammers[self.round_winner] = True
            self.hammer_used = {player: False for player in self.players}
            loser = self.players[1 - self.current_player]
            print(f'{loser} starts the next round.')
            self.current_player = 1 - self.current_player
            self.round_winner = None

    def check_winner(self):
        for i, score in enumerate(self.scores):
            if score >= 3:
                print(f'{self.players[i]} wins the game!')
                return True
        return False

    def start_game(self):
        while True:
            self.play_round()
            self.next_round()
            if self.check_winner():
                break
            if input('Continue to the next round? (y/n): ') != 'y':
                break

game = Game()
game.start_game()
