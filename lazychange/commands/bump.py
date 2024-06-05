import os

import click
import git

from openai import OpenAI

from typing import cast

def get_simple_answer(
    openai_client: OpenAI,
    content: str,
    model: str,
) -> str:
    response = openai_client.chat.completions.create(
        model=model,
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": content,
            },
        ],
    )

    answer = cast(str, response.choices[0].message.content)

    return answer.strip()

def get_commit_message(
    diff: str,
    model: str,
    openai_client: OpenAI,
) -> str:
    if len(diff) == 0:
        raise click.ClickException("Diff is empty!")

    content = "Generate a brief commit message (title only)" \
              "for the following changes, use markdown if needed " \
              "(for names of git branches, packages, classes, functions, keywords)" \
              f":\n```diff\n{diff}\n```"

    return get_simple_answer(
        openai_client=openai_client,
        content=content,
        model=model,
    )

def get_new_tag(
    repo: git.Repo,
    model: str,
    openai_client: OpenAI,
) -> str:
    previous_tag = repo.git.describe("--tags", "--abbrev=0")

    content = "Detect versioning style, increment version, and answer with result only, " \
              "ready for tagging (without descriptions and explanations). " \
              f"Current version: {previous_tag}"

    return get_simple_answer(
        openai_client=openai_client,
        content=content,
        model=model,
    )

def get_openai_client(api_key: str | None) -> OpenAI:
    if not api_key:
        raise click.ClickException(
            "OpenAI API key must be provided through " \
            "`--api-key`, " \
            "`OPENAI_API_KEY` or " \
            "`OPENAI_TOKEN`."
        )

    return OpenAI(api_key=api_key)

def run_bump(
    is_need_push_tags: bool,
    is_dry_run: bool,
    repo_path: str,
    model: str,
    openai_client: OpenAI,
) -> None:
    repo = git.Repo(repo_path)

    diff = repo.git.diff()

    message = get_commit_message(
        diff=diff,
        model=model,
        openai_client=openai_client,
    )

    if is_dry_run:
        print(f"Would commit with message:\n{message}\n")
    else:
        repo.git.add(A=True)
        repo.git.commit(m=message)
        repo.git.push()

        print(f"Pushed with commit message:\n{message}\n")

    if is_need_push_tags:
        new_tag = get_new_tag(
            repo=repo,
            model=model,
            openai_client=openai_client,
        )

        if is_dry_run:
            print(f"Would tag:\n{new_tag}\n")
        else:
            repo.git.tag(new_tag)
            repo.git.push(tags=is_need_push_tags)

            print(f"Pushed tag:\n{new_tag}\n")

@click.command()
@click.option(
    "--dry-run",
    is_flag=True,
    help="Doesn't commit or push anything.",
)
@click.option(
    "--tags",
    is_flag=True,
    help="Bumps and pushes the Git tag using ChatGPT.",
)
@click.option(
    "--repo",
    default=".",
    help="Path to the Git repository.",
)
@click.option(
    "--model",
    default="gpt-4o",
    help="OpenAI model to use for generating messages.",
)
@click.option(
    "--api-key",
    default=None,
    help="OpenAI API key.",
)
def bump(
    dry_run: bool,
    tags: bool,
    repo: str,
    model: str,
    api_key: str | None,
) -> None:
    api_key = api_key \
        or os.getenv("OPENAI_API_KEY") \
        or os.getenv("OPENAI_TOKEN")

    openai_client = get_openai_client(api_key)

    run_bump(
        is_need_push_tags=tags,
        is_dry_run=dry_run,
        repo_path=repo,
        model=model,
        openai_client=openai_client,
    )
