from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain_experimental.tools import PythonAstREPLTool
import pandas as pd

# Reference to https://smith.langchain.com/hub/langchain-ai/python-agent
prompt = """
You are an agent designed to write and execute python code to answer questions on tabular data using pandas.
You have access to a python REPL, which you can use to execute python code.
If you get an error, debug your code and try again.
Only use the output of your code to answer the question. 
You might know the answer without running any code, but you should still run the code to get the answer.
If it does not seem like you can write code to answer the question, just return "I don't know" as the answer.

Here is the list of the dataframes that are loaded to python REPL tool:
{table_names}

DO NOT recreate those tables.
"""

class PythonAgent:
    def __init__(self):
        self.model = ChatOpenAI(model="gpt-4o", temperature=0)

        self.memory = MemorySaver()

        self.config = {"configurable": {"thread_id": "1"}}
        self.graph = None
        
    def setup(self, files: list):
        locals = {}
        for file in files:
            df, table_name = self.read(file.path, file.name)
            locals[table_name] = df
            
        tools = [PythonAstREPLTool(locals=locals)]
        self.graph = create_react_agent(
            self.model, 
            tools=tools, 
            checkpointer=self.memory,
            state_modifier=prompt.format(table_names=', '.join(list(locals.keys())))
        )
        
    def read(self, path: str, name: str):
        if name.endswith('.csv'):
            df = pd.read_csv(path)
        elif name.endswith('.xlsx') or name.endswith('.xls'):
            df = pd.read_excel(path)
        elif name.endswith('.parquet'):
            df = pd.read_parquet(path)
        else:
            raise ValueError("Unsupported file format")
        table_name = name.split('.')[0]
        return df, table_name
    
    async def stream(self, user_input: str):
        inputs = dict(
            input={"messages": [("user", user_input)]},
            stream_mode="updates",
            config=self.config
        )
        async for output in self.graph.astream(**inputs):
            for key, value in output.items():
                yield value["messages"][-1]