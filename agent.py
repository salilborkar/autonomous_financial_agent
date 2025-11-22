import os
import sys

# Standard Imports
from langchain_google_genai import ChatGoogleGenerativeAI
# We use the specific path for AgentExecutor to avoid version errors
from langchain.agents.agent import AgentExecutor
from langchain.agents import create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

# Import the updated tools
from tools import get_stock_fundamentals, search_market_news

# --- CONFIGURATION ---
if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = input("Enter your Google AI Studio API Key: ").strip()

def main():
    print("--------------------------------------------------")
    print("   AUTONOMOUS HEDGE FUND ANALYST      ")
    print("--------------------------------------------------")
    
    # 1. Define Tools (Now much simpler!)
    my_tools = [get_stock_fundamentals, search_market_news]

    print("Initializing Agent... (Giving Agent its tools)")

    # 2. Initialize the Brain
    # We stick to the stable 1.5 Flash model to avoid 400/404 errors
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0
    )

    # 3. Define the Persona
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a ruthlessly efficient Hedge Fund Analyst. "
                   "Your goal is to provide a clear BUY, SELL, or HOLD recommendation based on data. "
                   "You have access to tools to get stock prices and search the news. "
                   "ALWAYS use your tools to back up your claims with data. "
                   "If you use a tool, explicitly state what data you found."),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    # 4. Construct the Agent
    agent = create_tool_calling_agent(llm, my_tools, prompt)
    
    # 5. Run the Executor
    # We assume you are on the version where AgentExecutor is available
    agent_executor = AgentExecutor(agent=agent, tools=my_tools, verbose=True)

    print("System Ready. Gemini is listening.")

    # 6. The Interaction Loop
    while True:
        user_query = input("\nUser (You): ")
        
        if user_query.lower() in ["exit", "quit"]:
            break
            
        try:
            print("\n... Gemini is thinking (and using tools) ...\n")
            response = agent_executor.invoke({"input": user_query})
            print(f"\nAnalyst Report:\n{response['output']}")
            
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()