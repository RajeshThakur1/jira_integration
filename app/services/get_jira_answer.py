# from jira import JIRA
# import pymongo
# import json
# import openai
# import app.config as cfg
# # Warning control
# import warnings
# warnings.filterwarnings('ignore')
# import os
# from utils import get_openai_api_key, get_serper_api_key
# from crewai import Agent, Task, Crew
# openai_api_key = get_openai_api_key()
# os.environ["OPENAI_MODEL_NAME"] = "gpt-4o" #'gpt-3.5-turbo'
# os.environ["SERPER_API_KEY"] = get_serper_api_key()
# os.environ['OPENAI_API_KEY'] = cfg.OPENAI_API_KEY
#
#
#
#
# os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")
# from crewai_tools import ScrapeWebsiteTool, SerperDevTool, DirectoryReadTool, FileReadTool
# search_tool = SerperDevTool()
# scrape_tool = ScrapeWebsiteTool()
# from crewai_tools import BaseTool
# import json
# from bson import ObjectId
# from langchain_community.document_loaders.mongodb import MongodbLoader
# # from langchain.chat_models import ChatOpenAI
# # from langchain.agents import create_json_agent
# from langchain.agents.agent_toolkits import JsonToolkit
# from langchain.tools.json.tool import  JsonSpec
# import json
#
#
# class ProjectManagementTool(BaseTool):
#     name: str = "Project Management Tool Analysis"
#     description: str = ("Analyzes the questation of given text "
#                         "fetch the data from the Mongo DB and and try to answer the given questation based of the Mongo DB result and strictly do not add any new things by own")
#
#     def get_data(self):
#         loader = MongodbLoader(
#             connection_string=cfg.mongo_url,
#             db_name=cfg.mongo_db_name,
#             collection_name=cfg.mongo_collection_name,
#         )
#         docs = loader.load()
#         json_data_list = {"dummy": []}
#
#         # Assume 'docs' is a list of objects that contain the 'page_content' attribute
#         for doc in docs:
#             data = doc.page_content.replace("'", '"')
#             # Convert ObjectId to string and None to null
#             data = data.replace('ObjectId(', '').replace(')', '').replace('None', 'null')
#
#             # Convert the string to a JSON object
#             try:
#                 data_json = json.loads(data)
#                 json_data_list['dummy'].append(data_json)  # Append the dictionary to the list
#             except json.JSONDecodeError as e:
#                 print(f"An error occurred: {e}")
#
#         # Write the list of JSON objects to a file
#         # with open('output3.json', 'w', encoding='utf-8') as f:
#         #     json.dump(json_data_list, f, ensure_ascii=False, indent=4)
#         return json_data_list
#
#     def _run(self, text: str) -> str:
#         data = self.get_data()
#         # json_data_list = self.get_data()
#         # spec=JsonSpec(dict_=json_data_list,max_value_length=4000)
#         # json_tool=JsonToolkit(spec=spec)
#         return data
#
#
# def get_data():
#     loader = MongodbLoader(
#         connection_string=cfg.mongo_url,
#         db_name=cfg.mongo_db_name,
#         collection_name=cfg.mongo_collection_name,
#     )
#     docs = loader.load()
#     json_data_list = {"dummy": []}
#
#     # Assume 'docs' is a list of objects that contain the 'page_content' attribute
#     for doc in docs:
#         data = doc.page_content.replace("'", '"')
#         # Convert ObjectId to string and None to null
#         data = data.replace('ObjectId(', '').replace(')', '').replace('None', 'null')
#
#         # Convert the string to a JSON object
#         try:
#             data_json = json.loads(data)
#             json_data_list['dummy'].append(data_json)  # Append the dictionary to the list
#         except json.JSONDecodeError as e:
#             print(f"An error occurred: {e}")
#
#     # Write the list of JSON objects to a file
#     with open(f'{cfg.BASE_DIR}/app/resources/instructions/output.json', 'w', encoding='utf-8') as f:
#         json.dump(json_data_list, f, ensure_ascii=False, indent=4)
#     return json_data_list
#
#
# def get_answer(que):
#     json_data_list = get_data()
#
#     directory_read_tool = DirectoryReadTool(directory=f'{cfg.BASE_DIR}/app/resources/instructions/')
#     file_read_tool = FileReadTool()
#     search_tool = SerperDevTool()
#     project_manager_agent = Agent(
#         role="Project Manager",
#         goal="Monitor and analyze jira issues and csv files"
#              "to identify which ticket is has been assigned whom complexity of the tasks and answer the que by observing all files carefully",
#         backstory="Specializing in Project Management, this agent "
#                   "uses statistical modeling and machine learning "
#                   "to provide crucial insights. With a knack for data, "
#                   "the Project Manager Agent is the cornerstone for "
#                   "informing issues and comments decisions.",
#         verbose=True,
#         allow_delegation=True,
#         tools=[directory_read_tool, file_read_tool]
#     )
#     # Task for Data Analyst Agent: Analyze Market Data
#     project_management_task = Task(
#         description=(
#             "Continuously monitor and analyze jira issues"
#             "answer the questions by observing all the csv files"
#             "and try to analyse the {question} find out the relevant answer from jira issues json data and csv files"
#             "Use generative model to "
#             "prepare the right answer"
#         ),
#         expected_output=(
#             "give the relevant and specific answer if you know"
#             "otherwise just say I don't know the answer of your question {question}."
#         ),
#         agent=project_manager_agent,
#     )
#
#     from crewai import Crew, Process
#     from langchain_openai import ChatOpenAI
#
#     # Define the crew with agents and tasks
#     project_manager_crew = Crew(
#         agents=[project_manager_agent],
#
#         tasks=[project_management_task],
#
#         manager_llm=ChatOpenAI(model= "gpt-4o", #"gpt-3.5-turbo",
#                                temperature=0.7),
#         # process=Process.hierarchical,
#         verbose=True,
#         memory=True
#
#     )
#     inputs = {
#         "question": que
#     }
#     result = project_manager_crew.kickoff(inputs=inputs)
#
#     return {"data":result}
#
#


import os
import json
from crewai import Agent, Task, Crew
from crewai_tools import DirectoryReadTool, FileReadTool, SerperDevTool
from langchain_openai import ChatOpenAI
import app.config as cfg

# Set up environment variables
os.environ["OPENAI_MODEL_NAME"] = "gpt-4"
os.environ['OPENAI_API_KEY'] = cfg.OPENAI_API_KEY

# Define the directory to read from
DATA_DIRECTORY = f'{cfg.BASE_DIR}/app/resources/instructions/'

def get_data():
    directory_read_tool = DirectoryReadTool(directory=DATA_DIRECTORY)
    file_list = directory_read_tool._run()
    data = {}
    for file_name in file_list:
        if file_name.endswith('.json'):
            with open(os.path.join(DATA_DIRECTORY, file_name), 'r', encoding='utf-8') as f:
                data[file_name] = json.load(f)
    return data

def get_answer(que):
    directory_read_tool = DirectoryReadTool(directory=DATA_DIRECTORY)
    file_read_tool = FileReadTool()

    project_manager_agent = Agent(
        role="Project Manager",
        goal="Analyze files in the specified directory to answer questions about project management",
        backstory="As a Project Manager, I specialize in analyzing project data from various files to provide insights and answer questions.",
        verbose=True,
        allow_delegation=True,
        tools=[directory_read_tool, file_read_tool]
    )

    project_management_task = Task(
        description=(
            f"Read and analyze all files in the directory: {DATA_DIRECTORY}. "
            "Pay special attention to JSON files containing project data. "
            "Based on the content of these files, answer the following question: {question}"
        ),
        expected_output=(
            "Provide a relevant and specific answer based on the information found in the files. "
            "If the answer cannot be determined from the available data, state that clearly."
        ),
        agent=project_manager_agent,
    )

    project_manager_crew = Crew(
        agents=[project_manager_agent],
        tasks=[project_management_task],
        manager_llm=ChatOpenAI(model="gpt-4o", temperature=0.7),
        verbose=True,
        memory=True
    )

    inputs = {
        "question": que
    }
    result = project_manager_crew.kickoff(inputs=inputs)

    return {"data": result}

# Example usage
if __name__ == "__main__":
    question = "how many tickets currently available in the bucket"
    answer = get_answer(question)
    print(answer)