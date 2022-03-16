import gtts
import os

from src.database.Schema import NicknamesSchema, UserSchema
from src.logging.logger import Logger

logger = Logger(__name__)

class AudioGen:
    def __init__(self, base_path='data/audio/', **kwargs):
        self._kwargs = kwargs
        self._base_path = base_path

        if not(os.path.isdir(self._base_path)):
            os.mkdir(self._base_path)

    def generateTTS(self, path: str, msg: str, **kwargs):
        kwargs = self._kwargs | kwargs
        tts = gtts.tts.gTTS(msg, **kwargs)
        tts.save(path)
        return path

    def generateNickname(self, user: UserSchema|NicknamesSchema, **kwargs):
        kwargs = self._kwargs | kwargs
        fileName = f"default_{user.guild_id}_{user.user_id}"
        nickname = user.nickname if user.nickname is not None else user.user_name
        path = os.path.join(self._base_path, fileName + ".mp3")
        if user.default_audio_path != path or not(os.path.exists(path)):
            logger.info(f"Generating audio for {user.user_name} at {path}")
            self.generateTTS(path=path, msg=nickname, **kwargs)  
        else:
            logger.info(f"Audio path for {user.user_name} already exists, not regenerating")
        return path

    def setKwargs(self, **kwargs):
        self._kwargs = self._kwargs | kwargs

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
    user = UserSchema(volume=167548932.0, user_name='test_name',
                      nickname='abcd', user_id=1, guild_id=100)
    print(user)
    gen = AudioGen(base_path='data/audio/tests/')
    gen.generateTTS('test', 'abcdefghijklmnopqrstuvwxyz')
    gen.generateNickname(user=user)
    gen.setKwargs(tld='co.in')
    gen.generateTTS('test', 'Hello, how are you')
