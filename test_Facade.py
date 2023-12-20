import random
import unittest
from io import StringIO
from unittest.mock import patch, mock_open
import pygame
from Facade import Facade


class TestFacade(unittest.TestCase):
    @patch('builtins.open')
    def test_LoadLevels(self, mock_open):
        facade = Facade()
        file_name = 'levels.txt'
        block_list = []
        color_blocks = []
        color_list = [(0xFF, 0x1C, 0x1C), (0x6A, 0xC7, 0x20), (0x43, 0x61, 0xFF),
                      (0xFF, 0xB2, 0x1C)]
        expected_block_list = [
            pygame.Rect(10, 10, 32, 32),
            pygame.Rect(94, 10, 32, 32),
            pygame.Rect(10, 52, 32, 32),
            pygame.Rect(94, 52, 32, 32),
            pygame.Rect(10, 94, 32, 32),
            pygame.Rect(94, 94, 32, 32)
        ]

        mock_open.return_value.__enter__.return_value = StringIO('0_0\n0_0\n0_0\n')

        with patch('os.path.exists') as mock_exists:
            mock_exists.return_value = True
            facade.LoadLevels(file_name, block_list, color_blocks, color_list)

        self.assertEqual(block_list, expected_block_list)
        self.assertEqual(len(color_blocks), len(block_list))
        self.assertIn(random.choice(color_blocks), color_list)

    @patch('builtins.open')
    def test_LoadRecords(self, mock_open):
        facade = Facade()
        text = []
        pygame.init()
        font1 = pygame.font.Font('big-shot.ttf', 20)

        mock_open.return_value.__enter__.return_value = StringIO('Ivan 1 1\nPetr 2 2\nZinar 3 3\n')
        with patch('os.path.exists') as mock_exists:
            mock_exists.return_value = True
            facade.LoadRecords('test_file.txt', text, font1)

        self.assertEqual(len(text), 3)

    def test_UpdateRecords(self):
        mock_file_content = [
            "player1 1 100\n",
            "player2 2 200\n",
            "player3 3 300\n"
        ]
        expected_file_content = [
            "player1 1 100\n",
            "player2 2 200\n",
            "player3 3 400\n"
        ]

        with patch('builtins.open', mock_open(read_data=''.join(mock_file_content))) as mock_file:
            obj = Facade()
            obj.UpdateRecords("имя_файла.txt", "player3", 3, 400)

            mock_file.assert_called_once_with("имя_файла.txt", 'r+')
            handle = mock_file.return_value.__enter__.return_value

            handle.writelines.assert_called_once_with(expected_file_content)
            handle.truncate.assert_called_once()


if __name__ == '__main__':
    unittest.main()
