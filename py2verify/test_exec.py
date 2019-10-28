def test_exec_statement(capsys):
    exec "print '%s' % v" in {"v": "foo"}

    captured = capsys.readouterr()
    assert "foo" in captured.out

def test_exec_function(capsys):
    exec("print '%s' % v", {"v": "foo"})

    captured = capsys.readouterr()
    assert "foo" in captured.out
