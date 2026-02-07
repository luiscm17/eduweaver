import asyncio
from workflows.group_chat_orchestration import GroupChatOrchestration

async def main():
    """Main function to run group chat workflow"""
    try:
        workflow_orchestrator = GroupChatOrchestration()

        print("Eduweaver Group Chat Workflow")
        print("Type 'exit' to quit")
        
        while True:
            user_input = input("User: ")
            if user_input == "exit":
                break
            
            print("Processing with group chat workflow...")
            response = await workflow_orchestrator.execute(user_input)
            print(response)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())