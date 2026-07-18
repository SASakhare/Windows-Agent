from src.agent.messages.messages import Message, MessageRole

from src.agent.runtime.runtime_builder import build_runtime


def main():

    runtime = build_runtime()

    state = runtime._context.state

    state.goal.user_goal = "Open google.com"

    state.conversation.conversation_history.append(
        Message(
            role=MessageRole.USER,
            content="Open google.com",
        )
    )

    runtime.run()

    print("\n")
    print("=" * 100)
    print("PLANNING")
    print("=" * 100)
    print(state.planning)

    print("\n")
    print("=" * 100)
    print("EXECUTION")
    print("=" * 100)
    print(state.execution)

    print("\n")
    print("=" * 100)
    print("OBSERVATION")
    print("=" * 100)
    print(runtime._context.observation_result)

    print("\n")
    print("=" * 100)
    print("WORLD STATE")
    print("=" * 100)
    print(state.world)

    print("\n")
    print("=" * 100)
    print("reflection STATE")
    print("=" * 100)
    print(state.reflection)

    print("\n")
    print("=" * 100)
    print("recovery STATE")
    print("=" * 100)
    print(state.recovery)


if __name__ == "__main__":
    main()