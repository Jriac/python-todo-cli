import os
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()  # Load environment variables from .env file

client = OpenAI(api_key= os.getenv("OPENAI_API_KEY"))

def create_simple_tasks(description):
    if not client.api_key:
        return ["OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable."]

    try:
        prompt = f"""do a break down of the following task into 3-5 simple sub-tasks.
        Task: {description}
        please provide the substas like so:
        - Sub-task 1
        - Sub-task 2
        - Sub-task 3
        - etc.
        answer only with the sub-tasks, do not include any other text or explanation.
        """
        params = {
            "model": "gpt-6-luna",
            "messages": [
                {"role": "system", "content": "You are a helpful expert assistant that breaks down tasks into simple sub-tasks."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 300,
            "verbosity": "medium",
            "reasoning_effort":"minimal"
            }
        response = client.chat.completions.create(**params)
        content = response.choices[0].message.content.strip()

        subtasks = []

        for line in content.split("\n" ):
            line = line.strip()
            if line.startswith("-"):
                subtask = line[1:].strip()
                if subtask:
                    subtasks.append(subtask)
        return subtasks if subtasks else ["Error: No sub-tasks generated."]
    

    except Exception as e:
        return [f"Error: {str(e)}"] 