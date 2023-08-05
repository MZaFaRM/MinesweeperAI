import itertools
import random
import re


class Minesweeper:
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):
        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence:
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count, source):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        known_safes = self.known_safes() or set()
        remaining_cells = self.cells - known_safes
        return remaining_cells.copy() if len(remaining_cells) <= self.count else set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        return self.cells.copy() if self.count <= 0 else set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.discard(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.discard(cell)


class MinesweeperAI:
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):
        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)


    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        
        self.moves_made.add(cell)
        neighbors = self.neighboring_cells(cell)
        sentence = Sentence([cell, *neighbors], count)

        self.knowledge.append(sentence)
        self.mark_safe(cell)

        for sentence in self.knowledge: 
            self.handle_mines(sentence)
            self.handle_safes(sentence)

        for i in range(len(self.knowledge)):
            for j in range(len(self.knowledge)):
                sentence = self.knowledge[i]
                other_sentence = self.knowledge[j]

                if other_sentence.cells <= sentence.cells:
                    if new_cells := sentence.cells - other_sentence.cells:
                        new_count = sentence.count - other_sentence.count
                        new_sentence = Sentence(new_cells, new_count)
                        self.knowledge.append(new_sentence)

                        self.handle_mines(new_sentence)
                        self.handle_safes(new_sentence)

        self.remove_duplicates()
        self.remove_empty_sentences()

    def remove_duplicates(self):
        unique_sentences = []
        seen_cells = set()

        for sentence in self.knowledge:
            key = (tuple(sorted(sentence.cells)), sentence.count)

            if key not in seen_cells:
                unique_sentences.append(sentence)
                seen_cells.add(key)

        self.knowledge = unique_sentences
    
    def remove_empty_sentences(self):
        for sentence in self.knowledge:
            if not sentence.cells and not sentence.count:
                self.knowledge.remove(sentence)

    def handle_mines(self, sentence):
        if mines := sentence.known_mines():
            for mine in mines:
                self.mines.add(mine)
                for other in self.knowledge:
                    other.mark_mine(mine)

        if self.mines:
            for cell in sentence.cells.copy():
                if cell in self.mines:
                    sentence.mark_mine(cell)
                    
    def handle_safes(self, sentence):
        if safes := sentence.known_safes():
            for safe in safes:
                self.safes.add(safe)
                for other in self.knowledge:
                    other.mark_safe(safe)

        if self.safes:
            sentence.cells -= self.safes

    def neighboring_cells(self, cell):
        """
        Returns the list of neighboring cells given a cell.
        """
        i, j = cell
        il = [i + k for k in range(-1, 2) if 0 <= i + k <= self.height - 1]
        jl = [j + k for k in range(-1, 2) if 0 <= j + k <= self.width - 1]
        return {(x, y) for x in il for y in jl if (x, y) != cell}

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        if safe_moves := (self.safes - self.moves_made):
            choice = random.choice(list(safe_moves))
            return choice
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        all_moves = {(i, j) for i in range(self.height) for j in range(self.width)}

        if remaining_moves := list(all_moves - self.moves_made - self.mines):
            choice = random.choice(remaining_moves)
            return choice
        return None
