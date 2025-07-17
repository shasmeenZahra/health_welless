import asyncio
from typing import Callable, Awaitable

# Async-compatible hook signatures
BeforeHook = Callable[[str], Awaitable[None]]
AfterHook = Callable[[str], Awaitable[None]]

# Example: async before/after hooks
async def log_before_hook(user_input: str):
    print(f"📥 [Before Hook] User input: {user_input}")

async def log_after_hook(response: str):
    print(f"📤 [After Hook] Agent response: {response}")

# Dummy async AI agent logic
async def async_agent(user_input: str) -> str:
    await asyncio.sleep(1)  # Simulate API delay
    return f"✅ Processed input: {user_input}"

# Main wrapper with async hooks
async def run_agent_with_hooks(
    user_input: str,
    before: BeforeHook = None,
    after: AfterHook = None,
):
    if before:
        await before(user_input)

    response = await async_agent(user_input)

    if after:
        await after(response)

    return response

# Example usage
if __name__ == "__main__":
    async def main():
        input_text = "How many calories should I eat?"
        result = await run_agent_with_hooks(
            input_text,
            before=log_before_hook,
            after=log_after_hook
        )
        print("🎯 Final Result:", result)

    asyncio.run(main())
