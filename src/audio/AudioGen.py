import gtts
import os

from src.database.Schema import UserSchema


class AudioGen:
    def __init__(self, base_path='data/audio/', **kwargs):
        self._kwargs = kwargs
        self._base_path = base_path

        if not(os.path.isdir(self._base_path)):
            os.mkdir(self._base_path)

    def generateTTS(self, fileName: str, msg: str, **kwargs):
        kwargs = self._kwargs|kwargs
        tts = gtts.tts.gTTS(msg, **kwargs)
        tts.save(self._base_path + fileName + ".mp3")

    def generateNickname(self, user:UserSchema, **kwargs):
        kwargs = self._kwargs|kwargs
        fileName = f"{user.user_name}_{user.guild_id}_{user.user_id}"
        self.generateTTS(fileName=fileName, msg=user.nickname, **kwargs)

    def setKwargs(self, **kwargs):
        self._kwargs = self._kwargs|kwargs

    def getKwargs(self):
        return self._kwargs

    def setDefaultAccent(self, lang='en'):
        self._kwargs['lang'] = lang

    def getDefaultAccent(self):
        return self._kwargs['lang']

    def setBasePath(self, base_path='data/audio/'):
        self._base_path = base_path

    def getBasePath(self):
        return self._base_path


if __name__ == "__main__":
    gen = AudioGen(base_path='data/audio/tests/')
    gen.generateTTS('test', 'abcdefghijklmnopqrstuvwxyz')
    gen.generateNickname('testname', 'testname, nickname', 1,2)
    gen.setKwargs(tld='co.in')
    gen.generateTTS('test', 'Hello, how are you')

