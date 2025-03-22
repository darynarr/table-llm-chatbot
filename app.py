from dotenv import load_dotenv
import chainlit as cl

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
            max_size_mb=2000,  
            max_files=10
        ).send()

        msg = cl.Message(content=f"Processing {len(files)} files...\n")
        for file in files:
            await msg.stream_token(f"Loading `{file.name}`...\n")
            await cl.make_async(database.read)(file.path, file.name)
        await msg.stream_token(f"Completed. Ask me questions!\n")
        await msg.update()
        
@cl.on_message
async def on_message(message): 
    async with cl.Step(name="agent", language='sql') as agent_step:        
        async for response in agent.stream(message.content):
            await agent_step.stream_token(response.pretty_repr() + '\n')
            
    await agent_step.update()
    await cl.Message(content=response.content).send()

    
@cl.on_stop
async def on_exit():
    database.drop_database()
