from langchain_core.messages import AIMessage, HumanMessage
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

def get_response(user_input, chat_history, llm):
    """Gets a response from the chatbot for a given user input and history."""
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful financial assistant. Answer the user's questions based on your knowledge."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ])
    
    chain = prompt | llm
    
    response = chain.invoke({
        "input": user_input,
        "chat_history": chat_history
    })
    
    return response.content