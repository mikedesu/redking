import unittest

from RedKingBot import RedKingBot


class TestRedKingBot(unittest.TestCase):
    def test_get_response(self):
        bot = RedKingBot(9001)
        addr = bot.virtual_address
        assert addr >= 0 and addr <= 1


if __name__ == "__main__":
    unittest.main()
