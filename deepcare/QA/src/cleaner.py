import string
from pyvi import ViTokenizer

def Load_Stopword():
    stopwords = []
    with open("./src/stopwords/vietnamese-stopwords-dash.txt") as f:
        for line in f:
            stopwords.append(line[:-1])
    stopwords.pop() # remove '' at the end of list
    return stopwords

class Cleaner:
    def __init__(self) -> None:
        self.stopwords = Load_Stopword()
    
    @staticmethod
    def remove_special_character(text):
        delete_dict = {sp_character: ' ' for sp_character in string.punctuation}
        table = str.maketrans(delete_dict)
        return text.translate(table) 
    
    @staticmethod
    def clean_space(text):
        return " ".join(text.split())

    @staticmethod
    def tokenizer(text):
        return ViTokenizer.tokenize(text)

    def remove_stopwords(self, text):
        text = text.split()
        for word in self.stopwords:
            if word in text:
                text.remove(word)
        return " ".join(text)

    def run(self, text):
        # Convert to lower
        text = text.lower()
        # Remove special character
        text = self.remove_special_character(text)
        # Clean space
        text = self.clean_space(text)
        # Tokenization
        text = self.tokenizer(text)
        # Remove stop word
        text_rm = self.remove_stopwords(text)
        # [option] process synonym
        # [option] remove number
        if text_rm == '':
            return text
        return text_rm


if __name__ == '__main__':
    clean = Cleaner()
    text = "Xin chào toàn thể bà con cô ^ bác,chú, dì ạ. Họ   là  #$%   Hàng nội Ngoại 098888 đâu đó ai kia giãy đành đạch, cùng chung niềm hạnh phúc"
    text = clean.run(text)
    print(text)


        