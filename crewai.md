# CrewAI Configuration

### Creating crewai project
crewai create crew organize_meetings

1. Select provider:            openai
2. Select model:               gpt-4o
3. Enter provider API key:     XXXXXXXXXXXXXXXXXXXXXXXXX


### Generated catalog structure (most important parts)
```
my_project/
├── .gitignore
├── pyproject.toml
├── README.md
├── .env
└── src/
    └── my_project/
        ├── __init__.py
        ├── main.py
        ├── crew.py
        ├── tools/
        │   ├── custom_tool.py
        │   └── __init__.py
        └── config/
            ├── agents.yaml
            └── tasks.yaml

```

### Most important catalogs and files - brief description

```
agents.yaml	    Define your AI agents and their roles
tasks.yaml	    Set up agent tasks and workflows
.env	        Store API keys and environment variables
main.py	        Project entry point and execution flow
crew.py	        Crew orchestration and coordination
tools/	        Directory for custom agent tools
```
### Running crewai project

```
cd organize_meeting
.\.venv\Scripts\activate
crewai install

crewai run
```
