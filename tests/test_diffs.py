import re
from sweepai.utils.diff import format_contents

# # Test real one line change
# old_file_content = """print("Hello World")"""
# new_file_content = """print("Hello Sweep")"""

# # Test middle cutoff
# old_file_content_a = """\
# print("Hello World")
# print("Hello World")
# print("Hello World")
# print("Hello World")
# """
# new_file_content_a = """\
# print("Hello World")
# # Rest of code
# print("Hello World")
# """

# # Test end cutoff
# old_file_content_b = """\
# print("Hello World")
# print("Hello World")
# print("Hello World")
# print("Hello World")
# """
# new_file_content_b = """\
# print("Hello World")
# # Rest of code
# """

# # Test a real difference
# old_file_content_c = """\
# print("Hello World")
# print("Hello World")
# print("Hello World")
# print("Hello World")
# """
# new_file_content_c = """\
# print("Hello World")print("Hello Sweep")
# print("Hello World")
# """

# # Test beginning cutoff
# old_file_content_d = """\
# print("Hello World")
# print("Hello World")
# print("Hello World")
# print("Hello World")
# """
# new_file_content_d = """\
# # Rest of code
# print("Hello World")
# """

# # Test two changes
# old_file_content_e = """\
# def match(line):
#     lowercase = line.lower().strip()
#     semantic_match = "rest" in lowercase or "remaining" in lowercase or "..." in lowercase
#     is_comment = lowercase.startswith("#") or lowercase.startswith("//")
#     return semantic_match and is_comment
# """
# new_file_content_e = """\
# def match(line):
#     semantic_match = "rest" in lowercase or "remaining" in lowercase or "..." in lowercase
#     return semantic_match and is_comment
# """

# # Test two changes
# old_file_content_f = """\
# def match(line):
#     lowercase = line.lower().strip()
#     semantic_match = "rest" in lowercase or "remaining" in lowercase or "..." in lowercase
#     is_comment = lowercase.startswith("#") or lowercase.startswith("//")
#     return semantic_match and is_comment
# """
# new_file_content_f = """\
# def match(line):
#     semantic_match = "rest" in lowercase or "remaining" in lowercase or "..." in lowercase
#     # ...
#     return semantic_match and is_comment
# """
# result_f = """\
# def match(line):
#     semantic_match = "rest" in lowercase or "remaining" in lowercase or "..." in lowercase
#     is_comment = lowercase.startswith("#") or lowercase.startswith("//")
#     return semantic_match and is_comment
# """

# old_file_content_g = """\
# def match(line):
#     lowercase = line.lower().strip()
#     semantic_match = "rest" in lowercase or "remaining" in lowercase or "..." in lowercase
#     is_comment = lowercase.startswith("#") or lowercase.startswith("//")
#     return semantic_match and is_comment
# """
# new_file_content_g = """\
# def match(line):
#     semantic_match = "rest" in lowercase or "remaining" in lowercase or "..." in lowercase
#     is_comment = lowercase.startswith("#") or lowercase.startswith("//")
# """

# old_file_content_h = """\
# def match(line):
#     lowercase = line.lower().strip()
#     semantic_match = "rest" in lowercase or "remaining" in lowercase or "..." in lowercase
#     is_comment = lowercase.startswith("#") or lowercase.startswith("//")
#     return semantic_match and is_comment
# """
# new_file_content_h = """\
#     semantic_match = "rest" in lowercase or "remaining" in lowercase or "..." in lowercase
#     is_comment = lowercase.startswith("#") or lowercase.startswith("//")
#     return semantic_match and is_comment
# """

# old_file_content_i = """\
# def match(line):
#     lowercase = line.lower().strip()
#     semantic_match = "rest" in lowercase or "remaining" in lowercase or "..." in lowercase
#     is_comment = lowercase.startswith("#") or lowercase.startswith("//")
#     return semantic_match and is_comment
# """
# new_file_content_i = """\
# # ...
#     semantic_match = "rest" in lowercase or "remaining" in lowercase or "..." in lowercase
#     is_comment = lowercase.startswith("#") or lowercase.startswith("//")
#     return semantic_match and is_comment
# """

# old_file_content_j = """\
# def match(line):
#     lowercase = line.lower().strip()
#     semantic_match = "rest" in lowercase or "remaining" in lowercase or "..." in lowercase
#     is_comment = lowercase.startswith("#") or lowercase.startswith("//")
#     return semantic_match and is_comment
# """
# new_file_content_j = """\
# def match(line):
#     lowercase = line.lower().strip()
#     semantic_match = "rest" in lowercase or "remaining" in lowercase or "..." in lowercase
#     is_comment = lowercase.startswith("#") or lowercase.startswith("//")
# # ...
# """
    
# if __name__ == "__main__":
#     # replaced_new_file_content = fuse_files(old_file_content, new_file_content)
#     # assert replaced_new_file_content == new_file_content + "\n"
#     # replaced_new_file_content = fuse_files(old_file_content_a, new_file_content_a)
#     # assert replaced_new_file_content == old_file_content_a
#     # replaced_new_file_content = fuse_files(old_file_content_b, new_file_content_b)
#     # assert replaced_new_file_content == old_file_content_b
#     # replaced_new_file_content = fuse_files(old_file_content_c, new_file_content_c)
#     # assert replaced_new_file_content == new_file_content_c
#     # replaced_new_file_content = fuse_files(old_file_content_d, new_file_content_d)
#     # assert replaced_new_file_content == old_file_content_d
#     # replaced_new_file_content = fuse_files(old_file_content_e, new_file_content_e)
#     # assert replaced_new_file_content == new_file_content_e
#     # replaced_new_file_content = fuse_files(old_file_content_f, new_file_content_f)
#     # assert replaced_new_file_content == result_f
#     # replaced_new_file_content = fuse_files(old_file_content_g, new_file_content_g)
#     # assert replaced_new_file_content == new_file_content_g
#     # replaced_new_file_content = fuse_files(old_file_content_h, new_file_content_h)
#     # assert replaced_new_file_content == new_file_content_h
#     # replaced_new_file_content = fuse_files(old_file_content_i, new_file_content_i)
#     # assert replaced_new_file_content == old_file_content_i
#     # replaced_new_file_content = fuse_files(old_file_content_j, new_file_content_j)
#     # assert replaced_new_file_content == old_file_content_j

#     test_file = """import torch
# import torchvision
# import torchvision.transforms as transforms

# def load_data():
#     # Load the training and testing data
#     # This is just a placeholder and should be replaced with your actual data loading code
#     pass

# def init_model():
#     # Initialize the model
#     # This is just a placeholder and should be replaced with your actual model initialization code
#     pass

# def train_model():
#     # Train the model
#     # This is just a placeholder and should be replaced with your actual model training code
#     pass

# def main():
#     # Load the data
#     load_data()

#     # Initialize the model
#     init_model()

#     # Train the model
#     train_model()

# if __name__ == "__main__":
#     main()
# ```

#     """
#     print(format_contents(test_file))
#     test_file = """```python
# import torch
# import torchvision
# import torchvision.transforms as transforms

# def load_data():
#     # Load the training and testing data
#     # This is just a placeholder and should be replaced with your actual data loading code
#     pass

# def init_model():
#     # Initialize the model
#     # This is just a placeholder and should be replaced with your actual model initialization code
#     pass

# def train_model():
#     # Train the model
#     # This is just a placeholder and should be replaced with your actual model training code
#     pass

# def main():
#     # Load the data
#     load_data()

#     # Initialize the model
#     init_model()

#     # Train the model
#     train_model()

# if __name__ == "__main__":
#     main()
# ```

#     """
#     print(format_contents(test_file))

#     test_file = """```python
# import torch
# import torchvision
# import torchvision.transforms as transforms

# def load_data():
#     # Load the training and testing data
#     # This is just a placeholder and should be replaced with your actual data loading code
#     pass

# def init_model():
#     # Initialize the model
#     # This is just a placeholder and should be replaced with your actual model initialization code
#     pass
#     reg = ```abc```
# def train_model():
#     # Train the model
#     # This is just a placeholder and should be replaced with your actual model training code
#     pass

# def main():
#     # Load the data
#     load_data()

#     # Initialize the model
#     init_model()

#     # Train the model
#     train_model()

# if __name__ == "__main__":
#     main()
# ```

#     """
#     print(format_contents(test_file))
# from sweepai.utils.diff import format_contents, fuse_files

# # Test real one line change
# old_file_content = """print("Hello World")"""
# new_file_content = """print("Hello Sweep")"""

# # Test middle cutoff
# old_file_content_a = """\
# print("Hello World")
# print("Hello World")
# print("Hello World")
# print("Hello World")
# """
# new_file_content_a = """\
# print("Hello World")
# # Rest of code
# print("Hello World")
# """

# # Test end cutoff
# old_file_content_b = """\
# print("Hello World")
# print("Hello World")
# print("Hello World")
# print("Hello World")
# """
# new_file_content_b = """\
# print("Hello World")
# # Rest of code
# """

# # Test a real difference
# old_file_content_c = """\
# print("Hello World")
# print("Hello World")
# print("Hello World")
# print("Hello World")
# """
# new_file_content_c = """\
# print("Hello World")print("Hello Sweep")
# print("Hello World")
# """

# # Test beginning cutoff
# old_file_content_d = """\
# print("Hello World")
# print("Hello World")
# print("Hello World")
# print("Hello World")
# """
# new_file_content_d = """\
# # Rest of code
# print("Hello World")
# """

# # Test two changes
# old_file_content_e = """\
# def match(line):
#     lowercase = line.lower().strip()
#     semantic_match = "rest" in lowercase or "remaining" in lowercase or "..." in lowercase
#     is_comment = lowercase.startswith("#") or lowercase.startswith("//")
#     return semantic_match and is_comment
# """
# new_file_content_e = """\
# def match(line):
#     semantic_match = "rest" in lowercase or "remaining" in lowercase or "..." in lowercase
#     return semantic_match and is_comment
# """

# # Test two changes
# old_file_content_f = """\
# def match(line):
#     lowercase = line.lower().strip()
#     semantic_match = "rest" in lowercase or "remaining" in lowercase or "..." in lowercase
#     is_comment = lowercase.startswith("#") or lowercase.startswith("//")
#     return semantic_match and is_comment
# """
# new_file_content_f = """\
# def match(line):
#     semantic_match = "rest" in lowercase or "remaining" in lowercase or "..." in lowercase
#     # ...
#     return semantic_match and is_comment
# """
# result_f = """\
# def match(line):
#     semantic_match = "rest" in lowercase or "remaining" in lowercase or "..." in lowercase
#     is_comment = lowercase.startswith("#") or lowercase.startswith("//")
#     return semantic_match and is_comment
# """

# old_file_content_g = """\
# def match(line):
#     lowercase = line.lower().strip()
#     semantic_match = "rest" in lowercase or "remaining" in lowercase or "..." in lowercase
#     is_comment = lowercase.startswith("#") or lowercase.startswith("//")
#     return semantic_match and is_comment
# """
# new_file_content_g = """\
# def match(line):
#     semantic_match = "rest" in lowercase or "remaining" in lowercase or "..." in lowercase
#     is_comment = lowercase.startswith("#") or lowercase.startswith("//")
# """

# old_file_content_h = """\
# def match(line):
#     lowercase = line.lower().strip()
#     semantic_match = "rest" in lowercase or "remaining" in lowercase or "..." in lowercase
#     is_comment = lowercase.startswith("#") or lowercase.startswith("//")
#     return semantic_match and is_comment
# """
# new_file_content_h = """\
#     semantic_match = "rest" in lowercase or "remaining" in lowercase or "..." in lowercase
#     is_comment = lowercase.startswith("#") or lowercase.startswith("//")
#     return semantic_match and is_comment
# """

# old_file_content_i = """\
# def match(line):
#     lowercase = line.lower().strip()
#     semantic_match = "rest" in lowercase or "remaining" in lowercase or "..." in lowercase
#     is_comment = lowercase.startswith("#") or lowercase.startswith("//")
#     return semantic_match and is_comment
# """
# new_file_content_i = """\
# # ...
#     semantic_match = "rest" in lowercase or "remaining" in lowercase or "..." in lowercase
#     is_comment = lowercase.startswith("#") or lowercase.startswith("//")
#     return semantic_match and is_comment
# """

# old_file_content_j = """\
# def match(line):
#     lowercase = line.lower().strip()
#     semantic_match = "rest" in lowercase or "remaining" in lowercase or "..." in lowercase
#     is_comment = lowercase.startswith("#") or lowercase.startswith("//")
#     return semantic_match and is_comment
# """
# new_file_content_j = """\
# def match(line):
#     lowercase = line.lower().strip()
#     semantic_match = "rest" in lowercase or "remaining" in lowercase or "..." in lowercase
#     is_comment = lowercase.startswith("#") or lowercase.startswith("//")
# # ...
# """
    
# if __name__ == "__main__":
#     # replaced_new_file_content = fuse_files(old_file_content, new_file_content)
#     # assert replaced_new_file_content == new_file_content + "\n"
#     # replaced_new_file_content = fuse_files(old_file_content_a, new_file_content_a)
#     # assert replaced_new_file_content == old_file_content_a
#     # replaced_new_file_content = fuse_files(old_file_content_b, new_file_content_b)
#     # assert replaced_new_file_content == old_file_content_b
#     # replaced_new_file_content = fuse_files(old_file_content_c, new_file_content_c)
#     # assert replaced_new_file_content == new_file_content_c
#     # replaced_new_file_content = fuse_files(old_file_content_d, new_file_content_d)
#     # assert replaced_new_file_content == old_file_content_d
#     # replaced_new_file_content = fuse_files(old_file_content_e, new_file_content_e)
#     # assert replaced_new_file_content == new_file_content_e
#     # replaced_new_file_content = fuse_files(old_file_content_f, new_file_content_f)
#     # assert replaced_new_file_content == result_f
#     # replaced_new_file_content = fuse_files(old_file_content_g, new_file_content_g)
#     # assert replaced_new_file_content == new_file_content_g
#     # replaced_new_file_content = fuse_files(old_file_content_h, new_file_content_h)
#     # assert replaced_new_file_content == new_file_content_h
#     # replaced_new_file_content = fuse_files(old_file_content_i, new_file_content_i)
#     # assert replaced_new_file_content == old_file_content_i
#     # replaced_new_file_content = fuse_files(old_file_content_j, new_file_content_j)
#     # assert replaced_new_file_content == old_file_content_j

#     test_file = """import torch
# import torchvision
# import torchvision.transforms as transforms

# def load_data():
#     # Load the training and testing data
#     # This is just a placeholder and should be replaced with your actual data loading code
#     pass

# def init_model():
#     # Initialize the model
#     # This is just a placeholder and should be replaced with your actual model initialization code
#     pass

# def train_model():
#     # Train the model
#     # This is just a placeholder and should be replaced with your actual model training code
#     pass

# def main():
#     # Load the data
#     load_data()

#     # Initialize the model
#     init_model()

#     # Train the model
#     train_model()

# if __name__ == "__main__":
#     main()
# ```

#     """
#     print(format_contents(test_file))
#     test_file = """```python
# import torch
# import torchvision
# import torchvision.transforms as transforms

# def load_data():
#     # Load the training and testing data
#     # This is just a placeholder and should be replaced with your actual data loading code
#     pass

# def init_model():
#     # Initialize the model
#     # This is just a placeholder and should be replaced with your actual model initialization code
#     pass

# def train_model():
#     # Train the model
#     # This is just a placeholder and should be replaced with your actual model training code
#     pass

# def main():
#     # Load the data
#     load_data()

#     # Initialize the model
#     init_model()

#     # Train the model
#     train_model()

# if __name__ == "__main__":
#     main()
# ```

#     """
#     print(format_contents(test_file))

#     test_file = """```python
# import torch
# import torchvision
# import torchvision.transforms as transforms

# def load_data():
#     # Load the training and testing data
#     # This is just a placeholder and should be replaced with your actual data loading code
#     pass

# def init_model():
#     # Initialize the model
#     # This is just a placeholder and should be replaced with your actual model initialization code
#     pass
#     reg = ```abc```
# def train_model():
#     # Train the model
#     # This is just a placeholder and should be replaced with your actual model training code
#     pass

# def main():
#     # Load the data
#     load_data()

#     # Initialize the model
#     init_model()

#     # Train the model
#     train_model()

# if __name__ == "__main__":
#     main()
# ```

#     """
#     print(format_contents(test_file))

test_file = """
test.py
```python
import json
from github import Github
import gradio as gr
from loguru import logger
import webbrowser
from gradio import Button
from sweepai.app.api_client import APIClient, create_pr_function, create_pr_function_call
from sweepai.app.config import SweepChatConfig
from sweepai.core.entities import Snippet

config = SweepChatConfig.load()

api_client = APIClient(config=config)

pr_summary_template = '''💡 I'll create the following PR:

**{title}**
{summary}

Here is my plan:
{plan}

Reply with "ok" to create the PR or anything else to propose changes.'''

github_client = Github(config.github_pat)
repos = list(github_client.get_user().get_repos())

css = '''
footer {
    visibility: hidden;
}
pre, code {
    white-space: pre-wrap !important;
    word-break: break-all !important;
}
#snippets {
    height: 750px;
    overflow-y: scroll;
}
'''

def get_files_recursively(repo, path=''):
    path_to_contents = {}
    try:
        contents = repo.get_contents(path)
        files = []
        while contents:
            file_content = contents.pop(0)
            if file_content.type == 'dir':
                contents.extend(repo.get_contents(file_content.path))
            else:
                try:
                    decoded_contents = file_content.decoded_content.decode("utf-8")
                except:
                    continue
                if decoded_contents:
                    path_to_contents[file_content.path] = file_content.decoded_content.decode("utf-8")
                    files.append(file_content.path)
        return sorted(files), path_to_contents
    except Exception as e:
        logger.error(e)
        return [], path_to_contents

def create_pr_button_click():
    global proposed_pr
    if proposed_pr:
        chat_history = [[None, f"⏳ Creating PR..."]]
        pull_request = api_client.create_pr(
            file_change_requests=[(item["file_path"], item["instructions"]) for item in proposed_pr["plan"]],
            pull_request={
                "title": proposed_pr["title"],
                "content": proposed_pr["summary"],
                "branch_name": proposed_pr["branch"],
            },
            messages=chat_history,
        )
        chat_history[-1][1] = f"✅ PR created at {pull_request['html_url']}"
        return chat_history

with gr.Blocks(theme=gr.themes.Soft(), title="Sweep Chat", css=css) as demo:
    with gr.Row():
        with gr.Column():
            repo_full_name = gr.Dropdown(choices=[repo.full_name for repo in repos], label="Repo full name", value=config.repo_full_name or "")
        with gr.Column(scale=2):
            repo = github_client.get_repo(config.repo_full_name)
            all_files, path_to_contents = get_files_recursively(repo)
            file_names = gr.Dropdown(choices=all_files, multiselect=True, label="Files")
    with gr.Row():
        with gr.Column(scale=2):
            chatbot = gr.Chatbot(height=750)
        with gr.Column():
            snippets_text = gr.Markdown(value="### Relevant snippets", elem_id="snippets")
    create_pr_button = Button("Create PR", create_pr_button_click)
    msg = gr.Textbox(label="Message to Sweep", placeholder="Write unit tests for OpenAI calls")
    # clear = gr.ClearButton([msg, chatbot, snippets_text])

    proposed_pr: str | None = None
    searched = False
    selected_snippets = []
    file_to_str = {}

    def repo_name_change(repo_full_name):
        global installation_id
        try:
            config.repo_full_name = repo_full_name
            api_client.config = config
            installation_id = api_client.get_installation_id()
            assert installation_id
            config.installation_id = installation_id
            api_client.config = config
            config.save()
            return ""
        except Exception as e:
            webbrowser.open_new_tab("https://github.com/apps/sweep-ai")
            config.repo_full_name = None
            config.installation_id = None
            config.save()
            api_client.config = config
            raise e

    repo_full_name.change(repo_name_change, [repo_full_name], [msg])

    def build_string():
        global selected_snippets
        global file_to_str
        for snippet in selected_snippets:
            file_name = snippet.file_path
            if file_name not in file_to_str:
                add_file_to_dict(file_name)
        snippets_text = "### Relevant snippets:\n" + "\n\n".join([file_to_str[snippet.file_path] for snippet in selected_snippets])
        return snippets_text

    def add_file_to_dict(file_name):
        global file_to_str
        global path_to_contents
        if file_name in path_to_contents:
            file_contents = path_to_contents[file_name]
        else:
            file_contents = repo.get_contents(file_name).decoded_content.decode('utf-8')
        file_contents_split = file_contents.split("\n")
        length = len(file_contents_split)
        backtick, escaped_backtick = "`", "\\`"
        preview = "\n".join(file_contents_split[:3]).replace(backtick, escaped_backtick)
        file_to_str[file_name] = f'{file_name}:0:{length}\n```python\n{preview}\n...\n```'
    
    def file_names_change(file_names):
        global selected_snippets
        global file_to_str
        global path_to_contents
        selected_snippets = [Snippet(content=path_to_contents[file_name], start=0, end=path_to_contents[file_name].count('\n'), file_path=file_name) for file_name in file_names]
        return file_names, build_string()
    
    file_names.change(file_names_change, [file_names], [file_names, snippets_text])
    
    def handle_message_submit(repo_full_name: str, user_message: str, history: list[tuple[str | None, str | None]]):
        if not repo_full_name:
            raise Exception("Set the repository name first")
        return gr.update(value="", interactive=False), history + [[user_message, None]]

    def handle_message_stream(chat_history: list[tuple[str | None, str | None]], snippets_text, file_names):
        global selected_snippets
        global searched
        message = chat_history[-1][0]
        yield chat_history, snippets_text, file_names
        if not selected_snippets:
            searched = True
            # Searching for relevant snippets
            chat_history[-1][1] = "Searching for relevant snippets..."
            snippets_text = build_string()
            yield chat_history, snippets_text, file_names
            logger.info("Fetching relevant snippets...")
            selected_snippets += api_client.search(chat_history[-1][0], 3)
            snippets_text = build_string()
            file_names = [snippet.file_path for snippet in selected_snippets]
            yield chat_history, snippets_text, file_names
            logger.info("Fetched relevant snippets.")
            chat_history[-1][1] = "Found relevant snippets."
            # Update using chat_history
            snippets_text = build_string()
            yield chat_history, snippets_text, file_names
        
        global proposed_pr
        if proposed_pr and chat_history[-1][0].strip().lower() in ("okay", "ok"):
            chat_history[-1][1] = f"⏳ Creating PR..."
            yield chat_history, snippets_text, file_names
            pull_request = api_client.create_pr(
                file_change_requests=[(item["file_path"], item["instructions"]) for item in proposed_pr["plan"]],
                pull_request={
                    "title": proposed_pr["title"],
                    "content": proposed_pr["summary"],
                    "branch_name": proposed_pr["branch"],
                },
                messages=chat_history,
            )
            chat_history[-1][1] = f"✅ PR created at {pull_request['html_url']}"
            yield chat_history, snippets_text, file_names
            return

        # Generate response
        logger.info("...")
        chat_history.append([None, "..."])
        yield chat_history, snippets_text, file_names
        chat_history[-1][1] = ""
        logger.info("Starting to generate response...")
        if len(chat_history) > 1 and "create pr" in message.lower():
            stream = api_client.stream_chat(
                chat_history, 
                selected_snippets,
                functions=[create_pr_function],
                function_call=create_pr_function_call,
            )
        else:
            stream = api_client.stream_chat(chat_history, selected_snippets)
        function_name = ""
        raw_arguments = ""
        for chunk in stream:
            if chunk.get("content"):
                token = chunk["content"]
                chat_history[-1][1] += token
                yield chat_history, snippets_text, file_names
            if chunk.get("function_call"):
                function_call = chunk["function_call"]
                function_name = function_name or function_call.get("name")
                raw_arguments += function_call.get("arguments")
                chat_history[-1][1] = f"Calling function: `{function_name}`\n```json\n{raw_arguments}\n```"
                yield chat_history, snippets_text, file_names
        if function_name:
            arguments = json.loads(raw_arguments)
            if function_name == "create_pr":
                assert "title" in arguments
                assert "summary" in arguments
                assert "plan" in arguments
                if "branch" not in arguments:
                    arguments["branch"] = arguments["title"].lower().replace(" ", "_").replace("-", "_")[:50]
                chat_history[-1][1] = pr_summary_template.format(
                    title=arguments["title"],
                    summary=arguments["summary"],
                    plan="\n".join([f"* `{item['file_path']}`: {item['instructions']}" for item in arguments["plan"]])
                )
                yield chat_history, snippets_text, file_names
                proposed_pr = arguments
            else:
                raise NotImplementedError

    response = msg.submit(handle_message_submit, [repo_full_name, msg, chatbot], [msg, chatbot], queue=False).then(handle_message_stream, [chatbot, snippets_text, file_names], [chatbot, snippets_text, file_names])
    response.then(lambda: gr.update(interactive=True), None, [msg], queue=False)


if __name__ == "__main__":
    demo.queue()
    demo.launch()
```
"""

# test_file = """
# ```python
# def main():
# ```"""

# test_file = """
# ```python
# def main():
# print(n)
# ```"""

test_file = """
test
```python
def main():
print(n)
def main():
print(n)
```"""

print(format_contents(test_file, False))