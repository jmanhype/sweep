import re
import subprocess
from sweepai.core.chat import ChatGPT
from sweepai.core.entities import Message
from sweepai.core.prompts import code_repair_system_prompt, code_repair_prompt

response_regex = r"```[^\n]*(?P<response>.+)```"


class CodeRepairer(ChatGPT):
    # idk why this part breaks
    # messages: list[Message] = [Message(role="system", content=code_repair_system_prompt)]
    # model = "gpt-3.5-turbo-16k-0613"

    @staticmethod
    def check_syntax(old_code, file_extension: str) -> bool:
        # this is WIP
        raise NotImplementedError()
        if file_extension == '.py':
            # Use Python's built-in formatter "Black"
            result = subprocess.run(['black', '--check', filename], text=True, capture_output=True)
        elif file_extension == '.tsx' or file_extension == '.js':
            # Use Prettier for JavaScript and TypeScript formatting
            result = subprocess.run(['prettier', '--check', filename], text=True, capture_output=True)
        elif file_extension == '.cs':
            # Use dotnet-format for C# formatting
            result = subprocess.run(['dotnet-format', '--check', '--include', filename], text=True, capture_output=True)
        elif file_extension == '.go':
            # Use gofmt for Go formatting
            result = subprocess.run(['gofmt', '-l', filename], text=True, capture_output=True)
        elif file_extension == '.rs':
            # Use rustfmt for Rust formatting
            result = subprocess.run(['rustfmt', '--check', filename], text=True, capture_output=True)
        else:
            print(f'No formatter for {file_extension} files')
            return False

        # If the return code is 0, that means the syntax is correct.
        # Else, there was a syntax error.
        if result.returncode == 0:
            return True
        else:
            print(result.stderr)
            return False


    def repair_code(self, diff: str, user_code: str, feature:str) -> str:
        self.messages = [Message(role="system", content=code_repair_system_prompt.format(feature=feature))]
        self.model = "gpt-3.5-turbo-16k-0613" # can be optimized
        response = self.chat(code_repair_prompt.format(diff=diff, user_code=user_code))
        self.undo()
        return response.strip() + "\n"

