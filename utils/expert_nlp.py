from typing import List

from expertai.nlapi.cloud.client import ExpertAiClient

client = ExpertAiClient()


def get_sentiment(text: str) -> int:
    """Returns a sentiment score from -100 to 100.

    Sentiment Analysis from expert.ai
    https://docs.expert.ai/nlapi/latest/guide/sentiment-analysis/

    Args:
        text (str): input text to be analyzed

    Returns:
        int: sentiment score
    """

    output = client.specific_resource_analysis(
        body={"document": {"text": text}},
        params={"language": "en", "resource": "sentiment"},
    )
    return output.sentiment.overall


def get_topics(text: str) -> List[str]:
    """Returns a list of topics from the text using
    expert.ai's Keyphrase extraction

    https://docs.expert.ai/nlapi/latest/guide/keyphrase-extraction/

    list of relevant topics
    https://docs.expert.ai/nlapi/latest/reference/topics/

    Args:
        text (str): input text to be analyzed

    Returns:
        List[str]: A list of topics
    """

    output = client.specific_resource_analysis(
        body={"document": {"text": text}},
        params={"language": "en", "resource": "relevants"},
    )
    topics = [t.label for t in output.topics]
    return topics


def get_emotional_traits(text: str) -> List[str]:
    """Get emotional traits from the text.

    https://docs.expert.ai/nlapi/latest/guide/classification/emotional-traits/

    Args:
        text (str): text to analyze

    Returns:
        List[str]: a list of emotional traits
    """

    output = client.classification(
        body={"document": {"text": text}},
        params={"language": "en", "taxonomy": "emotional-traits"},
    )

    emotional_traits = [category.label for category in output.categories]

    return emotional_traits
