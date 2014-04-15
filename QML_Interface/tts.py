import urllib
import urllib3
import tempfile
import pygame


class tts:

    def __init__(self, lang = "fr"):
        self.lang = lang

    def speak(self, text):
        parameter = urllib.parse.urlencode({"q": text, "tl": self.lang, "ie": "UTF-8"})
        api_url = "http://translate.google.fr/translate_tts?%s"%parameter

        http = urllib3.PoolManager()
        r = http.request('GET', api_url, None, {'Referer': ''})
        assert(r.status == 200)
        try:
            with tempfile.NamedTemporaryFile('w+b', 0) as mp3file:
                mp3file.write(r.data)
                pygame.mixer.music.load(mp3file.name)
                pygame.mixer.music.play()

        finally:
            r.release_conn()

if pygame.mixer.get_init() is None:
    pygame.mixer.init(16000)
