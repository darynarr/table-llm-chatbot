from dotenv import load_dotenv
import chainlit as cl
import atexit

from src import Database, SQLAgent

load_dotenv()
database = Database()
agent = SQLAgent(database.get_sql_database())


@cl.on_chat_start
async def start():
    files = None

    # Wait for the user to upload a file
    while files == None:
        files = await cl.AskFileMessage(
            content="Please upload a CSV, Excel, or Parquet file to begin!",
            accept={
                "text/csv": [".csv"],
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": [".xlsx"],
                "application/vnd.ms-excel": [".xls"],
                "application/octet-stream": [".parquet"]
            },
            max_size_mb=500,  
            max_files=10
        ).send()

        for file in files:
            msg = cl.Message(content=f"Processing `{file.name}`...")
            await msg.send()
            database.read(file.path)
        
@cl.on_message
async def on_message(message):
    async with cl.Step(name="gpt4", type="llm") as step:
        step.input = message.content

        events = agent.run(message.content)
        for event in events:
            await step.stream_token(event["messages"][-1].content)
            
    response = event["messages"][-1].content
    await cl.Message(
        content=response,
    ).send()
    
@cl.on_stop
async def on_exit():
    database.drop_database()
