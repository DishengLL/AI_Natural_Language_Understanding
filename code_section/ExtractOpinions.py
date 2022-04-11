# import StringDouble
# import ExtractGraph
import stanford_parse as NLP
import re
import nltk



# return a dict {review_pair: docID}
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

    def extract_pairs(self, review_id, review_contents):
        sNLP = NLP.StanfordNLP()

        # devide whole paragraph into sentences
        review_contents  = nltk.tokenize.sent_tokenize(review_contents )
        # print(review_contents)
        l = ['nsubj', 'amod']

        for review_content in review_contents:
            # text =self.preprocessing(review_content)
            # text = text.replace('/',' / ')
            # # print(text)
            text = review_content

            a = sNLP.dependency_parse(text)
            # print(a)
            if a:
                # text = re.sub('([.,!?()])', r' \1 ', text)
                # text = re.sub('\s{2,}', ' ', text)
                # text = text.split(' ')[:-1]
                # print(text)
                text = sNLP.word_tokenize(text)
                # print(text)
                for i, j, k in a:
                    if i == 'ROOT':
                        continue
                        print('>>>>', text[k - 1], i)

                    if i in l:
                        # print(j,k)
                        # print('\t>>>>', text[j - 1], text[k - 1], '-->', i)
                        review_content = text[j - 1]+',  '+text[k - 1]

                        tem = self.extracted_opinions.get(review_content,0)
                        if tem ==0:
                            self.extracted_opinions[review_content] = [review_id]
                        else:
                            if review_id in tem:
                                continue
                            else:
                                self.extracted_opinions[review_content].append(review_id)




if __name__ == "__main__":
    step_1_extract_opinion = ExtractOpinions()
    review_id=1
    f = open('data//assign4_reviews.txt', 'r')

    c="Delicious old school bar/restaurant. Love the ornate woodwork and white tablecloths. Service was absolutely excellent. I had the pot roast with the red skinned mashed potatoes and cole slaw. The meat was so tender and flavorful, and the potatoes...yum! The Cole slaw was delicious too, and I'm VERY picky about Cole slaw."
    step_1_extract_opinion.extract_pairs(review_id, c)

