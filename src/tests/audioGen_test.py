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
        user.nickname
        generated_file_path = audioGen.generateNickname(user=user)
        fileName = f"{audioGen._base_path}default_{user.guild_id}_{user.user_id}.mp3"
        assert fileName == generated_file_path


if __name__ == "__main__":
    unittest.main()
