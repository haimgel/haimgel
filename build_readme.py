#!/usr/bin/env python3
import feedparser
import dateparser
import pathlib
import re

# This code has been shamelessly copied from https://github.com/simonw/simonw, see
# https://simonwillison.net/2020/Jul/10/self-updating-profile-readme/ for more info.


def replace_chunk(content, marker, chunk):
    r = re.compile(
        r"<!\-\- {} starts \-\->.*<!\-\- {} ends \-\->".format(marker, marker),
        re.DOTALL,
    )
    chunk = "<!-- {} starts -->\n{}\n<!-- {} ends -->".format(marker, chunk, marker)
    return r.sub(chunk, content)


def fetch_blog_entries():
    entries = feedparser.parse("https://haim.dev/index.xml")["entries"]
    return [
        {
            "title": entry["title"],
            "url": entry["link"].split("#")[0],
            "published": dateparser.parse(entry["published"]).strftime("%Y-%m-%d"),
        }
        for entry in entries
    ]


def main():
    root = pathlib.Path(__file__).parent.resolve()
    readme = root / "README.md"
    readme_contents = readme.open().read()
    entries = fetch_blog_entries()[:5]
    entries_md = "\n".join(
        ["* [{title}]({url}) - {published}".format(**entry) for entry in entries]
    )
    rewritten = replace_chunk(readme_contents, "blog", entries_md)
    readme.open("w").write(rewritten)


if __name__ == "__main__":
    main()
