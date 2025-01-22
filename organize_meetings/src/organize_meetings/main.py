import yaml
import json
from organize_meetings.crew import InvitationAgent, SchedulerAgent, ConfirmationAgent, NegotiationAgent

# Load configurations from YAML files
def load_yaml(file_path):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)

# Save output data to JSON file
def save_to_file(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

# Main function to execute the task workflow
def main():
    # Load agents and tasks configurations
    agents_config = load_yaml("agents.yaml")
    tasks_config = load_yaml("tasks.yaml")

    # Initialize agents
    agents = {
        "InvitationAgent": InvitationAgent(),
        "SchedulerAgent": SchedulerAgent(),
        "ConfirmationAgent": ConfirmationAgent(),
        "NegotiationAgent": NegotiationAgent(),
    }

    # Sample input data
    friends_list = [
        {"name": "Alice", "email": "alice@example.com"},
        {"name": "Bob", "email": "bob@example.com"},
        {"name": "Charlie", "email": "charlie@example.com"},
    ]
    invitation_template = (
        "Hi {name},\n\nI’m organizing a party! Could you let me know your availability?\n"
        "Please include your preferred time, date, and place.\n\nThanks!"
    )

    # Context for passing inputs and outputs between tasks
    context = {
        "friends_list": friends_list,
        "invitation_template": invitation_template,
    }

    # Execute tasks in the defined order
    for task in tasks_config["tasks"]:
        task_name = task["name"]
        agent_name = task["agent"]
        agent = agents[agent_name]
        print(f"Executing task: {task_name} with agent: {agent_name}")

        # Gather inputs for the task
        inputs = {key: context[key] for key in task.get("inputs", [])}

        # Run the agent
        output = agent.run(**inputs)

        # Save outputs to context
        output_key = task.get("expected_output", "output")
        context[output_key] = output

        # Save output to file if specified
        if "output_file" in task:
            save_to_file(task["output_file"], output)
            print(f"Saved output of {task_name} to {task['output_file']}")

    # Finalize workflow
    print("All tasks completed. Party planning is done!")

if __name__ == "__main__":
    main()
