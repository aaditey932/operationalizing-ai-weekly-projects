import asyncio
from agents import Runner
from agents_config import chat_agent

async def main():
    question = input("Ask me: ")
    result = await Runner.run(chat_agent, input=question)
    print("📝 Answer:", result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
