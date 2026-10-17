Equity Research News Tool
A small Streamlit application that retrieves English-language news articles with NewsAPI and uses an OpenAI language model through LangChain to produce a concise research summary.
Features
Search by company name, ticker, or topic.
Choose how many articles to retrieve (5–50).
Generate a structured AI summary of retrieved article descriptions.
Inspect article source, publication time, description, and original link.
Friendly validation for missing API keys and basic error handling.
Requirements
Python 3.10 or newer
An OpenAI API key with API access/billing enabled as required
A NewsAPI key; the account's plan determines available articles and request limits
Setup on Windows
Download/extract the project folder and open it in VS Code or a terminal.
Create a virtual environment:
```powershell
   python -m venv .venv
   .venv\\Scripts\\Activate.ps1
   ```
If PowerShell blocks activation, use Command Prompt and run `.venv\\Scripts\\activate.bat` instead.
Install packages:
```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
Copy `.env.example` to a new file named `.env` in the same folder. Add your real keys to `.env`:
```text
   OPENAI\_API\_KEY=your-real-openai-key
   NEWSAPI\_KEY=your-real-newsapi-key
   OPENAI\_MODEL=gpt-4o-mini
   ```
Do not share or upload `.env`, and do not commit it to Git.
Start the app:
```powershell
   streamlit run app.py
   ```
Streamlit will show a local URL (usually `http://localhost:8501`). Open it in your browser, search for a company such as `Apple`, and click Get News.
Setup on macOS/Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your real API keys
streamlit run app.py
```
Troubleshooting
API key missing: Check that the file is named exactly `.env`, is in the same folder as `app.py`, and contains the correct variable names.
OpenAI authentication/billing error: Verify the key in the OpenAI API dashboard and confirm API usage is enabled. A ChatGPT subscription does not automatically include API credits.
NewsAPI error or no results: Verify the key, query, account plan, and NewsAPI request limits. Some plans limit historical access or development use.
Package/import error: Activate the virtual environment and run `pip install -r requirements.txt` again.
Port already in use: Run `streamlit run app.py --server.port 8502`.
Project structure
```text
news-research-tool/
├── app.py
├── langchain\_config.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```
Limitations and responsible use
Article availability depends on NewsAPI access and its plan restrictions.
The model summarizes the article text returned by the API; it does not independently verify every claim.
Summaries may omit context or contain mistakes. Open the original articles and verify key facts before relying on them.
This educational project is not investment advice.
Optional future enhancements
Save and export query history.
Add sentiment analysis and charts.
Add user authentication.
Deploy the app to a suitable hosting platform after configuring secrets securely.
