import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from langchain_groq import ChatGroq
import agentops
load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
AGENTOPS_API_KEY = os.getenv("AGENTOPS_API_KEY")
agentops.init(api_key=AGENTOPS_API_KEY)
import os
from dotenv import load_dotenv

# --- Prevent ChromaDB from writing to disk ---
import chromadb
from chromadb.config import Settings
os.environ["PERSIST_DIRECTORY"] = ""  # safety: blank disables persistence
chromadb.Client(Settings(persist_directory=None))  # forces in-memory mode

llm = ChatGroq(
    model="moonshotai/kimi-k2-instruct",
    temperature=0.1,
    max_tokens=3000
)

def run_study_assistant(topic, question):
    # --- Agents ---
    explainer = Agent(
        role='Subject Explainer',
        goal='Explain academic topics in simple and engaging language.',
        backstory="You explain concepts clearly with analogies and examples.",
        llm=llm,
        verbose=True
    )

    qa_agent = Agent(
        role='Question Answerer',
        goal='Answer specific academic questions accurately.',
        backstory="You give direct, informative answers.",
        llm=llm,
        verbose=True
    )

    quiz_maker = Agent(
        role='Quiz Generator',
        goal='Create short quizzes based on content.',
        backstory="You reinforce learning with quizzes.",
        llm=llm,
        verbose=True
    )

    # --- Tasks ---
    task1 = Task(
        description=f"Explain the topic '{topic}' in a student-friendly way.",
        expected_output="A simple explanation of the topic.",
        agent=explainer
    )

    task2 = Task(
        description=f"Answer this question: '{question}' in less than 100 words.",
        expected_output="Short and accurate answer.",
        agent=qa_agent
    )

    task3 = Task(
        description=f"Create 3 multiple-choice questions on the topic '{topic}'.",
        expected_output="3 MCQs with 4 options each and correct answers listed.",
        agent=quiz_maker
    )

    # --- Manual Execution of Tasks ---
    explanation = task1.execute()
    answer = task2.execute()
    quiz = task3.execute()

    return {
        "final_output": f"{explanation}\n\n{answer}\n\n{quiz}",
        "steps": {
            "task_1": explanation,
            "task_2": answer,
            "task_3": quiz
        }
    }
