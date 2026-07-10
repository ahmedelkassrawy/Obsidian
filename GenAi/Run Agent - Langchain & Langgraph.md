#### Langchain
```python
def run_agent():

    while True:
        config = {"configurable": {"thread_id": str(uuid.uuid4())}}

        print("=" * 50)
        print("Agent")
        print("=" * 50)
        print("Type 'exit' to quit.\n")

        while True:
            user_input = input("You: ").strip()

            if user_input.lower() in ("exit", "quit"):
                print("Goodbye! 👋")
                return

            if not user_input:
                continue

            result = agent.invoke(
                {
                    "messages": [
                        {
                            "role": "user", 
                            "content": user_input
                        }
                    ]
                },
                config,
            )

            last_message = result["messages"][-1]
            print(f"\nAgent: {last_message.content}\n")


if __name__ == "__main__":
    run_agent()
```

#### Langgraph
```python
def run_agent():
    while True:
        print("=" * 50)
        
        query = input("Enter a query (or 'exit' to quit): ").strip()
        if query.lower() in ("exit", "quit"):
            print("Goodbye!")
            break

        config = {"configurable": {"thread_id": str(uuid.uuid4())}

        initial_state = {
            "patient_id": "",
            "reason_for_visit": "",
            "classification": None,
            "patient_history": None,
            "messages": []
        }

        result = agent.invoke(initial_state, config)
        result = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user", 
                        "content": query
                    }
                ]
            }, config
        )

        # Handle interrupt loop
        while "__interrupt__" in result:
            current_interrupt = result["__interrupt__"][0]
            print("Interrupt:", current_interrupt.value)

            user_response = input(f"{current_interrupt.value['request']}: ").strip()
            
            if user_response.lower() in ("exit", "quit"):
                print("Exiting session.")
                return

            # Resume with the user's input
            result = agent.invoke(Command(resume=user_response), config)

        # Display a user-friendly summary
        print("\n" + "=" * 50)
        print("✅ Session Complete!")
        print(f"  Patient ID    : {result.get('patient_id', 'N/A')}")
        print(f"  Reason        : {result.get('reason_for_visit', 'N/A')}")
        
        classification = result.get("classification")
        
        if classification:
            print(f"  Urgency       : {classification.get('urgency', 'N/A')}")
            print(f"  Department    : {classification.get('department', 'N/A')}")
            print(f"  Topic         : {classification.get('topic', 'N/A')}")
        print("=" * 50)


if __name__ == "__main__":
    run_agent()
```