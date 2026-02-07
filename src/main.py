import asyncio
from agents.research_intelligence import ResearchIntelligenceAgent

async def main():
    """Main function to run agents"""
    try:
        research_agent = ResearchIntelligenceAgent()

        print("Research Intelligence Agent")
        print("Type 'exit' to quit")
        
        while True:
            user_input = input("User: ")
            if user_input == "exit":
                break
            response = await research_agent.execute(user_input)
            print(f"Agent: {response}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())