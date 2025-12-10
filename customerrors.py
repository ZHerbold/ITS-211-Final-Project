# CUSTOM ERRORS
# This error is meant to be thrown when player choses something other than heal/attack/quit
class InvalidGameChoice(Exception):
    pass

# This error is meant to be thrown when player chooses an enemy that does not exist
class InvalidEnemyChoice(Exception):
    pass

# This error is meant to be thrown when player chooses an invalid choice when trying to quit
class QuitError(Exception):
    pass

# This error is meant to be thrown when the player chooses an invalid choice when trying to either retry the floor or reset the game
class RestartError(Exception):
    pass

class DeadEnemyError(Exception):
    pass
