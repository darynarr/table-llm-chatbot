# table-llm-chatbot
 The agent interacts with an SQL database created from uploaded files (.csv, .xlsx, .xls, .parquet) to answer users questions on the data.


### Create and activate the environment
```
python3.12 -m venv .venv
source .venv/bin/activate
```
or
```
conda create my_env python=3.12
conda activate my_env
```
and
```
pip install -r requirements.txt
```

### Run
```
chainlit run app.py -w
```