import random


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

        # DELETE THESE 2 LINES OF CODE AFTER DONE DEBUG
        # print(self.board)
        # Sentence(self.mines, mines)

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

    def __init__(self, cells, count):
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
        # If length of set of cells and count are same, all aret mines
        if self.count == len(self.cells) and self.count != 0:
            return self.cells
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # If count is 0, all nearby are safe cells
        if self.count == 0:
            return self.cells
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # If cell is a mine,
        # remove its presence from sentence and decrease count
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # If cell is a safe, remove its presence from sentence
        if cell in self.cells:
            self.cells.remove(cell)


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
        # Mark the cell as safe and add it to the moves made
        self.moves_made.add(cell)
        self.mark_safe(cell)

        # All possible nearby cells
        possible_cells = set()

        # Iterate over neighboring cells
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Skip the current cell if it has already been explored
                if (i, j) in self.moves_made:
                    continue

                # Skip the current cell if it is known to be safe
                if (i, j) in self.safes:
                    continue

                # Decrement count if the current cell is a known mine
                if (i, j) in self.mines:
                    count -= 1
                    continue

                # Add the current cell to the set of possible cells
                elif 0 <= i < self.height and 0 <= j < self.width:
                    possible_cells.add((i, j))

        # Add a new sentence to the knowledge base
        self.knowledge.append(Sentence(possible_cells, count))
        changes = True

        # While there are changes made to knowledge base
        while changes:
            changes = False

            # Update mines and safes based on the knowledge base
            mines = set()
            safes = set()
            for sentence in self.knowledge:
                if len(sentence.cells) == 0:
                    self.knowledge.remove(sentence)
                else:
                    mines.update(sentence.known_mines())
                    safes.update(sentence.known_safes())

            # Mark inferred safes and mines
            for mine in mines:
                changes = True
                self.mark_mine(mine)
            for safe in safes:
                changes = True
                self.mark_safe(safe)

            # Infer mines from subsets of sets in the knowledge base
            for sentence1 in self.knowledge:
                for sentence2 in self.knowledge:

                    if sentence1.cells == sentence2.cells:
                        continue
                    if sentence1.cells.issubset(sentence2.cells):
                        new_sentence_cells = sentence2.cells - sentence1.cells
                        new_sentence_count = sentence2.count - sentence1.count
                        new_sentence = Sentence(new_sentence_cells, new_sentence_count)
                        if new_sentence not in self.knowledge:
                            changes = True
                            self.knowledge.append(new_sentence)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # Cells that are in safe and not in moves made and not in mines
        safe_moves = (self.safes - self.moves_made) - self.mines
        if safe_moves:
            return random.choice(list(safe_moves))

        # Return none if no cell available
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # Traverse board, and cells those are not in moves made
        # and not in mines are cells that are picked randomly
        random_moves = []

        for i in range(self.height):
            for j in range(self.width):

                move = (i, j)
                if move not in self.moves_made:
                    if move not in self.mines:
                        random_moves.append(move)

        if random_moves:
            return random.choice(random_moves)

        return None
