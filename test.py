class Board:
    def __init__(self):
        self.board = [" " for _ in range(9)]  # Represents 9 positions

    def display(self):
        print(f"{self.board[0]} | {self.board[1]} | {self.board[2]}")
        print("--+---+--")
        print(f"{self.board[3]} | {self.board[4]} | {self.board[5]}")
        print("--+---+--")
        print(f"{self.board[6]} | {self.board[7]} | {self.board[8]}")

    def update(self, position, marker):
        if 0 <= position < 9 and self.board[position] == " ":
            self.board[position] = marker
            return True
        return False

    def is_winner(self, marker):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]            # Diagonals
        ]
        for combo in winning_combinations:
            if all(self.board[i] == marker for i in combo):
                return True
        return False

    def is_draw(self):
        return all(spot != " " for spot in self.board)
    
test = Board()

test.display()