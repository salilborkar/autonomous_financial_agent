import os
import sys

# 1. Import Google-specific LangChain modules
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import Tool

# 2. Import your custom tools (No changes needed here!)
import tools

# --- CONFIGURATION ---
# Set your Google API Key
if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = input("Enter your Google AI Studio API Key: ").strip()

def main():
    print("--------------------------------------------------")
    print("   AUTONOMOUS HEDGE FUND ANALYST ")
    print("--------------------------------------------------")
    print("Initializing Agent... ")

    # 3. Define the Tools
    my_tools = [
        Tool(
            name="Get_Stock_Fundamentals",
            func=tools.get_stock_fundamentals,
            description="Use this to get the current price, PE ratio, and market cap of a stock. Input should be a ticker symbol (e.g. AAPL)."
        ),
        Tool(
            name="Search_Market_News",
            func=tools.search_market_news,
            description="Use this to search the web for recent news, sentiment, or analyst ratings. Input should be a search query string."
        )
    ]

    # 4. Initialize the Agent Brain
    # "gemini-1.5-flash" is the best balance of speed and reasoning for agents.
    # You can also use "gemini-1.5-pro" if you want deeper analysis.
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0
    )

    # 5. Define the Persona
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a Hedge Fund Analyst. "
                   "Your goal is to provide a clear BUY, SELL, or HOLD recommendation based on data. "
                   "If you use a tool, explicitly state what data you found."),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    # 6. Construct the Agent
    agent = create_tool_calling_agent(llm, my_tools, prompt)
    
    # The Executor runs the loop
    agent_executor = AgentExecutor(agent=agent, tools=my_tools, verbose=True)

    print("System Ready. Agent is listening.")

    # 7. The Interaction Loop
    while True:
        user_query = input("\nUser (You): ")
        
        if user_query.lower() in ["exit", "quit"]:
            break
            
        try:
            print("\n... Agent is thinking (and using tools) ...\n")
            response = agent_executor.invoke({"input": user_query})
            print(f"\nAnalyst Report:\n{response['output']}")
            
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()