# this readme file explains the main idea of coding section.

## ExtractOpinions.py 
extract opinion pairs ---- like ``service, good ``.  
store all of review pairs into a `dict` --- {``service, good ``: [`reviewID_1`, `reviewID_2`, ... ]}

## FindSimilarOpinions.py
use `cosin similiarity` to measure the similarity between input query opinion and the extracted review pairs from corpus.   
if the similarity value is greater than the predefined threshold, then the corresponding reivews is relavent with the input one.

**instance:**  
input query:  
`["service, good", "service, bad", "atmosphere, good", "food, delicious"]`

**stragety:**   
there are two portions in each query----`<NN, adj>`   
for word2vec embedding, it can only catch the corrresponding embedding of single word.   
So,   
I design two collections for similar token.  
1. nn_similar--- contains all of tokens which are similar with the `nn` in query
2. adj_similar--- contains all of token which are similar with the ``adj`` in the query

finally, use the intersection of these two collection to detemine the final relavent review in the corpus.
## stanford_parse.py
a demo file about the usage of stanford NLP parse tool

## word2vec.py
word2vec usage demo