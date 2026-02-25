import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage
    
config = {'configurable': {'thread_id': 'thread1'}}

# session state to store the message history
## session state advantage is  that when we press enter so the history in this will not get erase
## it gets erase only when you manually refresh the page or close the tab.
# without this.. every time we press enter the message history will get erased and only the latest message will be there because the whole script will rerun and the message history variable will get reinitialized to empty list.
if "message_history" not in st.session_state:
    st.session_state["message_history"] = []
    


# loading the conversation history
for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):
        st.text(message["content"])
    
user_input = st.chat_input('Type your message here...')

if user_input:
    
    # first add the message to message history
    st.session_state["message_history"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.text(user_input)
        
            
    # first add the message to message history 
    
    # with st.chat_message("assistant"):
    #     ai_message = st.write_stream(
    #         message_chunk.content 
    #         for message_chunk, metadata in chatbot.stream(
    #             {'messages': [HumanMessage(content=user_input)]},
    #             config={'configurable': {'thread_id': 'thread1'}},
    #             stream_mode='messages'
    #         )
            
    #     )
    # st.session_state["message_history"].append({"role": "assistant", "content": ai_message})   
    
    def generate_response():
        for message_chunk, metadata in chatbot.stream(
            {"messages": [HumanMessage(content=user_input)]},
            config=config,
            stream_mode="messages",
        ):
            if message_chunk.content:
                yield message_chunk.content

    with st.chat_message("assistant"):
        ai_message = st.write_stream(generate_response())
 