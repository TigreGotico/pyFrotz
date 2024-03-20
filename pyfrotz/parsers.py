from quebra_frases import sentence_tokenize


def default_room_parser(output):
    # assume first line is the room name
    sents = sentence_tokenize(output)
    room = sents[0]
    return room, output


def default_intro_parser(game):
    # default to clearing everything until prompt
    # this clear all credits serial number etc
    game._clear_until_prompt()
    # request fresh description
    return game.do_command("look")


def advent_intro_parser(game):
    game._clear_until_prompt("***MORE***")  # consume intro
    game.do_command("")  # need a \n before it accepts prompts
    return """You are standing at the end of a road before a small brick building.
 Around you is a forest.
 A small stream flows out of the building and down a gully."""


def planetfall_intro_parser(game):
    game._frotz_read()
    return """Another routine day of drudgery aboard the Stellar Patrol Ship Feinstein. This
morning's assignment for a certain lowly Ensign Seventh Class: scrubbing the
filthy metal deck at the port end of Level Nine. With your Patrol-issue self-
contained multi-purpose all-weather scrub-brush you shine the floor with a
diligence born of the knowledge that at any moment dreaded Ensign First Class
Blather, the bane of your shipboard existence, could appear.

Deck Nine
This is a featureless corridor similar to every other corridor on the ship. It
curves away to starboard, and a gangway leads up. To port is the entrance to one
of the ship's primary escape pods. The pod bulkhead is closed.
"""


def stationfall_intro_parser(game):
    game._frotz_read()
    return """It's been five years since your planetfall on Resida. Your heroics in saving
that doomed world resulted in a big promotion, but your life of dull scrubwork
has been replaced by a life of dull paperwork. Today you find yourself amidst
the administrative maze of Deck Twelve on a typically exciting task: an
emergency mission to Space Station Gamma Delta Gamma 777-G 59/59 Sector Alpha-
Mu-79 to pick up a supply of Request for Stellar Patrol Issue Regulation Black
Form Binders Request Form Forms...

Deck Twelve
   You are in the heart of the administrative level of the ship, the largest
level of the S.P.S. Duffy or any other Stellar Patrol ship for that matter. The
corridor continues starboard and a room lies aft. Beyond the door to port lies
the bulk of the Duffy. Next to the door is a slot.
"""


def starcross_intro_parser(game):
    game._frotz_read()
    return """You are sound asleep in your bunk aboard the deep-space black hole prospecting
ship "Starcross," operating out of Ceres. Just as your sleep becomes deep and
comfortable, an alarm bell begins ringing! It's the mass detector! Instantly you
awake. This hasn't been a profitable trip so far, and you don't even have the
cash for repairs. This could be the break you've been waiting for.

Living Quarters
(You are in the bunk.)
This nook is your spartan living quarters, containing only a bunk and a bureau.
The only exit is to starboard.
There is a tape library here. (outside the bunk)
"""


def hhgg_intro_parser(game):
    game._frotz_read()
    return """You wake up. The room is spinning very gently round your head. Or at least it
would be if you could see it which you can't.

It is pitch black.
"""
