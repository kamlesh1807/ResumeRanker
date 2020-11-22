import os, gensim, re
ROOT = os.path.dirname(os.path.realpath(__file__))
ModelName = "Model"

class ModelCreation():
    def __init__(self, root):
        self.root = root

    def __iter__(self):
        with open(self.root + '/files/' + 'sentences.txt', 'r', encoding='utf-8') as fin:
            for line in fin:
                review_text = re.sub("[^a-zA-Z]", " ", line)
                yield review_text.split()

sentenceG = ModelCreation(root= ROOT)
if not os.path.exists(ROOT + "/model"):
    os.makedirs(ROOT + "/model/")
model = gensim.models.Word2Vec(sentenceG, workers=4, size=300, min_count=1, window=15, sample=1e-3)
model.save(ROOT + '/model/' + ModelName)