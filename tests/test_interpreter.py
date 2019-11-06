from ghub.cliutils import Interpreter
from ghub.commands import EXIT
from ghub.ghubutils import GHub


class TestInterpreterClass:
    def test_intialization(self):
        interpreter = Interpreter()
        assert len(interpreter.registered_commands) == 7

    def test_register(self):
        interpreter = Interpreter()
        num_cmds = len(interpreter.registered_commands)
        interpreter.register(EXIT())
        assert (num_cmds + 1) == len(interpreter.registered_commands)

    def test_verify(self):
        interpreter = Interpreter()
        cv, av, cmd, args = interpreter.verify("cd repos")
        assert cv
        assert av
        cv, av, cmd, args = interpreter.verify("dummy repos")
        assert not cv
        assert not av
        cv, av, cmd, args = interpreter.verify("cd one two three")
        assert cv
        assert not av

    def test_execute(self):
        interpreter = Interpreter()
        ghub = GHub(fromenv=True)
        assert ghub.context.context == "root"
        interpreter.execute("cd repos", ghub)
        assert ghub.context.context == "repos"
        interpreter.execute("cd ghub", ghub)
        assert ghub.context.context == "repo"
        res = interpreter.execute("cat requirements.txt", ghub)
        assert res
        interpreter.execute("ls", ghub)
        interpreter.execute("cd", ghub)
        assert ghub.context.context == "root"
