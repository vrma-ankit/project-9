"""News retrieval and LLM summarization for the Equity Research News Tool."""
import os
from typing import Any

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from newsapi import NewsApiClient

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY", "").strip()


def get_news_articles(query: str, page_size: int = 20) -> list[dict[str, Any]]:
    """Fetch relevant English-language articles from NewsAPI."""
    if not NEWSAPI_KEY or NEWSAPI_KEY == "your-newsapi-key":
        raise ValueError("NEWSAPI_KEY is missing. Add your NewsAPI key to the .env file.")
    page_size = max(1, min(int(page_size), 100))
    client = NewsApiClient(api_key=NEWSAPI_KEY)
    response = client.get_everything(
        q=query,
        language="en",
        sort_by="relevancy",
        page_size=page_size,
    )
    if response.get("status") != "ok":
        raise RuntimeError(response.get("message", "NewsAPI returned an error."))
    return response.get("articles", [])


def summarize_with_ai(query: str, articles: list[dict[str, Any]]) -> str:
    """Summarize retrieved article content using an OpenAI chat model."""
    if not OPENAI_API_KEY or OPENAI_API_KEY == "your-openai-api-key":
        raise ValueError("OPENAI_API_KEY is missing. Add your OpenAI API key to the .env file.")
    snippets = []
    for article in articles:
        title = article.get("title") or "Untitled"
        source = (article.get("source") or {}).get("name") or "Unknown source"
        description = article.get("description") or article.get("content") or ""
        published = article.get("publishedAt") or "Unknown date"
        if description:
            snippets.append(f"Title: {title}\nSource: {source}\nPublished: {published}\nDetails: {description}")
    if not snippets:
        return "Articles were found, but they did not contain descriptions to summarize. Please review the source links below."

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You assist an equity research analyst. Summarize only the information provided. Distinguish reported facts from uncertainty, note conflicting reports if apparent, and do not invent figures or make unsupported predictions. This is not investment advice."),
        ("human", "Research query: {query}\n\nNews articles:\n{articles}\n\nWrite a concise, structured summary with key developments, potential business/market implications, and important caveats. Mention when the supplied articles do not support a conclusion."),
    ])
    model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    llm = ChatOpenAI(api_key=OPENAI_API_KEY, model=model_name, temperature=0)
    chain = prompt | llm
    result = chain.invoke({"query": query, "articles": "\n\n---\n\n".join(snippets)})
    return str(result.content)
