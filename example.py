from pyfrotz import Frotz
from pyfrotz.parsers import advent_intro_parser, planetfall_intro_parser
# load your game file
data = '/home/miro/PycharmProjects/OpenJarbas/pyFrotz/Advent.z5'
#data = "/home/miro/PycharmProjects/GameSkills/ovos-skill-planet-fall-game/res/planetfall.z5"
game = Frotz(data)


# use it inside code
#game_intro = game.get_intro()
#room, description = game.do_command("\n")



# or play in the cli
game = Frotz(data,
             intro_parser=advent_intro_parser)
game.play_loop()

