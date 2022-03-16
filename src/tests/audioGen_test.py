import unittest
from src.database.Schema import UserSchema
from src.audio.AudioGen import AudioGen
import glob

class AudioGen_test(unittest.TestCase):
    def test_generateNickname(self):
        audioGen = AudioGen()
        user = UserSchema()
        user.guild_id = 1
        user.user_name = "user_name"
        user.user_id = 10
        user.guild_name = "guild_name"
        audioGen.generateNickname(user=user)
        fileName = f"{user.user_name}_{user.guild_id}_{user.user_id}.mp3"
        assert len(glob.glob(audioGen._base_path + "/" + fileName)) > 0


if __name__ == "__main__":
    unittest.main()