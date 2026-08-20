from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser 
import os

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    MessagesPlaceholder(variable_name="history"),  # MessagesPlaceholder --> to insert some msg in prompt
    ("human", "{history}")
])

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    api_key=os.environ['GEMINI_API_KEY'],
    temperature=0
    )

chain = prompt | llm | StrOutputParser()

store = {}

def get_session_history(session_id):
    if session_id not in store:
        store[session_id] = []  #to create the chat with history and store in memory
    return store[session_id]

'''
start

User Input

session_id= session_1

Do you want to continue the session 
yes
no

create new session or exit
'''
session_id=1
print('--------- START ----------')

# 2 scenario for break
# 1- WHEN BREAK Excute
# 2- when there is error except bblock will execute

while True:  # run until break keyword get execute
    user_input=input(
                '''
                Enter your query ... 
                or
                For exit type => exit
                Query: =>
                    ''').lower()
    
    if user_input=='exit':
        print('Thank You 😊✌️')
        break

    try: 
        history=get_session_history(session_id)   # it will store list
        history.append({'user_query':user_input})
        response= chain.invoke({'history':history})
        print(f'''
                User input => {user_input}
                Response => {response}
            ''')

    except Exception as e:  # e --> will store the error msg
        print(f"Error => {e} ")
        break 

    new_session=input(
        ''' 
        If you want to continue with the same session type => Type anything except 'no'
        For new session type => No
        ''').lower()

    if new_session=='no':
        session_id+=1

    