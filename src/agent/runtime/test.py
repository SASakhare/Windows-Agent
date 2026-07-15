from src.agent.messages.messages import Message, MessageRole
from src.agent.runtime.runtime_builder import build_runtime

TEST_CONVERSATION = [

    # -------------------------
    # Browser
    # -------------------------

    "Hi",

    "Open Google.",

    "Search for LangGraph.",

    "Open the first result.",

    "Scroll down.",

    "Take a screenshot and save it as langgraph.png.",

    # -------------------------
    # Conversation Memory
    # -------------------------

    "Now go back.",

    "Open GitHub.",

    "Search for microsoft playwright repository.",

    "Open it.",

    "What website am I currently on?",

    # -------------------------
    # File
    # -------------------------

    "Create a file named notes.txt.",

    "Write 'LangGraph is a workflow framework.' into the file.",

    "Append 'It is built by LangChain.'",

    "Read the file.",

    "Rename it to ai_notes.txt.",

    # -------------------------
    # Network
    # -------------------------

    "What is my public IP?",

    "Check whether I have internet connectivity.",

    # -------------------------
    # Context Awareness
    # -------------------------

    "Delete the file we created earlier.",

    "What was the last thing I asked you to do?"

]


def main():

    runtime = build_runtime()

    for index, user_input in enumerate(TEST_CONVERSATION, start=1):

        print("\n" + "=" * 100)
        print(f"USER {index}")
        print("=" * 100)

        print(user_input)

        runtime._context.state.conversation.conversation_history.append(

            Message(
                role=MessageRole.USER,
                content=user_input,
            )

        )

        runtime.run()

        print()

        print("=" * 100)
        print("PLANNING")
        print("=" * 100)

        print(runtime._context.state.planning)

        print()

        print("=" * 100)
        print("EXECUTION")
        print("=" * 100)

        print(runtime._context.state.execution)

        print()

        print("=" * 100)
        print("WORLD")
        print("=" * 100)

        print(runtime._context.state.world)

        input("\nPress Enter for next message...")


if __name__ == "__main__":
    main()