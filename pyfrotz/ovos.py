import os.path
from os.path import expanduser

from ovos_utils.xdg_utils import xdg_cache_home
from ovos_workshop.skills.game_skill import ConversationalGameSkill
from quebra_frases import sentence_tokenize
from ovos_utils.lang import standardize_lang_tag
from pyfrotz import Frotz


class FrotzSkill(ConversationalGameSkill):
    def __init__(self,
                 game_id: str,
                 game_data: str = None,
                 skill_voc_filename: str = None,
                 game_lang="en-us",
                 intro_parser=None,
                 skill_icon=None,
                 game_image=None,
                 *args, **kwargs):
        # TODO use path from gui cache path to ensure docker compat
        game_image = game_image or os.path.join(os.path.dirname(__file__), "gui", "all", "bg.png")
        skill_icon = skill_icon or os.path.join(os.path.dirname(__file__), "gui", "all", "pyfrotz.png")
        super().__init__(skill_voc_filename=skill_voc_filename or game_id,
                         skill_icon=skill_icon, game_image=game_image,
                         *args, **kwargs)
        self.game_lang = standardize_lang_tag(game_lang).split("-")[0]
        self.game_id = game_id
        self.game = None
        self.save_file = expanduser(f"{xdg_cache_home()}/{self.game_id}.save")
        self.game_data = game_data or f'{self.root_dir}/res/{self.game_id}.z5'
        self.log.info(f"game data: {self.game_data} ## save file: {self.save_file}")
        self.intro_parser = intro_parser

    def on_play_game(self):
        """called by ocp_pipeline when 'play XXX' matches the game"""
        if self.game is None:
            self.game = Frotz(self.game_data,
                              intro_parser=self.intro_parser,
                              save_file=self.save_file)
        if self.settings.get("auto_save", False) and os.path.isfile(self.save_file):
            self.game.restore(self.save_file)
            self.speak_dialog("game.restore")
        else:
            self.game.parse_intro()
            self.speak_output(self.game.intro)
        self.do_command("look")

    def on_save_game(self):
        """skills can override method to implement functioonality"""
        self.game.save()
        self.speak_dialog("game.saved")

    def on_load_game(self):
        """skills can override method to implement functioonality"""
        if os.path.isfile(self.save_file):
            self.game.restore(self.save_file)
            self.speak_dialog("game.restore")
        else:
            super().on_load_game()  # to speak default error dialog

    def on_stop_game(self):
        """called when game is stopped for any reason
        auto-save may be implemented here"""
        self.game = None
        self.speak_dialog("game.ended")
        self.gui.release()

    def on_game_command(self, utterance: str, lang: str):
        """pipe user input that wasnt caught by intents to the game
        do any intent matching or normalization here
        don't forget to self.speak the game output too!
        """
        if self.game.game_ended():
            self.game_over()
            return
        lang = standardize_lang_tag(lang).split("-")[0]
        autotranslate = lang != self.game_lang
        if autotranslate:
            utterance = self.translator.translate(utterance,
                                                  target=self.game_lang,
                                                  source=lang)
        # this may return empty string if the game ended
        answer = self.game.do_command(utterance)
        if not answer:
            self.game_over()
        else:
            if autotranslate:
                answer = self.translator.translate(answer,
                                                   target=lang,
                                                   source=self.game_lang)
            self.speak_output(answer)

    def on_abandon_game(self):
        """user abandoned game mid interaction

        auto-save is done before this method is called
        (if enabled in self.settings)

        on_game_stop will be called after this handler"""
        self.gui.release()

    def speak_output(self, line):
        # replace type with say because its voice game
        lines = [(l, False) for l in sentence_tokenize(line.replace("type", "say"))]
        # set listen flag
        lines[-1] = (lines[-1][0], True)

        for line, listen in lines:
            self.gui.show_image(self.game_image, caption=line, title=self.game_id,
                                override_idle=True)
            self.speak(line.strip(), wait=True, expect_response=listen)
