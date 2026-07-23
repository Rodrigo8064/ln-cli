from ln_cli.commands import install_packages, install_packages_dev


def test_install_packages(mocker):
    mock_run = mocker.patch('ln_cli.commands.subprocess.run')
    install_packages(['requests', 'rich'], 'new_test')
    mock_run.assert_called_once_with(
        ['poetry', 'add', 'requests', 'rich'], cwd='new_test'
    )


def test_install_packages_dev(mocker):
    mock_run = mocker.patch('ln_cli.commands.subprocess.run')
    install_packages_dev(['taskpy', 'ruff'], 'new_test')
    mock_run.assert_called_once_with(
        ['poetry', 'add', '--group', 'dev', 'taskpy', 'ruff'], cwd='new_test'
    )
