
class ClassicGameRules:
    """
    These game rules manage the control flow of a game, deciding when
    and how the game starts and ends.
    """

    def __init__(self, timeout=30):
        self.timeout = timeout

    def newGame(self, layout, pacmanAgent, ghostAgents, display, quiet=False, catchExceptions=False):
        agents = [pacmanAgent] + ghostAgents[:layout.getNumGhosts()]
        initState = GameState()
        initState.initialize(layout, len(ghostAgents))
        game = Game(agents, display, self, catchExceptions=catchExceptions)
        game.state = initState
        self.initialState = initState.deepCopy()
        self.quiet = quiet
        return game

    def process(self, state, game):
        """
        Checks to see whether it is time to end the game.
        """
        if state.isWin(): self.win(state, game)
        if state.isLose(): self.lose(state, game)

    # def win(self, state, game):
    #     if not self.quiet: print("Pacman emerges victorious! Score: %d" % state.data.score)
    #     game.gameOver = True
    #
    # def lose(self, state, game):
    #     if not self.quiet: print("Pacman died! Score: %d" % state.data.score)
    #     game.gameOver = True
    #
    # def getProgress(self, game):
    #     return float(game.state.getNumFood()) / self.initialState.getNumFood()

    # def agentCrash(self, game, agentIndex):
    #     if agentIndex == 0:
    #         print("Pacman crashed")
    #     else:
    #         print("A ghost crashed")

