from langchain_community.utilities.sql_database import SQLDatabase
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain import hub

prompt_template = hub.pull("langchain-ai/sql-agent-system-prompt")
system_message = prompt_template.format(dialect="SQLite", top_k=10)

class SQLAgent:
    def __init__(self, db: SQLDatabase):

        self.model = ChatOpenAI(model="gpt-4o", temperature=0)
        self.toolkit = SQLDatabaseToolkit(db=db, llm=self.model)

        self.memory = MemorySaver()
        self.graph = create_react_agent(
            self.model, 
            tools=self.toolkit.get_tools(), 
            checkpointer=self.memory,
            state_modifier=system_message
        )
        self.config = {"configurable": {"thread_id": "1"}}

    
    async def stream(self, user_input: str):
        inputs = dict(
            input={"messages": [("user", user_input)]},
            stream_mode="updates",
            config=self.config
        )
        async for output in self.graph.astream(**inputs):
            for key, value in output.items():
                yield value["messages"][-1]
