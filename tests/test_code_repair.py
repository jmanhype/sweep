from sweepai.core.code_repair import CodeRepairer

bad_code = """
from sweepai.utils.prompt_constructor import HumanMessageCommentPrompt
from sweepai.utils.constants import PREFIX

github_access_token = os.environ.get("GITHUB_TOKEN")
openai.api_key = os.environ.get("OPENAI_API_KEY")


def on_comment(
    repo_full_name: str,
    repo_description: str,
    comment: str,
    pr_path: str | None,
    pr_line_position: int | None,
    username: str,
    installation_id: int,
    pr_number: int = None,
def on_comment(
    repo_full_name: str,
    repo_description: str,
    comment: str,
    pr_path: str | None,
    pr_line_position: int | None,
    username: str,
    installation_id: int,
    pr_number: int = None,
):
    # Check if the comment is "REVERT"
    if comment.strip().upper() == "REVERT":
        revert_file_to_previous_commit(repo_full_name, pr_path, installation_id)
        return {"success": True}

    # Flow:
    # 1. Get relevant files
    # 2: Get human message
    # 3. Get files to change
    # 4. Get file changes
    # 5. Create PR
    logger.info(f"Calling on_comment() with the following arguments: {comment}, {repo_full_name}, {repo_description}, {pr_path}")
    organization, repo_name = repo_full_name.split("/")
    metadata = {
        "repo_full_name": repo_full_name,
        "repo_name": repo_name,
        "organization": organization,
        "repo_description": repo_description,
        "installation_id": installation_id,
        "username": username,
        "function": "on_comment",
        "mode": PREFIX,
    }

    posthog.capture(username, "started", properties=metadata)
    logger.info(f"Getting repo {repo_full_name}")
    try:
        g = get_github_client(installation_id)
        repo = g.get_repo(repo_full_name)
        pr = repo.get_pull(pr_number)
        branch_name = pr.head.ref
        pr_title = pr.title
        pr_body = pr.body
        diffs = get_pr_diffs(repo, pr)
        snippets, tree = search_snippets(repo, comment, installation_id, branch=branch_name, num_files=1 if pr_path else 3)
        pr_line = None
        pr_file_path = None
        if pr_path and pr_line_position:
            pr_file = repo.get_contents(pr_path, ref=branch_name).decoded_content.decode("utf-8")
            pr_lines = pr_file.splitlines()
            pr_line = pr_lines[min(len(pr_lines), pr_line_position) - 1]
            pr_file_path = pr_path.strip()

            
        logger.info("Getting response from ChatGPT...")
        human_message = HumanMessageCommentPrompt(
            comment=comment,
            repo_name=repo_name,
            repo_description=repo_description if repo_description else "",
            diffs=diffs,
            issue_url=pr.html_url,
            username=username,
            title=pr_title,
            tree=tree,
            summary=pr_body,
            snippets=snippets,
            pr_file_path=pr_file_path, # may be None
            pr_line=pr_line, # may be None
        )
        logger.info(f"Human prompt{human_message.construct_prompt()}")
        sweep_bot = SweepBot.from_system_message_content(
            # human_message=human_message, model="claude-v1.3-100k", repo=repo
            human_message=human_message, repo=repo, 
        )
    except Exception as e:
        posthog.capture(username, "failed", properties={
            "error": str(e),
            "reason": "Failed to get files",
            **metadata
        })
        raise e

    try:
        logger.info("Fetching files to modify/create...")
        file_change_requests = sweep_bot.get_files_to_change()

        logger.info("Making Code Changes...")
        sweep_bot.change_files_in_github(file_change_requests, branch_name)

        logger.info("Done!")
    except Exception as e:
        posthog.capture(username, "failed", properties={
            "error": str(e),
            "reason": "Failed to make changes",
            **metadata
        })
        raise e

    posthog.capture(username, "success", properties={**metadata})
    logger.info("on_comment success")
    return {"success": True}


def revert_file_to_previous_commit(repo_full_name: str, pr_path: str, installation_id: int):
    g = get_github_client(installation_id)
    repo = g.get_repo(repo_full_name)
    file = repo.get_contents(pr_path)
    commit = repo.get_commits(path=file.path)[1]  # Get the second latest commit
    repo.update_file(file.path, "Revert file to previous commit", commit.commit.tree[file.path].content, file.sha)
"""

bad_code = """
# TODO: Add file validation

import os
import openai

from loguru import logger

from sweepai.core.sweep_bot import SweepBot
from sweepai.handlers.on_review import get_pr_diffs
from sweepai.utils.event_logger import posthog
from sweepai.utils.github_utils import (
    get_github_client,
    search_snippets,
)
from sweepai.utils.prompt_constructor import HumanMessageCommentPrompt
from sweepai.utils.constants import PREFIX

github_access_token = os.environ.get("GITHUB_TOKEN")
openai.api_key = os.environ.get("OPENAI_API_KEY")


def on_comment(
    repo_full_name: str,
    repo_description: str,
    comment: str,
    pr_path: str | None,
    pr_line_position: int | None,
    username: str,
    installation_id: int,
    pr_number: int = None,
):
    # Check if the comment is "REVERT"
    if comment.strip().upper() == "REVERT":
        rollback_file(repo_full_name, pr_path, installation_id, pr_number)
        return {"success": True, "message": "File has been reverted to the previous commit."}

    # Rest of the original code
):
    # Flow:
    # 1. Get relevant files
    # 2: Get human message
    # 3. Get files to change
    # 4. Get file changes
    # 5. Create PR
    logger.info(f"Calling on_comment() with the following arguments: {comment}, {repo_full_name}, {repo_description}, {pr_path}")
    organization, repo_name = repo_full_name.split("/")
    metadata = {
        "repo_full_name": repo_full_name,
        "repo_name": repo_name,
        "organization": organization,
        "repo_description": repo_description,
        "installation_id": installation_id,
        "username": username,
        "function": "on_comment",
        "mode": PREFIX,
    }

    posthog.capture(username, "started", properties=metadata)
    logger.info(f"Getting repo {repo_full_name}")
    try:
        g = get_github_client(installation_id)
        repo = g.get_repo(repo_full_name)
        pr = repo.get_pull(pr_number)
        branch_name = pr.head.ref
        pr_title = pr.title
        pr_body = pr.body
        diffs = get_pr_diffs(repo, pr)
        snippets, tree = search_snippets(repo, comment, installation_id, branch=branch_name, num_files=1 if pr_path else 3)
        pr_line = None
        pr_file_path = None
        if pr_path and pr_line_position:
            pr_file = repo.get_contents(pr_path, ref=branch_name).decoded_content.decode("utf-8")
            pr_lines = pr_file.splitlines()
            pr_line = pr_lines[min(len(pr_lines), pr_line_position) - 1]
            pr_file_path = pr_path.strip()

        logger.info("Getting response from ChatGPT...")
        human_message = HumanMessageCommentPrompt(
            comment=comment,
            repo_name=repo_name,
            repo_description=repo_description if repo_description else "",
            diffs=diffs,
            issue_url=pr.html_url,
            username=username,
            title=pr_title,
            tree=tree,
            summary=pr_body,
            snippets=snippets,
            pr_file_path=pr_file_path, # may be None
            pr_line=pr_line, # may be None
        )
        logger.info(f"Human prompt{human_message.construct_prompt()}")
        sweep_bot = SweepBot.from_system_message_content(
            # human_message=human_message, model="claude-v1.3-100k", repo=repo
            human_message=human_message, repo=repo, 
        )
    except Exception as e:
        posthog.capture(username, "failed", properties={
            "error": str(e),
            "reason": "Failed to get files",
            **metadata
        })
        raise e

    try:
        logger.info("Fetching files to modify/create...")
        file_change_requests = sweep_bot.get_files_to_change()

        logger.info("Making Code Changes...")
        sweep_bot.change_files_in_github(file_change_requests, branch_name)

        logger.info("Done!")
    except Exception as e:
        posthog.capture(username, "failed", properties={
            "error": str(e),
            "reason": "Failed to make changes",
            **metadata
        })
        raise e

    posthog.capture(username, "success", properties={**metadata})
    logger.info("on_comment success")
    return {"success": True}
def rollback_file(repo_full_name, pr_path, installation_id, pr_number):
    g = get_github_client(installation_id)
    repo = g.get_repo(repo_full_name)
    pr = repo.get_pull(pr_number)
    branch_name = pr.head.ref

    # Get the file's content from the previous commit
    previous_commit = repo.get_commits()[1]
    previous_file_content = repo.get_contents(pr_path, ref=previous_commit.sha).decoded_content.decode("utf-8")

    # Create a new commit with the previous file content
    repo.update_file(pr_path, "Revert file to previous commit", previous_file_content, repo.get_contents(pr_path).sha, branch=branch_name)
"""

code_repairer = CodeRepairer()
new_code = code_repairer.repair_code(bad_code)
print(new_code)