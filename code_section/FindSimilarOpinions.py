import gensim.models.keyedvectors as word2vec


class FindSimilarOpinions:
    extracted_opinions = {}
    word2VecObject = []
    cosine_sim = 0

    def __init__(self, input_cosine_sim, input_extracted_ops):
        self.cosine_sim = input_cosine_sim
        self.extracted_opinions = input_extracted_ops
        word2vec_add = "data//assign4_word2vec_for_python.bin"
        self.word2VecObject = word2vec.KeyedVectors.load_word2vec_format(word2vec_add, binary=True)
        return

    def get_word_sim(self, word_1, word_2):
        return self.word2VecObject.similarity(word_1, word_2)

    def findSimilarOpinions(self, query_opinion):
        # example data, which you will need to remove in your real code. Only for demo.
        example_similarity = self.get_word_sim("great", "good")
        print("Similarity of 'great' and 'good' is " + str(example_similarity))
        similar_opinions = {'service, good': [1, 2, 3], 'service, excellent': [11, 12]}
        return similar_opinions
