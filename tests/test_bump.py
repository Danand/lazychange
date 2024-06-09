import subprocess

from click.testing import CliRunner

from lazychange.cli import cli
from lazychange.llm.clients.client_test import ClientTest

def test_bump(dummy_git_repo):
    dummy_file_path = dummy_git_repo.join("dummy.txt")

    with open(dummy_file_path, "w") as file:
        file.write("This is a dummy file.")

    commit_msg_expected = "Make some changes"
    tag_expected = "0.1.1"

    ClientTest.enqueue_answer(commit_msg_expected)
    ClientTest.enqueue_answer(tag_expected)

    runner = CliRunner()

    result = runner.invoke(
        cli=cli,
        args=["bump", "--tags", "--llm", "test", "--repo", dummy_git_repo],
    )

    assert result.exit_code == 0, result.output

    process_last_tag = subprocess.run(
        args=["git", "-C", dummy_git_repo, "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
    )

    last_tagged_rev = process_last_tag.stdout.strip()

    process_describe = subprocess.run(
        args=["git", "-C", dummy_git_repo, "describe", "--tags", last_tagged_rev],
        capture_output=True,
        text=True,
    )

    tag_actual = process_describe.stdout.strip()

    assert tag_actual == tag_expected

    commit_msg_last = subprocess.run(
        ["git", "-C", dummy_git_repo, "log", "-1", "--pretty=%B"],
        capture_output=True,
        text=True,
    )

    commit_msg_actual = commit_msg_last.stdout.strip()

    assert commit_msg_actual == commit_msg_expected
