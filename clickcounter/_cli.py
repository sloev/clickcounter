from clickcounter import providers
import argparse
import logging
import json

logging.basicConfig(level=logging.INFO)


_VALID_COMMANDS = ["register", "get", "getall"]


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "command", type=str, help="valid commands: " + ", ".join(_VALID_COMMANDS)
    )
    parser.add_argument(
        "--provider", default="shorturl.at", type=str, help="defaults to shorturl.at"
    )
    parser.add_argument(
        "--username", default=None, type=str, help="some providers require login"
    )
    parser.add_argument(
        "--password", default=None, type=str, help="some providers require login"
    )
    parser.add_argument("--url", default=None, type=str, help="used during register")
    parser.add_argument("--trackurl", default=None, type=str, help="used during get")
    try:
        args = parser.parse_args()

        provider = providers.get(args.provider)
        if provider is None:
            logging.error(
                f"unsupported provider: '{args.provider}', valid providers: {list(providers.keys())}"
            )
            exit(1)
        provider = provider()
        provider.login(args.username, args.password)

        if args.command == "register":
            track_url = provider.register_url(args.url)
            print(track_url)

        elif args.command == "get":
            track_url_count = provider.get_visits(args.trackurl)
            print(track_url_count)

        elif args.command == "getall":
            track_url_counts = provider.get_all_visits()
            print(json.dumps(track_url_counts))
        else:
            logging.error(
                f"unsupported command: '{args.command}', valid commands: {_VALID_COMMANDS}"
            )
            exit(1)
    except:
        parser.print_help()
        raise


if __name__ == "__main__":
    cli()
