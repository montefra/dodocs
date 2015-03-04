"""Main function"""

from dodocs.cmdline import parse


def main():
    """
    Main code
    """
    args = parse()

    if args.subparser_name is None:
        raise ValueError("No command provided")
    elif args.subparser_name == "create":
        import dodocs.pyvenvex as pyenv
        pyenv.create_venv(args)
