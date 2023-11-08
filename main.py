import streamlit as st
import boto3
from botocore.config import Config
import json

__session = boto3.session.Session()
bedrock = __session.client("bedrock-runtime")

#Streamlit application
st.title('Abhi\'s GenAI  Assistant')

option = st.selectbox('Select Task?',['Rephrase','Summarize',"Direct"])
col1 , col2 = st.columns(2)

def process_text():
   reframed_sentece = anthropic_model(st.session_state.input,option)
   st.session_state.result = reframed_sentece

with col1:
    text_value = st.text_area("ENTER HERE --> ",height=400 ,key='input')
    st.button("Submit",on_click=process_text)
with col2:
    text_value_2 = st.text_area("Result --> ",height=400,key='result' )
    
def anthropic_model(prompt, task):
    # Define body for the model invocation
    if task=="Rephrase":
        prompt= "Rephrase This :"+prompt
    elif task=="Summarize":
        prompt= "Summarize This :"+prompt
    
    body = json.dumps({
        "prompt": "\n\nHuman:{}\n\nAssistant:".format(prompt),
        "max_tokens_to_sample": 10000,
        "temperature": 0.1,
        "top_p": 0.9,
    })

    modelId = 'anthropic.claude-v2'
    accept = 'application/json'
    contentType = 'application/json'

    response = bedrock.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)
    response_body = json.loads(response.get("body").read())
    completion_response = response_body.get("completion")
    return completion_response
