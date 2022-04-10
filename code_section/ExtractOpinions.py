# import StringDouble
# import ExtractGraph
import stanford_parse as NLP
import re


class ExtractOpinions:
    # Extracted opinions and corresponding review id is saved in extracted_pairs, where KEY is the opinion and VALUE
    # is the set of review_ids where the opinion is extracted from.
    # Opinion should in form of "attribute, assessment", such as "service, good".
    extracted_opinions = {}

    def __init__(self):

        return

    # preprocessing text before parsing
    def preprocessing(self,review_content):
        plain_text = review_content
        plain_text = plain_text.strip()
        plain_text = plain_text.replace('  ',' ')
        ## try whether or not strip punctuation.
        #plain_text = re.sub(r'[^\w\s]', '', plain_text)
        # plain_text = plain_text.lower()

        return plain_text

    def extract_pairs(self, review_id, review_content):
        sNLP = NLP.StanfordNLP()

        text =self.preprocessing(review_content)
        # print(text)

        a = sNLP.dependency_parse(text)
        print(a)

        text = re.sub('([.,!?()])', r' \1 ', text)
        text = re.sub('\s{2,}', ' ', text)
        text = text.split(' ')[:-1]
        print(text)
        for i, j, k in a:
            if i == 'ROOT':
                continue
                print('>>>>', text[k - 1], i)
            l = ['nsubj', 'amod']
            if i in l:
                print(j,k)
                print('\t>>>>', text[j - 1], text[k - 1], '-->', i)
                review_content = text[j - 1]+',  '+text[k - 1]
                # print(j-1,k-1)
                # print(review_content, i)
            # print(text[j - 1], text[k - 1], '-->', i)
        # example data, which you will need to remove in your real code. Only for demo.
                tem = self.extracted_opinions.get(review_content,0)
                if tem ==0:
                    self.extracted_opinions[review_content] = [review_id]
                else:
                    if review_id in tem:
                        continue
                    else:
                        self.extracted_opinions[review_content].append(review_id)


        # self.extracted_opinions = {'service, good': [1, 2, 5], 'service, excellent': [4, 6]}

step_1_extract_opinion = ExtractOpinions()
review_id=1
f = open('data//assign4_reviews.txt', 'r')

c='The menu is large, the portions are even larger, and the prices are reasonable.'
step_1_extract_opinion.extract_pairs(review_id, c)



# for line in open('data//assign4_reviews.txt'):
#     review_content = f.readline()
#     step_1_extract_opinion.extract_pairs(review_id, review_content)
#     review_id = review_id + 1
# f.close()
#
# extracted_opinions = step_1_extract_opinion.extracted_opinions
# for tmp_opinion in extracted_opinions:
#     review_ids = extracted_opinions[tmp_opinion]
#     print("\n[" + tmp_opinion + "] appears in review " + "\t" + " ".join(str(review_ids)))
# print("\n--------------------------------------------------------------")
#
