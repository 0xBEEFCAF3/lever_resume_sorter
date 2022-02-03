#!/usr/bin/env python3
import sys
import os
import requests
import json
import pprint
import nltk
from requests.auth import HTTPBasicAuth
from difflib import SequenceMatcher
from nltk.corpus import stopwords

# Download nltk packages
nltk.download('stopwords')
nltk.download('punkt')

pretty_print = pprint.PrettyPrinter(indent=4)


LEVER_API_URL = 'https://api.lever.co/v1/'
SIMILARITY_THRESHOLD = 0.7


def get_opportunities_for_posting(posting_id, api_key):
    opportunities = requests.get(
        f'{LEVER_API_URL}/opportunities?posting_id={posting_id}&limit=1000', auth=HTTPBasicAuth(api_key, ''))
    return opportunities.json()


def get_resume(opportunity_id, api_key):
    resumes = requests.get(
        f'{LEVER_API_URL}/opportunities/{opportunity_id}/resumes', auth=HTTPBasicAuth(api_key, ''))
    return resumes.json()


def clean_text(text) -> str:
    ls = nltk.PorterStemmer()

    # Tokenize words
    words = nltk.word_tokenize(text)
    # Convert to lower case
    words = [word.lower() for word in words]
    # Eliminate stop words and stem the word
    words = [ls.stem(word) for word in words if word not in stopwords.words(
        "english") and word.isalnum()]

    return words


def get_resume_ranking(parsed_resume, traits) -> int:
    ranking = 0
    for position in parsed_resume['positions']:
        summary = clean_text(position['summary'])
        for trait, value in traits.items():
            for word in summary:
                ratio = SequenceMatcher(
                    None, trait.lower(), word).ratio()
                if (ratio > SIMILARITY_THRESHOLD):
                    ranking += value

    return ranking


def main():

    if ('LEVER_API_KEY' not in os.environ):
        raise Exception('Missing environ LEVER_API_KEY')

    api_key = os.environ['LEVER_API_KEY']

    posting_id = sys.argv[1]
    print(f'Sorting resumes for posting id {posting_id}')

    traits_path = sys.argv[2]
    traits = {}
    print(f'Sorting by traits found in {traits_path}')
    with open(traits_path, 'r') as f:
        traits = json.load(f)

    opportunities = get_opportunities_for_posting(posting_id, api_key)
    print(f'Going thru {len(opportunities["data"])} opportunities')

    rankings = []  # Tuple of candidate email and score
    for _, opportunity in enumerate(opportunities['data']):
        if (opportunity['stage'] != 'applicant-new'):
            continue
        email = opportunity['emails'][0]
        # Only considering the first resume on file
        resume = get_resume(opportunity['id'], api_key)

        if (len(resume['data']) == 0):
            continue

        ranking = get_resume_ranking(resume['data'][0]['parsedData'], traits)
        rankings.append((email, ranking))

    pretty_print.pprint(sorted(rankings, key=lambda rank: rank[1]))


if __name__ == "__main__":
    main()
