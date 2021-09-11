from os import listdir, popen


def test_w_cli_help_string():
    result = str(popen('poetry run page-loader -h').read())
    assert '-o OUTPUT, --output OUTPUT' in result
    assert 'positional arguments:\n  link' in result
    assert 'debug,info,warning,error,critical' in result


def test_cli_log_w_err(tmpdir):
    popen('poetry run page-loader -o {0} http://badsite'.format(tmpdir)).read()
    assert not listdir(tmpdir)
