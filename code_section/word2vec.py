# from gensim.models import Word2Vec
import gensim.models.keyedvectors as word2vec


# path_to_word2vec="D:\\Projects\\AllData\\dataset-word2vec-skipgram-google\\GoogleNews-vectors-negative300.bin"
# path_to_word2vec_txt="D:\\Projects\\AllData\\dataset-word2vec-skipgram-google\\GoogleNews-vectors-negative300.txt"
# embed_map = word2vec.KeyedVectors.load_word2vec_format(path_to_word2vec, binary=True)
# embed_map.save_word2vec_format(path_to_word2vec_txt, binary=False)


path_to_word2vec="../assign4_word2vec.txt"
path_to_word2vec_txt="../assign4_word2vec_for_python.bin"
embed_map = word2vec.KeyedVectors.load_word2vec_format(path_to_word2vec_txt, binary=True)
print(embed_map.similarity('good', 'bad'))

print(embed_map.similarity('attentive', 'good'))

# allergy,  food
# food, delicious
embed_map.save_word2vec_format(path_to_word2vec_txt, binary=True)