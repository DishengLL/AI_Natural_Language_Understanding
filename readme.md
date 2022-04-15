# Natural Language Understanding

This assignment focuses on natural language understanding. Assume a user, Lily, wants to decide whether or not to have an important dinner at [Union Grill](https://www.yelp.com/biz/union-grill-pittsburgh) on Craig Street. She wants to know the past consumers’ opinion on the restaurant. For example, does Union Grill provide good service? Does it have delicious food? Does it provide a good price for the food? You want to help her by mining Yelp, which contains 368 reviews about the restaurant. **Opinion** is an aspect of the restaurant in Yelp’s reviewer assessment.

 

You decide to design and develop a reviewer opinion extraction and querying system for this task: 

1. the system automatically extracts opinions from all the reviews; 
2.  the user inputs an opinion as a query, and your system compares the input opinion with the extracted opinions and returns similar opinions 
3. a set of reviews are returned as supporting evidence for this opinion.

 

Dataset: You are provided with 20 reviews randomly selected from Yelp of Union Grill. We do know you will face a large amount of data in a real scenario, but manually annotation is expensive, so we only provide 20 reviews in this assignment. You can regard it as a validation dataset, i.e., design and tune your system to get best performance on this small corpus. The IDs for these 20 reviews are from 1 to 20.

 

 

## **1: Extract opinions from reviews with CoreNLP tool.**

The extracted opinions from the reviews can be represented as a tuple with two elements: attribute and value. The attribute can be an aspect of the restaurant, i.e., an entity or a few entities of the restaurant. The value is a descriptive word that provides the assessment mentioned in the reviews. For example, three opinions are expressed in reviews 

**“The menu is large, the portions are even larger, and the prices are reasonable.”,** the system should extract three tuples **[menu, large], [portion, large], [price, reasonable],** and menu, portion and price are attributes, large, large and reasonable are values. [Stanford coreNLP](http://corenlp.run/) will provide parsing in the following figure, and maybe you want to extract _nsubj_(large, menu), _nsubj_(larger, portions) and _amod_(prices, reasonable). The examples we provide here are only some forms of opinions.You are strongly encouraged to read the reviews to design your own ways to extract opinions based on the coreNLP Enhanced Dependencies Annotation parsing results.

<img width="850" alt="image" src="https://user-images.githubusercontent.com/39432361/161781695-7ffd0f10-ce6b-479a-9edd-9a01bbb42835.png">


Download CoreNLP tool: [Python](https://www.khalidalnajjar.com/setup-use-stanford-corenlp-server-python/).

Materials (but not limited to) to help you understand and use CoreNLP: 

1. https://interviewbubble.com/stanford-corenlp-tutorial/
2. https://nlp.stanford.edu/software/dependencies_manual.pdf
3. https://en.wikipedia.org/wiki/Brown_Corpus#Part-of-speech_tags_used
4. https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
5. http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.9.8216&rep=rep1&type=pdf

 

 

 

## ** 2: Given query, find the similar extracted opinions.**

User will input an opinion as the query, and your system compares it against the extracted opinions. For example, in your extracted opinions, there are “**excellent service**”, “**nice waiter**”, “**great service**”, and “**good service**”. When Lily inputs “**good service**”, your system should return all these extracted opinions since they are all the evidence supporting  __“good service”__. 

 

The semantic similarity between different words can be obtained by word embedding. You can use [Google pre-trained word embeddings](https://code.google.com/archive/p/word2vec/)] with Skip-gram model, and use __cosine similarity__ to measure the word semantic similarity. **You need to *tune the threshold*** for cosine similarity (***cosine_sim*** *in Assignment4Main*) to determine whether words are similar or not. However, the Google pre-trained word embeddings is too large, 8G after decompression. Therefore, we prepared assign4_word2vec1.bin, which only contains words that appear in our corpus. We provided example word2vec codes in ***FindSimilarOpinions*** for your reference.

 

After finding the similar opinions, you need to return the review IDs. Materials (but not limited to) to help you process and understand the word embedding vectors are:

1. https://deeplearning4j.org/docs/latest/deeplearning4j-nlp-word2vec
2. [https://arxiv.org/pdf/1301.3781.pdf%5D](https://arxiv.org/pdf/1301.3781.pdf])

 

Please note that there is no correct solution to this assignment. You need to understand the task, learn the NLP tools, and try to make your algorithm performance better by tuning the threshold. 

 

Suggested ground-truth for 4 query opinions for your reference:

According to **manually annotation**, we provide ground_truth review_IDs for the four input query opinion:

 

query opinion [**service, good**] has similar opinions: 

[service, excellent] appears in review 1, 2   

[service, great] appears in review 5, 14

[service, warm] appears in review 8 

[service, solid] appears in review 13

[service, good] appears in review 20 

[waiter, kind] appears in review 16

[waiter, friendly] appears in review 17

[waiter, attentive] appears in review 17

 

query opinion [**service, bad**] has similar opinions: 

[server, rude] appears in review 4   

[service, rude] appears in review 7

[service, bad] appears in review 9 

[service, slow] appears in review 19 

[waiter, slow] appears in review 15
 


If you are interested in mining deeper in this area, you may also find:

[bread stick, delicious] appears in review 1

[california salad, delicious] appears in review 1

[meat, flavorful] appears in review 2

[meat, tender] appears in review 2, 18

[potatoes, yum] appears in review 2

[cole slaw, delicious] appears in review 2

[waffle fries, amazing] appears in review 3

[turkey devonshire, awesome] appears in review 6

[fish taco, good] appears in review 15

[nachos, good] appears in review 17

[food quality, excellent] appears in review 11

[waffles fries, great] appears in review 17
