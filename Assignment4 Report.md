# Assignment4 Report 

Disheng Liu | dil36@pitt.edu | 4/11/2022



```python
Tool: pycharm

Language: python

Package: re, gensim, nltk
```





## 1. How did you design your opinion extraction module with CoreNLP?

In this assignement, taking advantage of CoreNLP, I extract all of `['nsubj', 'amod','compound']` dependencies between words.

This stratety can catch most of pairs in this corpus I want. But in some  scenarios, like in this sentence:

"*Today we order pierogies. They were undercooked and tasteless. The dishes were not cooked properly and quality of food is really bad. Even the **service** is really and very **rude**. They have do not care attitude and there is no humbleness. It was my bad day I went to Union Grill.*"

this strategy can not catch pair `(service, rude)`.



In another case, the user uses a pronoun before some adjectives to refer to the previous noun, as in comment 15.  

"*I got the fish taco **which** was pretty **good** but I would recommend splitting with another person since it's so big.*"

In this case, this strategy can catch `(which,good)`, but unable to know user uses `which` to refer to `fish taco`. Actually, the essential pair should be `(fish taco,good)` rather than `(which,good)`





## 2. How did you measure the opinion similarity? How do you tune the threshold?

In this practice, use `cosine similiarity` to measure the similarity between input query opinions and the extracted review pairs from corpus.
When similarity value is greater than the predefined threshold, then the corresponding reivews is relavent with the input one.



### 2.1 **Measure stragety:**
There are two portions in each query----`<NN, adj>`
For **word2vec** embedding, it can only catch the corrresponding embedding of single word.
Therefore, I measure the similiarity in `token` level (rather than pair level).

in this case, not only need to find the relevant document,but also need to extract the opinion pair.

Furthermore, after I extract all of pair from corpus. In these pairs, there is no gaurantee that `noun` will appear before or after `adjective`, so it is risky to directly assign the first token in query to match the first token in extracted pair. 

My strategy is to try all of combination tokens in query and extracted pair, and use one assignment which generates the largest cosine similarity.

For exaple:

For  Query---`<food, delicious>`

​		extracted pair --- `<meal,  wonderful>`

Calculate similarity:

`similarity<food,meal>= 0.5433713`

`similarity<food,wonderful>=0.09148949`

`0.5433713`>`0.09148949`, so assigning `food ` to match `meal`.

so `delicious` should be matched with `wonderful`



Therefore, for `<food, delicious>` and `<meal,  wonderful>`

I get similarity:

`similarity<food,meal>`= 0.5433713

`similarity<delicious,wonderful>`= 0.50828356



Since there are two portions in each query and extracted pairs, the final similarity measurement should consider both of them.

I define my fianl similarity measurement as below
$$
\begin{equation}
\label{eq6}
similarity_{overall}= Portion_1 + Portion_2\\
\left\{
\begin{aligned}
Portion_{1/2} = similarity_{portion_{1/2}} & , & {similarity_{portion_{1/2}}}\leq 0.8 \\
Portion_{1/2} = 0.8 & , & similarity_{portion_{1/2}}> 0.8
\end{aligned}
\right.
\end{equation}
$$
in this formula, I set a upper bound for the similarity in each portion, when the similarity is greater than 0.8, I will limit it to just be `0.8`. (I did a few tests and `0.8` got a good performance)

These designs can reduce the impact of the portion when it gets a large similarity (let's say similarity = 1) and then dominates the final overall similarity.

overall, my measure is a linear combination of cosine similarities of among differernt portions.

set the `threshold = 0.5`(cosine_sim = 0.5), when 
$$
similarity_{overall}\geq NumOfPortion\times threshold = 2\times threshold
$$
then I assign this pair to be relevant with the qurey pair.



### 2.2  **Tuning threshold**:

 for the value of threshold, I try several value,  `threshold  = [0.2, 0.3, 0.4,0.5,0.6,0.7,0.8] `.

When the value of threshold is small, cosine_sim = 0.2, then the precision of extracted relevant pair is low, while the the recall is high

When the value of threshold is high, cosine_sim = 0.8, then less pairs will be returned. In this case, recall becomes lower than the case using small threshold,  while precision of the extracted result is higher than the case using small thresold.



Finally, I use `threshold = 0.5`(cosine_sim = 0.5), which generates a more balanced outcomes between precision and recall 





## 3.  Discuss the successful cases that your system can handle.

for `<food, delicious>` query, 

My algorithm works quite well

````python
[meal,  wonderful] appears in review 	[ 1 ]

[delicious,  meal] appears in review 	[ 4 ]

[food,  great] appears in review 	[ 5 ]

[food,  Excellent] appears in review 	[ 6 ]

[food,  Good] appears in review 	[ 8 ]

[food,  hearty] appears in review 	[ 8 ]

[excellent,  food] appears in review 	[ 1 3 ]

[food,  fresh] appears in review 	[ 1 4 ]

[food,  interesting] appears in review 	[ 1 4 ]

[satisfying,  food] appears in review 	[ 1 6 ]
````

In this case, my `FindSimilarOpinion` find all of pairs which are extractd by `ExtractOpinion`

in this case, comparing with the ground truth,

the Precision of this outcome  is 1, the Recall of this result is $\frac{7}{8}$





## 4 Discuss the cases that your system fail. For example, you may find the review shows an opinion similar to the input opinion, but your algorithm fail to extract. Or you may have a similar opinion, but cannot be matched to the input opinion through your current algorithm.

The shortages of my algorithm come from two part

1. in `ExtractOpinion` section, my algorithm can not extract all of pairs in the corpus

   1. For example, like in this sentence:

      "*Today we order pierogies. They were undercooked and tasteless. The dishes were not cooked properly and quality of food is really bad. Even the **service** is really and very **rude**. They have do not care attitude and there is no humbleness. It was my bad day I went to Union Grill.*"

      my algorithm can not catch pair `(service, rude)`.

   2. In another case, the user uses a pronoun before some adjectives to refer to the previous noun, as in comment 15.  

      "*I got the fish taco **which** was pretty **good** but I would recommend splitting with another person since it's so big.*"

      In this case, this strategy can catch `(which,good)`, but unable to know user uses `which` to refer to `fish taco`. Actually, the essential pair should be `(fish taco,good)` rather than `(which,good)`

   

2. in `FindSimilarOpinion` seciton, word2vec embedding can not catch all of similar tokens 

   1. based on word2vec embedding, my algorithm can not catch the similarity between `waiter` and `service`. 

       the cosine similarity between `waiter` and `service`  is only 0.13051517, and the cosine similarity between `attentive` and `good`  is only 0.19479631,

      after combining this two portion, the final overall similarity is only 0.325, less than the threshold, so finally this pair become a false negative case in my algorithm 

   2. another shortage comes from the weakness of word2vec embedding which is not so powerful to differentiate `antonym`.  For example, the cosine similarity between `good` and `bad` is relative large (`0.719`), so when I try to extract reviews about `bad service`, the algorithm may return some reviews containing `good service`

      

      (p.s.: Cosine_Similarity <service, service> = 1, Cosine_Similarity <bad, good> = 0.71, the the overall similarity will be 0.8+0.7=1.5>1)

      

   





## 5. The output of your algorithm with your best results (threshold).

**output**

/opt/anaconda3/bin/python "/Users/liu/Desktop/Pitts/MSIS/2022srping/2224 INFSCI 2440 SEC1010 ARTIFICIAL INTELLIGENCE/assignment/4--Natural Language Understanding/code_section/Assignment4Main.py"

[visited,  I] appears in review 	[ 1 ]

[Grill,  Union] appears in review 	[ 1 ,   7 ,   1 2 ,   1 3 ,   1 9 ]

[co-worker,  old] appears in review 	[ 1 ]

[meal,  wonderful] appears in review 	[ 1 ]

[had,  We] appears in review 	[ 1 ]

[salad,  California] appears in review 	[ 1 ]

[huge,  which] appears in review 	[ 1 ]

[came,  It] appears in review 	[ 1 ]

[stick,  little] appears in review 	[ 1 ]

[stick,  bread] appears in review 	[ 1 ]

[delicious,  which] appears in review 	[ 1 ]

[excellent,  Service] appears in review 	[ 1 ,   2 ]

[place,  This] appears in review 	[ 1 ]

[place,  great] appears in review 	[ 1 ]

[experience,  upscale] appears in review 	[ 1 ]

[experience,  lunch] appears in review 	[ 1 ]

[spots,  other] appears in review 	[ 1 ]

[Street,  Craig] appears in review 	[ 1 ]

[looking,  I] appears in review 	[ 1 ]

[restaurant,  Delicious] appears in review 	[ 2 ]

[restaurant,  old] appears in review 	[ 2 ]

[bar,  school] appears in review 	[ 2 ]

[restaurant,  bar] appears in review 	[ 2 ]

[woodwork,  ornate] appears in review 	[ 2 ]

[tablecloths,  white] appears in review 	[ 2 ]

[had,  I] appears in review 	[ 2 ,   5 ,   1 9 ]

[roast,  pot] appears in review 	[ 2 ,   1 1 ]

[potatoes,  red] appears in review 	[ 2 ]

[potatoes,  skinned] appears in review 	[ 2 ]

[potatoes,  mashed] appears in review 	[ 2 ]

[slaw,  cole] appears in review 	[ 2 ]

[tender,  meat] appears in review 	[ 2 ]

[slaw,  Cole] appears in review 	[ 2 ]

[delicious,  slaw] appears in review 	[ 2 ]

[picky,  I] appears in review 	[ 2 ]

[meant,  We] appears in review 	[ 3 ]

[did,  we] appears in review 	[ 3 ]

[nice,  atmosphere] appears in review 	[ 3 ]

[list,  local] appears in review 	[ 3 ]

[list,  draft] appears in review 	[ 3 ]

[great,  list] appears in review 	[ 3 ]

[taco,  fish] appears in review 	[ 3 ,   8 ,   1 5 ]

[world,  taco] appears in review 	[ 3 ]

[sandwich,  fish] appears in review 	[ 3 ]

[potions,  HUGE] appears in review 	[ 3 ]

[shared,  We] appears in review 	[ 3 ]

[huge,  menu] appears in review 	[ 3 ]

[thing,  that] appears in review 	[ 3 ]

[thing,  good] appears in review 	[ 3 ]

[regulars,  people] appears in review 	[ 3 ]

[return,  We] appears in review 	[ 3 ]

[start,  I] appears in review 	[ 4 ]

[note,  positive] appears in review 	[ 4 ]

[delicious,  meal] appears in review 	[ 4 ]

[recommend,  I] appears in review 	[ 4 ,   1 2 ,   1 5 ]

[sandwich,  grilled] appears in review 	[ 4 ]

[sandwich,  chicken] appears in review 	[ 4 ]

[fries,  waffle] appears in review 	[ 4 ,   1 7 ]

[amazing,  fries] appears in review 	[ 4 ]

[option,  choose] appears in review 	[ 4 ]

[option,  toppings] appears in review 	[ 4 ]

[something,  option] appears in review 	[ 4 ]

[love,  I] appears in review 	[ 4 ]

[has,  atmosphere] appears in review 	[ 4 ]

[ambiance,  nice] appears in review 	[ 4 ]

[seemed,  they] appears in review 	[ 4 ]

[selection,  great] appears in review 	[ 4 ]

[rude,  server] appears in review 	[ 4 ]

[dropped,  she] appears in review 	[ 4 ]

[short,  She] appears in review 	[ 4 ]

[refills,  drink] appears in review 	[ 4 ]

[are,  meals] appears in review 	[ 4 ]

[wanted,  We] appears in review 	[ 4 ]

[jumped,  she] appears in review 	[ 4 ]

[assume,  I] appears in review 	[ 4 ]

[said,  she] appears in review 	[ 4 ]

[young,  we] appears in review 	[ 4 ]

[ordered,  We] appears in review 	[ 4 ]

[note,  thing] appears in review 	[ 4 ]

[small,  restaurant] appears in review 	[ 4 ]

[close,  tables] appears in review 	[ 4 ]

[asked,  hostess] appears in review 	[ 4 ]

[table,  OWN] appears in review 	[ 4 ]

[put,  we] appears in review 	[ 4 ]

[ride,  useless] appears in review 	[ 5 ]

[ride,  Uber] appears in review 	[ 5 ]

[distance,  walking] appears in review 	[ 5 ]

[Devonshire,  Turkey] appears in review 	[ 5 ,   6 ,   1 2 ]

[one,  it] appears in review 	[ 5 ]

[meals,  best] appears in review 	[ 5 ]

[fan,  I] appears in review 	[ 5 ]

[fan,  huge] appears in review 	[ 5 ]

[great,  Service] appears in review 	[ 5 ]

[large,  drinks] appears in review 	[ 5 ]

[ordered,  Girlfriend] appears in review 	[ 5 ]

[sandwiches,  French] appears in review 	[ 5 ]

[sandwiches,  dip] appears in review 	[ 5 ]

[says,  she] appears in review 	[ 5 ]

[restaurant,  nice] appears in review 	[ 5 ]

[restaurant,  small] appears in review 	[ 5 ]

[atmosphere,  great] appears in review 	[ 5 ]

[food,  great] appears in review 	[ 5 ]

[rotation,  place] appears in review 	[ 6 ]

[rotation,  regular] appears in review 	[ 6 ]

[rotation,  lunch] appears in review 	[ 6 ]

[food,  Excellent] appears in review 	[ 6 ]

[awesome,  Devonshire] appears in review 	[ 6 ]

[tenders,  Chicken] appears in review 	[ 6 ]

[like,  I] appears in review 	[ 6 ]

[deserts,  recent] appears in review 	[ 6 ]

[$,  1] appears in review 	[ 6 ]

[deserts,  mini] appears in review 	[ 6 ]

[think,  I] appears in review 	[ 6 ]

[deal,  bottle] appears in review 	[ 6 ]

[deal,  great] appears in review 	[ 6 ]

[selection,  draft] appears in review 	[ 6 ]

[selection,  beer] appears in review 	[ 6 ]

[good,  selection] appears in review 	[ 6 ]

[seem,  mugs] appears in review 	[ 6 ]

[pour,  12oz] appears in review 	[ 6 ]

[order,  we] appears in review 	[ 7 ]

[undercooked,  They] appears in review 	[ 7 ]

[bad,  quality] appears in review 	[ 7 ]

[care,  They] appears in review 	[ 7 ]

[is,  humbleness] appears in review 	[ 7 ]

[day,  It] appears in review 	[ 7 ]

[day,  bad] appears in review 	[ 7 ]

[went,  I] appears in review 	[ 7 ]

[food,  Good] appears in review 	[ 8 ]

[food,  hearty] appears in review 	[ 8 ]

[prices,  decent] appears in review 	[ 8 ]

[service,  warm] appears in review 	[ 8 ]

[fish,  beer] appears in review 	[ 8 ]

[fish,  battered] appears in review 	[ 8 ]

[York,  New] appears in review 	[ 8 ]

[strip,  York] appears in review 	[ 8 ]

[trout,  Rainbow] appears in review 	[ 8 ]

[treat,  trout] appears in review 	[ 8 ]

[good,  bad] appears in review 	[ 8 ]

[service,  Bad] appears in review 	[ 9 ]

[ask,  We] appears in review 	[ 9 ]

[fingers,  homemade] appears in review 	[ 1 0 ]

[fingers,  chicken] appears in review 	[ 1 0 ]

[good,  Burgers] appears in review 	[ 1 0 ]

[beer,  Good] appears in review 	[ 1 0 ]

[beer,  priced] appears in review 	[ 1 0 ]

[value,  great] appears in review 	[ 1 0 ]

[large,  menu] appears in review 	[ 1 1 ]

[larger,  portions] appears in review 	[ 1 1 ]

[reasonable,  prices] appears in review 	[ 1 1 ]

[excellent,  quality] appears in review 	[ 1 1 ]

[have,  They] appears in review 	[ 1 1 ,   2 0 ]

[menu,  entire] appears in review 	[ 1 1 ]

[dedicated,  menu] appears in review 	[ 1 1 ]

[specialities,  Other] appears in review 	[ 1 1 ]

[cakes,  specialities] appears in review 	[ 1 1 ]

[cakes,  roast] appears in review 	[ 1 1 ]

[come,  wait] appears in review 	[ 1 1 ]

[time,  lunch] appears in review 	[ 1 1 ]

[favorites,  restaurant] appears in review 	[ 1 2 ]

[favorites,  top] appears in review 	[ 1 2 ]

[favorites,  local] appears in review 	[ 1 2 ]

[has,  restaurant] appears in review 	[ 1 2 ]

[feeling,  warm] appears in review 	[ 1 2 ]

[offer,  They] appears in review 	[ 1 2 ]

[deal,  which] appears in review 	[ 1 2 ]

[deal,  cheapest] appears in review 	[ 1 2 ]

[deal,  wine] appears in review 	[ 1 2 ]

[find,  you] appears in review 	[ 1 2 ]

[generous,  portions] appears in review 	[ 1 2 ]

[Taco,  UG] appears in review 	[ 1 2 ]

[Taco,  Fish] appears in review 	[ 1 2 ]

[Burger,  UG] appears in review 	[ 1 2 ]

[order,  particular] appears in review 	[ 1 2 ]

[hungry,  you] appears in review 	[ 1 2 ]

[course,  main] appears in review 	[ 1 2 ]

[soup,  French] appears in review 	[ 1 2 ]

[soup,  onion] appears in review 	[ 1 2 ]

[dined,  I] appears in review 	[ 1 3 ]

[Summer,  last] appears in review 	[ 1 3 ]

[night,  girls] appears in review 	[ 1 3 ]

[had,  we] appears in review 	[ 1 3 ]

[time,  wonderful] appears in review 	[ 1 3 ]

[excellent,  food] appears in review 	[ 1 3 ]

[loved,  We] appears in review 	[ 1 3 ]

[dessert,  smores] appears in review 	[ 1 3 ]

[ordered,  we] appears in review 	[ 1 3 ]

[solid,  service] appears in review 	[ 1 3 ]

[group,  larger] appears in review 	[ 1 3 ]

[going,  I] appears in review 	[ 1 3 ]

[Grill,  Best] appears in review 	[ 1 4 ]

[Grill,  Reuben] appears in review 	[ 1 4 ]

[made,  Grill] appears in review 	[ 1 4 ]

[turkey,  roasted] appears in review 	[ 1 4 ]

[atmosphere,  Fun] appears in review 	[ 1 4 ]

[service,  great] appears in review 	[ 1 4 ]

[food,  fresh] appears in review 	[ 1 4 ]

[food,  interesting] appears in review 	[ 1 4 ]

[got,  I] appears in review 	[ 1 5 ,   1 9 ]

[good,  which] appears in review 	[ 1 5 ]

[big,  it] appears in review 	[ 1 5 ]

[giving,  I] appears in review 	[ 1 5 ]

[waiter,  slow] appears in review 	[ 1 5 ]

[took,  He] appears in review 	[ 1 5 ]

[time,  long] appears in review 	[ 1 5 ]

[kept,  I] appears in review 	[ 1 5 ]

[contact,  eye] appears in review 	[ 1 5 ]

[thing,  second] appears in review 	[ 1 5 ]

[sure,  thing] appears in review 	[ 1 5 ]

[sure,  I] appears in review 	[ 1 5 ]

[forgot,  he] appears in review 	[ 1 5 ]

[took,  it] appears in review 	[ 1 5 ]

[cold,  food] appears in review 	[ 1 5 ]

[Drew,  waiter] appears in review 	[ 1 6 ]

[group,  Drew] appears in review 	[ 1 6 ]

[group,  large] appears in review 	[ 1 6 ]

[satisfying,  food] appears in review 	[ 1 6 ]

[food,  typical] appears in review 	[ 1 6 ]

[food,  American] appears in review 	[ 1 6 ]

[way,  bad] appears in review 	[ 1 6 ]

[WONDERFUL,  it] appears in review 	[ 1 6 ]

[options,  Vegan] appears in review 	[ 1 6 ]

[are,  options] appears in review 	[ 1 6 ]

[take,  you] appears in review 	[ 1 6 ]

[salad,  Large] appears in review 	[ 1 7 ]

[lot,  salad] appears in review 	[ 1 7 ]

[Salad,  Greek] appears in review 	[ 1 7 ]

[nachos,  Good] appears in review 	[ 1 7 ]

[fries,  great] appears in review 	[ 1 7 ]

[friendly,  waiter] appears in review 	[ 1 7 ]

[be,  We] appears in review 	[ 1 7 ]

[bottles,  dollar] appears in review 	[ 1 8 ]

[heard,  you] appears in review 	[ 1 8 ]

[wines,  They] appears in review 	[ 1 8 ]

[wines,  decent] appears in review 	[ 1 8 ]

[Pinot,  Sea] appears in review 	[ 1 8 ]

[Pinot,  Glass] appears in review 	[ 1 8 ]

[Noir,  Pinot] appears in review 	[ 1 8 ]

[favorite,  Noir] appears in review 	[ 1 8 ]

[food,  Fast] appears in review 	[ 1 8 ]

[ingredients,  quality] appears in review 	[ 1 8 ]

[get,  I] appears in review 	[ 1 8 ]

[Strip,  NY] appears in review 	[ 1 8 ]

[salad,  Strip] appears in review 	[ 1 8 ]

[salad,  steak] appears in review 	[ 1 8 ]

[gotten,  I] appears in review 	[ 1 8 ]

[allergy,  food] appears in review 	[ 1 8 ]

[contamination,  allergy] appears in review 	[ 1 8 ]

[contamination,  cross] appears in review 	[ 1 8 ]

[list,  eat] appears in review 	[ 1 9 ]

[restaurants,  busy] appears in review 	[ 1 9 ]

[hopes,  high] appears in review 	[ 1 9 ]

[disappointed,  I] appears in review 	[ 1 9 ]

[suspect,  I] appears in review 	[ 1 9 ]

[ordered,  I] appears in review 	[ 1 9 ]

[OK,  food] appears in review 	[ 1 9 ]

[good,  service] appears in review 	[ 2 0 ]

[pleasant,  ambience] appears in review 	[ 2 0 ]

[see,  I] appears in review 	[ 2 0 ]

[Pittsburghers,  older] appears in review 	[ 2 0 ]

[airing,  that] appears in review 	[ 2 0 ]

[looks,  It] appears in review 	[ 2 0 ]

[is,  it] appears in review 	[ 2 0 ]

--------------------------------------------------------------

query opinion [service, good] has similar opinions: 

	[excellent,  Service] appears in review 	[ 1 ,   2 ]
	
	[great,  Service] appears in review 	[ 5 ]
	
	[service,  warm] appears in review 	[ 8 ]
	
	[service,  Bad] appears in review 	[ 9 ]
	
	[solid,  service] appears in review 	[ 1 3 ]
	
	[service,  great] appears in review 	[ 1 4 ]
	
	[good,  service] appears in review 	[ 2 0 ]

query opinion [service, bad] has similar opinions: 

	[bad,  quality] appears in review 	[ 7 ]
	
	[service,  warm] appears in review 	[ 8 ]
	
	[service,  Bad] appears in review 	[ 9 ]
	
	[solid,  service] appears in review 	[ 1 3 ]
	
	[service,  great] appears in review 	[ 1 4 ]
	
	[good,  service] appears in review 	[ 2 0 ]

query opinion [atmosphere, good] has similar opinions: 

	[nice,  atmosphere] appears in review 	[ 3 ]
	
	[thing,  good] appears in review 	[ 3 ]
	
	[ambiance,  nice] appears in review 	[ 4 ]
	
	[atmosphere,  great] appears in review 	[ 5 ]
	
	[food,  Good] appears in review 	[ 8 ]
	
	[atmosphere,  Fun] appears in review 	[ 1 4 ]
	
	[pleasant,  ambience] appears in review 	[ 2 0 ]

query opinion [food, delicious] has similar opinions: 

	[meal,  wonderful] appears in review 	[ 1 ]
	
	[delicious,  meal] appears in review 	[ 4 ]
	
	[food,  great] appears in review 	[ 5 ]
	
	[food,  Excellent] appears in review 	[ 6 ]
	
	[food,  Good] appears in review 	[ 8 ]
	
	[food,  hearty] appears in review 	[ 8 ]
	
	[excellent,  food] appears in review 	[ 1 3 ]
	
	[food,  fresh] appears in review 	[ 1 4 ]
	
	[food,  interesting] appears in review 	[ 1 4 ]
	
	[satisfying,  food] appears in review 	[ 1 6 ]

--------------------------------------------------------------

Process finished with exit code 0