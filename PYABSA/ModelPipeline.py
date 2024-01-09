import spacy
import pickle

class Aspect:
    def __init__(self, model):
        self.model = model
        self.aspect_dict = {}

    def predict(self, text):
        text = text.split(' ')
        text = list(filter(lambda x: x != "", text))
        text = " ".join(text)

        result = self.model.predict(text)
        pos = result['position']
        asp = result['aspect']

        posasp = {}
        for i, j in zip(asp, pos):
            k = i.split(' ')
            # length of aspect less than or equals 2
            if len(k) <= 2:
                posasp[i] = j[0]

        print(posasp)
        # Load the English language model
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text)
        text = text.split(' ')
        for i in posasp:
            index = posasp[i]
            string = ''
            nextindex = index
            for j in text[index:]:
                string += j + ' '
                nextindex += 1
                j = nlp(j)
                if j[0].pos_ == 'ADJ' or j[0].pos_ == 'PRON':
                    try:
                        if nlp(text[nextindex])[0].pos_ == 'CCONJ':
                            continue
                    except IndexError:
                        pass
                    break

            cleaned_string = ''
            for nth in string.split(' '):
                if nth != i and nth in posasp.keys():
                    break
                cleaned_string += nth + ' '

            self.aspect_dict[i] = cleaned_string.strip()

        return self.aspect_dict


