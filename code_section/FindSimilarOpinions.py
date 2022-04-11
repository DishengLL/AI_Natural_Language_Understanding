import gensim.models.keyedvectors as word2vec
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

ps = PorterStemmer()

class FindSimilarOpinions:
    extracted_opinions = {}
    word2VecObject = []
    cosine_sim = 0

    # input_extracted_ops --- a dicttionary containing {review text: [docId]}
    def __init__(self, input_cosine_sim, input_extracted_ops):
        self.cosine_sim = input_cosine_sim
        self.extracted_opinions = input_extracted_ops
        word2vec_add = "data//assign4_word2vec_for_python.bin"
        self.word2VecObject = word2vec.KeyedVectors.load_word2vec_format(word2vec_add, binary=True)
        token_corpus = {}

        # token_corpus dict ---- {token: [doc_ID]}
        for i, j in input_extracted_ops.items():
            a, b = i.split(',  ')
            token_corpus[a] = token_corpus.get(a, []) + j
            token_corpus[b] = token_corpus.get(b, []) + j
        self.token_corpus = token_corpus
        # print(input_extracted_ops)
        # print('the number of token in the corpus:',len(self.token_corpus ))
        return

    def get_word_sim(self, word_1, word_2):
        return self.word2VecObject.similarity(word_1, word_2)

    def similar_or_not(self, n, opinion, similar_,id):
        # get similar token in the whole dataset
        count=0
        try:
            example_similarity = self.get_word_sim(opinion, n)

            if example_similarity >= self.cosine_sim:
                similar_[opinion] = (example_similarity,id)

        except KeyError:
            #                 print(f'do not exist this term: **{opinion}**, the program just skip this term and continue to run following term')
            try:
                example_similarity = self.get_word_sim(opinion.lower(), n)
                if example_similarity >= self.cosine_sim:
                    similar_[opinion] = (example_similarity,id)

            except:
                #                     print(f'>>do not exist this term: **{opinion.lower()}**, the program just skip this term and continue to run following term')
                try:
                    if example_similarity >= self.cosine_sim:
                        similar_[opinion] = (example_similarity,id)
                except:
                    #                         print(f'>>>>do not exist this term: **{ps.stem(opinion.lower())}**, the program just skip this term and continue to run following term\n')
                    count += 1
        # print(type(similar_))
        # similar_ = sorted(similar_.items(), reverse=True, key=lambda kv: kv[1][0])
        return similar_

    def similar_or_not_2(self, n,opinion):
        try:
            example_similarity = self.get_word_sim(opinion, n)
            return example_similarity

        except KeyError:
            #                 print(f'do not exist this term: **{opinion}**, the program just skip this term and continue to run following term')
            try:
                example_similarity = self.get_word_sim(opinion.lower(), n)

                return example_similarity

            except:
                #                     print(f'>>do not exist this term: **{opinion.lower()}**, the program just skip this term and continue to run following term')
                try:
                    example_similarity = self.get_word_sim(ps.stem(opinion.lower()), n)
                    return example_similarity
                except:
                    #                         print(f'>>>>do not exist this term: **{ps.stem(opinion.lower())}**, the program just skip this term and continue to run following term\n')
                    return 0
        # print(type(similar_))
        # similar_ = sorted(similar_.items(), reverse=True, key=lambda kv: kv[1][0])



    def findSimilarOpinions(self, query_opinion):
        # example data, which you will need to remove in your real code. Only for demo.
        # example_similarity = self.get_word_sim("great", "good")
        # print("Similarity of 'great' and 'good' is " + str(example_similarity))
        # similar_opinions = {'service, good': [1, 2, 3], 'service, excellent': [11, 12]}
        # query_opinion ---- input opinion

######### strategy 1 --- intersection method
        # similar_nn = {}  # store similar token--nn
        # similar_adj = {}  # store similar token--adj
        # similar_opinions = {}  # get final similar review
        # n, adj = query_opinion.split(', ')  # get NN and adj in the query review
        # count = 0  # count the number of missing token in small word2vec database

        # print(self.token_corpus.items())
        # # get similar token in the whole dataset
        # for opinion,id in self.token_corpus.items():
        #     similar_nn = self.similar_or_not(n, opinion, similar_nn,id)
        # for opinion,id in self.token_corpus.items():
        #     similar_adj = self.similar_or_not(adj, opinion, similar_adj,id)
        # print(similar_nn)
        # print(similar_adj)
        # similar_nn_l = []
        # similar_adj_l = []
        # for _,j in similar_nn.items():
        #     similar_nn_l.extend(j[-1])
        # for _, j in similar_adj.items():
        #     similar_adj_l.extend(j[-1])
        # # print(similar_nn_l)
        # # print(similar_adj_l)
        # intersecion = set(similar_adj_l).intersection(set(similar_nn_l))
        # print(intersecion)
        #
        # for ind in  intersecion:
        #     for i,j in self.extracted_opinions.items():
        #          if ind in j:
        #             similar_opinions[i] = self.extracted_opinions.get(i)
        #             break
        # print(similar_opinions)


####### strategy 2----- combination method
        similar_opinions = {}
        qurey_pair = query_opinion.split(', ')
        for i in self.extracted_opinions:
            flag_ = -1    #make sure each token in query can only match only one token in corpus which has not be mateched
            corpus_pair = i.split(',  ')
            res = 0
            for int_ind,j in enumerate(qurey_pair):
                tem= float('-inf')
                for flag, k in enumerate(corpus_pair):
                    if flag == flag_ :
                        continue
                    else:

                        j_k = self.similar_or_not_2(j,k)
                        if j_k>tem:
                            # print('here',j,k,flag,flag_)
                            tem = j_k
                            if int_ind==0:
                                flag_ = flag

                res+=(tem) if tem<.8 else .8

            if res > 2*self.cosine_sim:
                similar_opinions[i]=self.extracted_opinions[i]
                # print(i)
                # print('flag_',flag_)
                # print(res)
                # print()






        return similar_opinions

if __name__ == "__main__":
    cosine_sim = 0.5

    extracted_opinions={'visited,  I': [1], 'Grill,  Union': [1, 7, 12, 13, 19], 'co-worker,  old': [1], 'meal,  wonderful': [1], 'had,  We': [1], 'salad,  California': [1], 'huge,  which': [1], 'came,  It': [1], 'stick,  little': [1], 'stick,  bread': [1], 'delicious,  which': [1], 'excellent,  Service': [1, 2], 'place,  This': [1], 'place,  great': [1], 'experience,  upscale': [1], 'experience,  lunch': [1], 'spots,  other': [1], 'Street,  Craig': [1], 'looking,  I': [1], 'restaurant,  Delicious': [2], 'restaurant,  old': [2], 'bar,  school': [2], 'restaurant,  bar': [2], 'woodwork,  ornate': [2], 'tablecloths,  white': [2], 'had,  I': [2, 5, 19], 'roast,  pot': [2, 11], 'potatoes,  red': [2], 'potatoes,  skinned': [2], 'potatoes,  mashed': [2], 'slaw,  cole': [2], 'tender,  meat': [2], 'slaw,  Cole': [2], 'delicious,  slaw': [2], 'picky,  I': [2], 'meant,  We': [3], 'did,  we': [3], 'nice,  atmosphere': [3], 'list,  local': [3], 'list,  draft': [3], 'great,  list': [3], 'taco,  fish': [3, 8, 15], 'world,  taco': [3], 'sandwich,  fish': [3], 'potions,  HUGE': [3], 'shared,  We': [3], 'huge,  menu': [3], 'thing,  that': [3], 'thing,  good': [3], 'regulars,  people': [3], 'return,  We': [3], 'start,  I': [4], 'note,  positive': [4], 'delicious,  meal': [4], 'recommend,  I': [4, 12, 15], 'sandwich,  grilled': [4], 'sandwich,  chicken': [4], 'fries,  waffle': [4, 17], 'amazing,  fries': [4], 'option,  choose': [4], 'option,  toppings': [4], 'something,  option': [4], 'love,  I': [4], 'has,  atmosphere': [4], 'ambiance,  nice': [4], 'seemed,  they': [4], 'selection,  great': [4], 'rude,  server': [4], 'dropped,  she': [4], 'short,  She': [4], 'refills,  drink': [4], 'are,  meals': [4], 'wanted,  We': [4], 'jumped,  she': [4], 'assume,  I': [4], 'said,  she': [4], 'young,  we': [4], 'ordered,  We': [4], 'note,  thing': [4], 'small,  restaurant': [4], 'close,  tables': [4], 'asked,  hostess': [4], 'table,  OWN': [4], 'put,  we': [4], 'ride,  useless': [5], 'ride,  Uber': [5], 'distance,  walking': [5], 'Devonshire,  Turkey': [5, 6, 12], 'one,  it': [5], 'meals,  best': [5], 'fan,  I': [5], 'fan,  huge': [5], 'great,  Service': [5], 'large,  drinks': [5], 'ordered,  Girlfriend': [5], 'sandwiches,  French': [5], 'sandwiches,  dip': [5], 'says,  she': [5], 'restaurant,  nice': [5], 'restaurant,  small': [5], 'atmosphere,  great': [5], 'food,  great': [5], 'rotation,  place': [6], 'rotation,  regular': [6], 'rotation,  lunch': [6], 'food,  Excellent': [6], 'awesome,  Devonshire': [6], 'tenders,  Chicken': [6], 'like,  I': [6], 'deserts,  recent': [6], '$,  1': [6], 'deserts,  mini': [6], 'think,  I': [6], 'deal,  bottle': [6], 'deal,  great': [6], 'selection,  draft': [6], 'selection,  beer': [6], 'good,  selection': [6], 'seem,  mugs': [6], 'pour,  12oz': [6], 'order,  we': [7], 'undercooked,  They': [7], 'bad,  quality': [7], 'care,  They': [7], 'is,  humbleness': [7], 'day,  It': [7], 'day,  bad': [7], 'went,  I': [7], 'food,  Good': [8], 'food,  hearty': [8], 'prices,  decent': [8], 'service,  warm': [8], 'fish,  beer': [8], 'fish,  battered': [8], 'York,  New': [8], 'strip,  York': [8], 'trout,  Rainbow': [8], 'treat,  trout': [8], 'good,  bad': [8], 'service,  Bad': [9], 'ask,  We': [9], 'fingers,  homemade': [10], 'fingers,  chicken': [10], 'good,  Burgers': [10], 'beer,  Good': [10], 'beer,  priced': [10], 'value,  great': [10], 'large,  menu': [11], 'larger,  portions': [11], 'reasonable,  prices': [11], 'excellent,  quality': [11], 'have,  They': [11, 20], 'menu,  entire': [11], 'dedicated,  menu': [11], 'specialities,  Other': [11], 'cakes,  specialities': [11], 'cakes,  roast': [11], 'come,  wait': [11], 'time,  lunch': [11], 'favorites,  restaurant': [12], 'favorites,  top': [12], 'favorites,  local': [12], 'has,  restaurant': [12], 'feeling,  warm': [12], 'offer,  They': [12], 'deal,  which': [12], 'deal,  cheapest': [12], 'deal,  wine': [12], 'find,  you': [12], 'generous,  portions': [12], 'Taco,  UG': [12], 'Taco,  Fish': [12], 'Burger,  UG': [12], 'order,  particular': [12], 'hungry,  you': [12], 'course,  main': [12], 'soup,  French': [12], 'soup,  onion': [12], 'dined,  I': [13], 'Summer,  last': [13], 'night,  girls': [13], 'had,  we': [13], 'time,  wonderful': [13], 'excellent,  food': [13], 'loved,  We': [13], 'dessert,  smores': [13], 'ordered,  we': [13], 'solid,  service': [13], 'group,  larger': [13], 'going,  I': [13], 'Grill,  Best': [14], 'Grill,  Reuben': [14], 'made,  Grill': [14], 'turkey,  roasted': [14], 'atmosphere,  Fun': [14], 'service,  great': [14], 'food,  fresh': [14], 'food,  interesting': [14], 'got,  I': [15, 19], 'good,  which': [15], 'big,  it': [15], 'giving,  I': [15], 'waiter,  slow': [15], 'took,  He': [15], 'time,  long': [15], 'kept,  I': [15], 'contact,  eye': [15], 'thing,  second': [15], 'sure,  thing': [15], 'sure,  I': [15], 'forgot,  he': [15], 'took,  it': [15], 'cold,  food': [15], 'Drew,  waiter': [16], 'group,  Drew': [16], 'group,  large': [16], 'satisfying,  food': [16], 'food,  typical': [16], 'food,  American': [16], 'way,  bad': [16], 'WONDERFUL,  it': [16], 'options,  Vegan': [16], 'are,  options': [16], 'take,  you': [16], 'salad,  Large': [17], 'lot,  salad': [17], 'Salad,  Greek': [17], 'nachos,  Good': [17], 'fries,  great': [17], 'friendly,  waiter': [17], 'be,  We': [17], 'bottles,  dollar': [18], 'heard,  you': [18], 'wines,  They': [18], 'wines,  decent': [18], 'Pinot,  Sea': [18], 'Pinot,  Glass': [18], 'Noir,  Pinot': [18], 'favorite,  Noir': [18], 'food,  Fast': [18], 'ingredients,  quality': [18], 'get,  I': [18], 'Strip,  NY': [18], 'salad,  Strip': [18], 'salad,  steak': [18], 'gotten,  I': [18], 'allergy,  food': [18], 'contamination,  allergy': [18], 'contamination,  cross': [18], 'list,  eat': [19], 'restaurants,  busy': [19], 'hopes,  high': [19], 'disappointed,  I': [19], 'suspect,  I': [19], 'ordered,  I': [19], 'OK,  food': [19], 'good,  service': [20], 'pleasant,  ambience': [20], 'see,  I': [20], 'Pittsburghers,  older': [20], 'airing,  that': [20], 'looks,  It': [20], 'is,  it': [20]}
    step_2_find_similar_opinion = FindSimilarOpinions(cosine_sim, extracted_opinions)
    opinions = ["food, delicious"]
    for query_opinion in opinions:
        print("\nquery opinion [" + query_opinion + "] has similar opinions: ")
        similar_opinions = step_2_find_similar_opinion.findSimilarOpinions(query_opinion)

        # print similar result
        for tmp_opinion in similar_opinions:
            review_ids = similar_opinions[tmp_opinion]
            print("\n\t[" + tmp_opinion + "] appears in review " + "\t" + " ".join(str(review_ids)))
    print("\n--------------------------------------------------------------")

