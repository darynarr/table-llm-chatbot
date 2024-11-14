from dotenv import load_dotenv
import streamlit as st
import atexit

from src import Database, SQLAgent

def main():
    load_dotenv()

    st.set_page_config(page_title="Ask your table")
    st.header("Ask your table 📈")
    database = Database()
    
    # Register the drop_database function to be called on exit
    atexit.register(database.drop_database)

    uploaded_files = st.file_uploader(
        "Upload files", 
        type=["csv", "xlsx", "xls", "parquet"], 
        accept_multiple_files=True)

    if len(uploaded_files):
        for uploaded_file in uploaded_files:
            database.read(uploaded_file)
            
        agent = SQLAgent(database.get_sql_database())
        if 'messages' not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if user_question := st.chat_input("Ask a question about your table: "):
            st.session_state.messages.append({"role": "user", "content": user_question})
            with st.chat_message("user"):
                st.markdown(user_question)

            with st.spinner(text="In progress..."):
                response = agent.run(user_question)
                st.session_state.messages.append({"role": "assistant", "content": response})
                with st.chat_message("assistant"):
                    st.markdown(response)

if __name__ == "__main__":
    main()