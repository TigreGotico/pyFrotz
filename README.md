# PyFrotz

 <img src='./pyfrotz/gui/all/pyfrotz.png' card_color='#00ff00' width='150' height='150' style='vertical-align:bottom'/> 

minimal python wrapper around [Frotz](https://gitlab.com/DavidGriffith/frotz)

get some classic games to try it out [here](https://if.illuminion.de/infocom.html)


# install

install the python package from pip

```bash
pip install pyfrotz
```

you also need [dfrotz](https://gitlab.com/DavidGriffith/frotz.git) available, sometimes packaged as `frotz-dumb`

# usage

```python
from pyfrotz import Frotz

# load your game file
data = '/home/user/PycharmProjects/infocom-games-skill/planetfall.z5'
game = Frotz(data)


# use it inside code
game_intro = game.get_intro()
room, description = game.do_command("look")
game.save()  # optionally pass filename, default='save.qzl'
game.restore()  # optionally pass filename, default='save.qzl'


# or play in the cli
game = Frotz(data)
game.play_loop()
```
