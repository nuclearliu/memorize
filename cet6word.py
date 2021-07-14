class Word:
    def __init__(self, word, info):
        self.word = word
        self.info = info

        self.alreadyLearned = False
        self.toBeReviewed = False
        self.reviewCount = 0
        self.incorrectCount = 0
        self.mastered = False

        self.content = info[0]
        self.pronunciation = info[1]
        translate_end_line = 2
        # while info[translate_end_line].split()[0] in properties:
        #     translate_end_line += 1
        while info[translate_end_line][0:5] == "\x1b[34m":
            translate_end_line += 1
        self.translation = info[2:translate_end_line]
        self.rank = info[translate_end_line]
        self.example = info[translate_end_line + 2:]

    def getInfo(self):
        print(self.content, end="")
        print(self.pronunciation, end="")
        for line in self.translation:
            print(line, end="")
        print(self.rank)
        for line in self.example:
            print(line, end="")
