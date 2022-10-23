import argparse

from tqdm import tqdm

from utils.expert_nlp import get_emotional_traits, get_sentiment, get_topics
from utils.notion import (
    get_all_entries,
    get_entry_title,
    get_latest_entry,
    update_sentiment,
    update_text,
)


def add_nlp(entry, verbose=False):
    """add nlp information to a single page"""
    if entry is None:
        raise ValueError("entry is None")

    title = get_entry_title(entry)
    sentiment = get_sentiment(title)
    topics = get_topics(title)
    emotional_traits = get_emotional_traits(title)

    if verbose:
        print(f"Title: {title}")
        print(f"Sentiment: {sentiment}")
        print(f"Topics: {topics}")
        print(f"Emotional Traits: {emotional_traits}")

    update_sentiment(entry, sentiment)
    update_text(entry, topics, "topics")
    update_text(entry, emotional_traits, "emotion")


def run_all():
    """run add_nlp on all entries"""
    entries = get_all_entries()

    for entry in tqdm(entries):
        add_nlp(entry)


def run_latest():
    """run add_nlp on the latest entry"""
    entry = get_latest_entry()

    add_nlp(entry)


def main():

    parser = argparse.ArgumentParser("Notion NLP")

    parser.add_argument(
        "--all",
        action="store_true",
        help="Run NLP on all entries",
        required=True,
    )
    parser.add_argument(
        "--latest",
        action="store_true",
        help="Run NLP on the latest entry",
        required=True,
    )

    args = parser.parse_args()

    if args.all:
        run_all()
    elif args.latest:
        run_latest()


if __name__ == "__main__":
    main()
