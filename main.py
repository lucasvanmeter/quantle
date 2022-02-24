import model

# this is gonna be sick!!!

game = model.Board()

#game.npc_game()

gd = game.make_entropy_dict()

max_key = max(gd, key=gd.get)

print(max_key.word_string)

# test_word = model.Word('LUCAS')
# print('results of check1 are',test_word.check('MASSU'))