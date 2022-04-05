import StringDouble
import ExtractGraph


class ExtractOpinions:
    # Extracted opinions and corresponding review id is saved in extracted_pairs, where KEY is the opinion and VALUE
    # is the set of review_ids where the opinion is extracted from.
    # Opinion should in form of "attribute, assessment", such as "service, good".
    extracted_opinions = {}

    def __init__(self):
        return

    def extract_pairs(self, review_id, review_content):
        # example data, which you will need to remove in your real code. Only for demo.
        self.extracted_opinions = {'service, good': [1, 2, 5], 'service, excellent': [4, 6]}
