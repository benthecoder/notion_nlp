import logging
import os
import sys
from datetime import datetime, timedelta
from pprint import pprint
from typing import Dict, List

from dotenv import load_dotenv
from notion_client import APIErrorCode, APIResponseError, Client

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN", "")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID", "")


notion = Client(auth=NOTION_TOKEN)


def get_all_entries() -> List[Dict]:
    """Get all the entries from the database."""

    try:
        results = notion.databases.query(
            **{"database_id": NOTION_DATABASE_ID}
        ).get("results")
    except APIResponseError as error:
        if error.code == APIErrorCode.ObjectNotFound:
            raise ValueError("Database not found.")
        else:
            logging.error(error)

    no_of_results = len(results)

    if no_of_results == 0:
        print("No entries found.")
        sys.exit()

    print(f"Entries pulled: {len(results)}")

    return results


def get_latest_entry() -> Dict:
    """get the latest entry by filtering on or after yesterday and return the first result."""

    # get the the day before today
    ydt = datetime.today() - timedelta(days=1)
    # format the date
    ydt = ydt.strftime("%Y-%m-%d")

    try:
        results = notion.databases.query(
            **{
                "database_id": NOTION_DATABASE_ID,
                "filter": {
                    "property": "date",
                    "date": {"on_or_after": ydt},
                },
            }
        ).get("results")

    except APIResponseError as error:
        if error.code == APIErrorCode.ObjectNotFound:
            raise ValueError("Database not found.")
        else:
            logging.error(error)

    return results[0]


def update_text(result, tag_list, property_name):
    """Add tags as a comma separated string in a text property"""

    # get page id
    page_id = result["id"]

    # get properties
    properties = get_property(page_id)

    # get topic property
    text_prop = properties.get(property_name)

    if text_prop is None:
        raise KeyError(f"{property_name} property not found.")

    # add text to the property
    text_prop["rich_text"] = [{"text": {"content": ""}}]

    text_prop["rich_text"][0]["text"]["content"] = ", ".join(tag_list)

    try:
        notion.pages.update(page_id=page_id, properties=properties)
    except Exception as e:
        print(e)


def update_sentiment(result, sentiment):
    """Add sentiment score to a number property"""

    page_id = result["id"]
    properties = get_property(page_id)

    sentiment_score = properties.get("sentiment_score")

    if sentiment_score is None:
        raise KeyError("sentiment_score property not found.")

    sentiment_score["number"] = sentiment

    try:
        notion.pages.update(page_id=page_id, properties=properties)
    except Exception as e:
        print(e)


def get_entry_title(result) -> str:
    """Get the title of the entry."""

    try:
        title = result["properties"]["text"]["title"][0]["plain_text"]
    except KeyError:
        raise KeyError("error in getting entry title.")

    return title


def get_property(page_id) -> Dict:
    """Get the property from the result."""

    # get the page
    page = notion.pages.retrieve(page_id=page_id)

    # get the properties
    props = page.get("properties")

    return props