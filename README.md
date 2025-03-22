# Table LLM Chatbot
An AI-powered chatbot that interfaces with SQL databases to answer questions about your data. Simply upload your files (.csv, .xlsx, .xls, .parquet), and the agent will help you analyze and understand your datasets through natural language queries.

## Quick Start

### Using Docker
```
docker build -t table_llm_chatbot .
docker run -d -p 8001:8001 table_llm_chatbot
```

### Using Python Environment
Choose one of these methods to set up your environment:

1. Using venv:
```
python3.12 -m venv .venv
source .venv/bin/activate
```

2. Using Conda:
```
conda create my_env python=3.12
conda activate my_env
```

Then install dependencies:
```
pip install -r requirements.txt
```

Launch the application:
```
chainlit run app.py -w
```

### Access the Application
Once running, access the chatbot interface at: http://localhost:8001