# PyFrotz

**PyFrotz** is a minimal Python wrapper around [Frotz](https://gitlab.com/DavidGriffith/frotz), a popular interpreter for Infocom's text adventure games. It complies with the Z-Machine Standard version 1.1, making it compatible with classic interactive fiction.

 <img src='./pyfrotz/gui/all/pyfrotz.png' card_color='#00ff00' width='150' height='150' style='vertical-align:bottom'/> 

Get some classic games to try [@The Obsessively Complete Infocom Catalog](https://eblong.com/infocom/). 

Source code for a lot of infocom games can be found [@historicalsource](https://github.com/historicalsource)

---

## Installation

First, install the PyFrotz Python package via pip:

```bash
pip install pyfrotz
```

Additionally, ensure you have [dfrotz](https://gitlab.com/DavidGriffith/frotz.git) installed on your system. It is often packaged as `frotz-dumb` in Linux distributions.

---

## Usage

PyFrotz can be used programmatically or interactively in the command line interface (CLI).

### Programmatic Usage

```python
from pyfrotz import Frotz

# Load your game file
data = '/path/to/your/game/data.z5'
game = Frotz(data)

# Interact with the game in your code
game_intro = game.get_intro()
room, description = game.do_command("look")
game.save()  # Optionally pass filename, default='save.qzl'
game.restore()  # Optionally pass filename, default='save.qzl'
```

### CLI Gameplay

You can also play games directly in the CLI:

```python
from pyfrotz import Frotz

data = '/path/to/your/game/data.z5'

game = Frotz(data)
game.play_loop()
```

---

## Integration with OVOS Skills

PyFrotz can be utilized as a voice-based interpreter for Infocom and other Z-Machine games. It enables seamless integration with OpenVoiceOS (OVOS) through a provided template class for wrapping games into skills.

### Existing Game Skills

Several prebuilt OVOS skills based on PyFrotz are available:

- [Planetfall Game](https://github.com/JarbasSkills/ovos-skill-planet-fall-game)
- [Stationfall Game](https://github.com/JarbasSkills/ovos-skill-station-fall-game)
- [Starcross Game](https://github.com/JarbasSkills/ovos-skill-starcross-game)
- [The Hitchhiker's Guide to the Galaxy](https://github.com/JarbasSkills/ovos-skill-hhgg-game)
- [White House Adventure](https://github.com/OVOSHatchery/ovos-skill-white-house-adventure)
- [Zork II](https://github.com/JarbasSkills/ovos-skill-zork2-game)
- [Zork III](https://github.com/JarbasSkills/ovos-skill-zork3-game)
- [Zork 0](https://github.com/JarbasSkills/ovos-skill-zork0-game)
- [Colossal Cave Adventure](https://github.com/OVOSHatchery/ovos-skill-cave-adventure-game)

---

Enjoy bringing these timeless text-based adventures to life with PyFrotz!

