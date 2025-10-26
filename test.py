from click.testing import CliRunner
from cyclone_cli import peer

# testing peer group
def test_cmd():
    runner = CliRunner()
    result = runner.invoke(peer, "list")
    print(result)

test_cmd()