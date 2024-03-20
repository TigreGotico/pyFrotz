import os.path
from os.path import expanduser

from ovos_bus_client.message import Message
from ovos_utils.xdg_utils import xdg_cache_home
from ovos_workshop.skills.auto_translatable import UniversalSkill
from quebra_frases import sentence_tokenize

from pyfrotz import Frotz


class FrotzSkill(UniversalSkill):
    def __init__(self, game_id: str,
                 game_data:str = None,
                 game_lang="en-us",
                 intro_parser=None,
                 *args, **kwargs):
        # game is english only, apply bidirectional translation
        super().__init__(internal_language=game_lang, *args, **kwargs)
        self.game_id = game_id
        self.playing = False
        self.game = None
        self.save_file = expanduser(f"{xdg_cache_home()}/{self.game_id}.save")
        self.game_data = game_data or f'{self.root_dir}/res/{self.game_id}.z5'
        self.log.info(f"game data: {self.game_data} ## save file: {self.save_file}")
        self.intro_parser = intro_parser

    def initialize(self):
        # async commands due to converse timeout!
        self.add_event(f"frotz.{self.game_id}.cmd", self._async_cmd)

    # converse
    def _async_cmd(self, message):
        utt = message.data["utterance"]
        self.do_command(utt)
        # check for game end
        if self.game.game_ended():
            self.game_over()

    def converse(self, message):
        utterances = message.data["utterances"]
        if self.playing:
            # capture speech and pipe to the game
            # NOTE this is too slow, converse times out and we get double
            # intents, delay execution and return now!
            self.bus.emit(Message(f"frotz.{self.game_id}.cmd",
                                  {"utterance": utterances[0]}))
            return True
        return False

    def handle_deactivate(self, message: Message):
        """
        Called when this skill is no longer considered active by the intent
        service;
        """
        if self.playing:
            self.speak_dialog("game.timeout")
            self.handle_save()
            self.game_over()

    # game wrappers
    def game_over(self):
        self.playing = False
        self.game = None
        self.speak_dialog("game.ended")

    def do_command(self, utterance):
        if self.game.game_ended():
            self.game_over()
            return
        # this may return empty string if the game ended
        data = self.game.do_command(utterance)
        if not data:
            self.game_over()
        else:
            self.speak_output(data)

    def speak_output(self, line):
        # replace type with say because its voice game
        lines = [(l, False) for l in sentence_tokenize(line.replace("type", "say"))]
        # set listen flag
        lines[-1] = (lines[-1][0], True)

        for line, listen in lines:
            # TODO nice background picture
            self.gui.show_text(line)
            self.speak(line.strip(), wait=True, expect_response=listen)

    def save_game(self):
        self.game.save()
        self.speak_dialog("game.saved")

    def exit_game(self, save=True):
        if save:
            self.save_game()
            self.speak_dialog("game.exit")
        else:
            self.speak_dialog("game.ended")

    def start_game(self, load_save=True):
        self.playing = True
        if self.game is None:
            self.game = Frotz(self.game_data,
                              intro_parser=self.intro_parser,
                              save_file=self.save_file)

        if load_save and os.path.isfile(self.save_file):
            self.game.restore(self.save_file)
            self.speak_dialog("game.restore")
        else:
            self.game.parse_intro()
            self.speak_output(self.game.intro)
        self.do_command("look")
