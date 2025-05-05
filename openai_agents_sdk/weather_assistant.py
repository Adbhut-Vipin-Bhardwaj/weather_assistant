import asyncio
from openai import AsyncOpenAI
from agents import (
    Agent,
    Runner,
    set_default_openai_api,
    set_default_openai_client,
    set_tracing_disabled,
)
from agents.mcp import MCPServerSse

import weather_agent_prompt


client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="sk-1234",
)
set_default_openai_client(client=client, use_for_tracing=False)
set_default_openai_api("chat_completions")
set_tracing_disabled(disabled=True)


class WeatherAssistant:
    def __init__(self):
        pass

    def __create_agent(self, mcp_server):
        instructions = f"Instructions: {weather_agent_prompt.instructions}\n\nExamples: {weather_agent_prompt.examples}"
        agent = Agent(
            name=weather_agent_prompt.name,
            instructions=instructions,
            mcp_servers=[mcp_server],
            model="openai/gpt-4o-mini",
        )
        return agent

    async def answer(self, user_input):
        async with MCPServerSse(
            name="Weather Assistant Server",
            params={
                "url": "http://localhost:9300/sse",
            }
        ) as mcp_server:
            agent = self.__create_agent(mcp_server=mcp_server)
            response = await Runner.run(starting_agent=agent, input=user_input)
            return response.final_output


if __name__ == "__main__":
    weather_assistant = WeatherAssistant()
    user_input = "What will the weather be in London tomorrow?"
    response = asyncio.run(weather_assistant.answer(user_input=user_input))
    print(response)
