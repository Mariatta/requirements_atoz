# Python 3.7
import os
import sys
from argparse import ArgumentParser


def sort_entries(path, apply):
    if not os.path.exists(path):
        print(f"{path} doesn't exist")
        sys.exit(-1)
    comments = []
    entries = []
    print(f"found requirements file {path}")
    with open(path) as file:
        entries = [entry.strip() for entry in file.readlines()]

    for index, entry in enumerate(entries):
        if entry.startswith('#'):
            comment_dict = {
                'comment_text': entry,
                'comment_for': entries[index+1],
                'comment_index': index}
            comments.append(comment_dict)

    for comment_dict in comments:
        entries.pop(comment_dict['comment_index'])

    sorted_entries = sorted(entries, key=lambda s: s.lower())
    for comment_dict in comments:
        entry_index = sorted_entries.index(comment_dict['comment_for'])
        sorted_entries.insert(entry_index, comment_dict['comment_text'])

    print("sorted entries:")
    for s in sorted_entries:
        print(s)

    if apply:
        print(f"Will rewrite {path} with the sorted entries")
        with open(path, 'w+') as file:
            for entry in sorted_entries:
                file.write(f"{entry}{os.linesep}")
        print(f"Done! {path} updated.")


if __name__ == '__main__':
    parser = ArgumentParser(
        description="sort requirements alphabetically")

    parser.add_argument("path")
    parser.add_argument('-a', '--apply', action='store_true')
    args = parser.parse_args()
    sort_entries(args.path, args.apply)
