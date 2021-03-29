from clickcounter import providers
import secrets
import clickcounter
import sys
import argparse

import base64
import zlib
import logging
from tqdm import tqdm
logging.basicConfig(level=logging.INFO)


def encode_from_bytes(x):
    x = zlib.compress(x)
    x = base64.urlsafe_b64encode(x)
    return x.decode("utf-8").rstrip("=")


def decode_to_bytes(b64s):
    padding = 4 - (len(b64s) % 4)
    string = b64s + ("=" * padding)

    x = base64.urlsafe_b64decode(string)
    return zlib.decompress(x)


max_len = 1500
prefix = "https://www.example.com?q="
seperator = "_"
short_url_prefix = 'https://www.shorturl.at/'


def encode_bytes_to_url(b):
    s = encode_from_bytes(b)
    segments = [s[start:start+max_len] for start in range(0, len(s), max_len)]
    total_length = len(s)

    short_url_id = ""
    for segment in tqdm(reversed(segments), desc="encoding bytes to url", total=len(segments)):
        url = f"{prefix}{segment}{seperator}{total_length}{seperator}{short_url_id}"
        short_url = clickcounter.register_url(url)
        short_url_id = short_url.rsplit("/", 1)[1]
    return short_url_prefix+short_url_id


def url_to_bytes(url):
    session = clickcounter._default_provider_singleton.session
    buffer = ""
    with tqdm(desc="decoding url to bytes") as pbar:
        while True:
            response = session.get(url, allow_redirects=False)
            received_url = response.headers['Location']
            segment, total_length, next_id = received_url.split(
                prefix, 1)[1].rsplit(seperator, 2)

            segment = segment.replace('.', "")
            buffer += segment
            if not next_id:
                break

            url = short_url_prefix + next_id
            pbar.total = int(total_length)
            pbar.update(len(segment))

    return decode_to_bytes(buffer)


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "command", type=str, help="valid commands: encode, decode"
    )
    parser.add_argument(
        "input", type=str, help="filename or url"
    )
    args = parser.parse_args()
    if args.command == "encode":
        with open(args.input, "rb") as f:
            url = encode_bytes_to_url(f.read())
            print(url)
    elif args.command == "decode":
        bytes_out = url_to_bytes(args.input)
        sys.stdout.buffer.write(bytes_out)


if __name__ == "__main__":
    cli()
