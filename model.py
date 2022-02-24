import random
import json
import itertools
import math

with open('nbr_dict.json') as file:
    default_dictionary = json.load(file)

# with open('test_nbr_dict.json') as file:
#     default_dictionary = json.load(file)

#class NPC:
#  def __init__(self):
    
class Board:
    def __init__(self, dictionary = default_dictionary):
        self.dictionary = default_dictionary
        self.answer_word = random.choice(list(self.dictionary.keys()))
        self.guesses = []
        self.turn = 1

    def make_entropy_dict(self):
        entropy_dict = {}
        outcome_sequences = itertools.product(range(3),repeat=5)
        #print(list(outcome_sequences))
        possible_words = self.dictionary.keys()
        #print(list(outcome_sequences))
        seq_dict = {seq:[] for seq in outcome_sequences}
        # foreword: impossible words
        i=0
        while i <= 2:
            for word in possible_words:
            # First make a dictionary whose keys are the possible 5 digit responses and the values are words that if they were the answer would return that sequence.
              #QUESTION: WHY CAN't we just redefine seq_dict for each word????
                for key in seq_dict.keys():
                    seq_dict[key] =[]
              # print('im the empyt list!', seq_dict[tuple([2,2,0,0,0])])
              # print("toop in seqdict_keys",tuple([2,2,0,0,0]) in seq_dict.keys())
                word = Word(word)
                for word2 in possible_words:
                    seq = word.check2(word2) # <--- seq needs to be a tuple
                    seq_dict[seq].append(word2)
                  # Next we sum entropy over all possible sequences
                entropy = 0
                for seq in seq_dict.keys():
                    prob = len(seq_dict[seq])/len(possible_words) #<-- float?
                    if not prob == 0:
                        entropy += prob * math.log2(1/prob)
                    entropy_dict[word] = entropy
                i += 1
        return entropy_dict
    
    def npc_game(self):
        print("answer_word ", self.answer_word)
    
    def human_game(self):
        print("answer word ", self.answer_word)
        current_guess = Word(self.ask_for_guess())
        self.guesses.append(current_guess)
        while not current_guess.check(self.answer_word) == [2,2,2,2,2]:
            print("gamey guessY", current_guess.check(self.answer_word))
            self.turn += 1
            current_guess = Word(self.ask_for_guess())
            self.guesses.append(current_guess)
        if self.turn==1:
            print('You cheated!')
        else:
            print('You Win! it took you {turns} guesses.'.format(turns=self.turn))

    def ask_for_guess(self):
        return input("guess a word, you winner you: ").upper()

    def make_guess():
        guess = 'LUCAS' #ask user for word
        return(self.compare_words(self.answer_word,guess))

    def drift(nbr_dict):
        answer_word = random.random_choice(nbr_dict[answer_word])



class Word:
    def __init__(self, word_string):
        self.word_string = word_string
  
    def check(self, target_word):
        current_word=self.word_string
        # This method will return a dictonary, the keys are the letter position of the current word (ranging from 0-4) and the values are: 0 if wrong letter, 1 if right letter but wrong position, and 2 if right letter in correct position.
        correctness_list = [0,0,0,0,0] # <-- be thy a tuple but later!
        for i in range(len(self.word_string)):
          # set all to wrong first
          correctness_list[i] = 0
        # target_dict says where the letters in the target word are
        # keys are letters
        # values are indices where that letter occurs
        target_dict = {}
        for i in range(len(self.word_string)):
            if not target_word[i] in target_dict.keys():
                target_dict[target_word[i]] = [i]
            else:
                target_dict[target_word[i]].append(i)
        # go letter-by-letter in current word
        for i in range(len(self.word_string)):
            if current_word[i] in target_dict.keys():
                if i in target_dict[current_word[i]]:
                    correctness_list[i] = 2
                    target_dict[current_word[i]].remove(i)
        # Next we check for correct 
        for i in range(len(self.word_string)):
            if correctness_list[i] != 2:
                if current_word[i] in target_dict.keys():  
                    if len(target_dict[current_word[i]]) > 0:
                        correctness_list[i] = 1
                        target_dict[current_word[i]].remove(target_dict[current_word[i]][0])
        return tuple(correctness_list)

    def check2(self, target_word):
        # We reverse the word so we can look through it from right to left more easily
        current_word=self.word_string[::-1]
        target_word= target_word[::-1]
        # First set all entries to 1.
        correctness_list = [1,1,1,1,1]
        # Now we go through each letter from right to left.
        for i in range(len(self.word_string)):
            # If the letter is in the correct spot, we change the correctness to a 2 and delete it from the target word so that it won't count in the next step when we see which letters should be marked 0.
            if current_word[i] == target_word[i]:
                correctness_list[i]=2
                target_word.replace(current_word[i], '', 1)
            # If the number of matches of a letter in the target word is less than or equal to the number of letters to the left in the current word than it should be marked as a 0.
            elif target_word.count(current_word[i]) <= current_word[i+1:].count(current_word[i]):
                correctness_list[i]=0
        correctness_list= correctness_list[::-1]
        return tuple(correctness_list)

