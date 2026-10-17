"""Streamlit interface for the Equity Research News Tool."""
import streamlit as st
from langchain_config import get_news_articles, summarize_with_ai

st.set_page_config(page_title="Equity Research News Tool", page_icon="📰", layout="wide")
st.title("📰 Equity Research News Tool")
st.caption("Search recent English-language news and generate an AI-assisted research summary.")

with st.form("news_search_form"):
    query = st.text_input("Company, ticker, or research topic", placeholder="e.g. Apple, TSLA, Microsoft earnings")
    article_count = st.slider("Number of articles", min_value=5, max_value=50, value=20, step=5)
    submitted = st.form_submit_button("Get News", type="primary")

if submitted:
    if not query.strip():
        st.warning("Please enter a company, ticker, or research topic.")
    else:
        try:
            with st.spinner("Fetching articles from NewsAPI..."):
                articles = get_news_articles(query.strip(), page_size=article_count)
            if not articles:
                st.info("No articles were found. Try a broader query or another company name.")
            else:
                with st.spinner("Generating the AI summary..."):
                    summary = summarize_with_ai(query.strip(), articles)
                st.subheader("Research Summary")
                st.write(summary)
                st.caption(f"Based on {len(articles)} article(s). Check the original sources before making investment decisions.")

                st.subheader("Articles reviewed")
                for index, article in enumerate(articles, start=1):
                    title = article.get("title") or "Untitled article"
                    source = (article.get("source") or {}).get("name") or "Unknown source"
                    published = article.get("publishedAt") or "Publication date unavailable"
                    url = article.get("url")
                    description = article.get("description") or "No description provided."
                    with st.expander(f"{index}. {title}"):
                        st.write(f"**Source:** {source}  |  **Published:** {published}")
                        st.write(description)
                        if url:
                            st.markdown(f"[Read original article]({url})")
        except ValueError as exc:
            st.error(str(exc))
        except Exception as exc:
            st.error("The request failed. Check your API keys, internet connection, and API plan, then try again.")
            st.caption(f"Technical details: {exc}")

st.divider()
st.caption("Educational project. AI summaries may omit context or contain errors; this tool is not investment advice.")
