import click
import git

from ..llm.client_factory import get_llm_client
from ..llm.client_base import ClientBase

def get_commit_message(
    diff: str,
    model: str,
    llm_client: ClientBase,
) -> str:
    if len(diff) == 0:
        raise click.ClickException("Diff is empty!")

    content = "Generate a brief commit message (title only)" \
              "for the following changes, wrap some names in backticks if needed " \
              "(mentions of git branches, packages, classes, functions, keywords)" \
              f":\n```diff\n{diff}\n```"

    return llm_client.get_simple_answer(
        content=content,
        model=model,
    )

def get_new_tag(
    repo: git.Repo,
    model: str,
    llm_client: ClientBase,
) -> str:
    previous_tag = repo.git.describe("--tags", "--abbrev=0")

    content = "Detect versioning style, increment version, and answer with result only, " \
              "ready for tagging (without descriptions and explanations). " \
              f"Current version: {previous_tag}"

    return llm_client.get_simple_answer(
        content=content,
        model=model,
    )

def run_bump(
    is_need_push_tags: bool,
    is_dry_run: bool,
    repo_path: str,
    model: str,
    llm_client: ClientBase,
) -> None:
    repo = git.Repo(repo_path)

    repo.git.add(A=True)

    diff = repo.git.diff("HEAD")

    message = get_commit_message(
        diff=diff,
        model=model,
        llm_client=llm_client,
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
            llm_client=llm_client,
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
    "--llm",
    default="openai",
    help="LLM service.",
)
@click.option(
    "--model",
    default="gpt-4o",
    help="LLM model to use for generating messages.",
)
@click.option(
    "--api-key",
    default=None,
    help="LLM service API key.",
)
def bump(
    dry_run: bool,
    tags: bool,
    repo: str,
    llm: str,
    model: str,
    api_key: str | None,
) -> None:
    llm_client = get_llm_client(
        llm= llm,
        api_key=api_key,
    )

    run_bump(
        is_need_push_tags=tags,
        is_dry_run=dry_run,
        repo_path=repo,
        model=model,
        llm_client=llm_client,
    )
