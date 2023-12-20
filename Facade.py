import os
import random
import pygame

class Facade:
    def LoadLevels(self, file_name, block_list, color_blocks, color_list):
        if not os.path.exists(file_name):
            return []
        with open(file_name, 'r') as f:
            raws = f.readlines()
            for i, raw in enumerate(raws):
                for j, char in enumerate(raw):
                    if char == '0':
                        block_list.append(pygame.Rect(10 + 42 * j, 10 + 42 * i, 32, 32))
                        color_blocks.append(random.choice(color_list))
                    else:
                        continue

    def LoadRecords(self, file_name, text, font1):
        if not os.path.exists(file_name):
            return []
        with open(file_name, 'r') as f:
            raws = f.readlines()
        for i, raw in enumerate(raws):
            text.append(font1.render(raw.strip(), True, (0xF5, 0xF5, 0xF5)))

    # def SaveRecords(self, file_name, text, font1):
    #     if not os.path.exists(file_name):
    #         return []
    #     with open(file_name, 'w') as f:
    #         raws = f.readlines()
    #     for i, raw in enumerate(raws):
    #         text.append(font1.render(raw.strip(), True, (0xF5, 0xF5, 0xF5)))

    def UpdateRecords(self, file, player_name, player_lvl, player_score):
        with open(file, 'r+') as f:
            raws = f.readlines()
            for i, raw in enumerate(raws):
                if raw.strip().split()[0] == player_name and int(raw.strip().split()[1]) == player_lvl and int(raw.strip().split()[2]) < player_score:
                    raws[i] = f"{raw.strip().split()[0]} {raw.strip().split()[1]} {str(player_score)}\n"
                    f.seek(0)
                    f.writelines(raws)
                    f.truncate()
                    break
            # else:
            #     raws.append(f"{player_name} {player_lvl} {str(player_score)}\n")
            #     f.seek(0)
            #     f.writelines(raws)
            #     f.truncate()