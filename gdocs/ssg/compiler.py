import re
import typing as t
from pathlib import Path

import mistune
from flask import render_template

from .exceptions import NoPostDefinition
from .helpers import get_relative_files_in_the_docs_folder, pytz_dt_now, post_date
from .render_engines import HighlightRenderer


def _raw_markdown_processor(raw_markdown: str) -> tuple[t.Optional[list], str, str]:
    """
    :param raw_markdown: The raw markdown to process
    :return: publish: bool, date: str, title: str, description: str, post: str
    """
    if not raw_markdown.startswith("```"):
        raise NoPostDefinition

    split_md = raw_markdown.split("```")[1:]
    raw_meta = split_md[0]

    menu_ptn = re.compile(r"Menu =(.*?)\n", re.IGNORECASE)
    title_ptn = re.compile(r"Title =(.*?)\n", re.IGNORECASE)

    try:
        menu = menu_ptn.findall(raw_meta)[0].strip().split("/")
    except (ValueError, IndexError, TypeError) as _:
        menu = None

    try:
        title = title_ptn.findall(raw_meta)[0].strip()
    except (ValueError, IndexError, TypeError) as _:
        title = "[Unable to find Title]"

    try:
        post = "```".join(split_md[1:])
    except (IndexError, TypeError, ValueError) as _:
        post = "[Unable to find Post]"

    return menu, title, post


def replace_post_date(content: str, new_date: str) -> str:
    date_ptn = re.compile(r"Date =(.*?)\n", re.IGNORECASE)
    return content.replace(date_ptn.findall(content)[0], f" {new_date}")


def compiler(docs_dir: Path, markdown_dir: Path):
    docs_dir.mkdir(exist_ok=True)
    markdown_dir.mkdir(exist_ok=True)

    markdown_menu = markdown_dir / "__menu__.md"
    markdown_index = markdown_dir / "__index__.md"

    markdown_menu_dict = dict()

    with open(markdown_menu, mode="r") as menu_file:
        for line in menu_file.readlines():
            if line.startswith("-"):
                line_strip = line.strip()
                markdown_menu_dict[line_strip.replace("- ", "").strip()] = {
                    "page": "",
                    "pages": [],
                }
                continue

            if line.startswith(" ") or line.startswith("\t"):
                line_strip = line.strip()
                if line_strip.startswith("-"):
                    markdown_menu_dict[list(markdown_menu_dict.keys())[-1]][
                        "pages"
                    ].append({line_strip.replace("- ", "").strip(): ""})

    index_html = docs_dir / "index.html"

    docs_dir_files = get_relative_files_in_the_docs_folder(docs_dir)
    markdown_dir_files = markdown_dir.glob("*.md")
    html_engine = mistune.create_markdown(renderer=HighlightRenderer())

    html_pages = dict()
    dt_date = pytz_dt_now()

    for file in docs_dir_files:
        (docs_dir / f"{file}.html").unlink()

    for file in markdown_dir_files:
        if "__" in file.stem:
            continue

        raw_markdown = file.read_text()
        menu, title, post = _raw_markdown_processor(raw_markdown)
        html_filename = f'{file.stem.lower().replace(" ", "_")}.html'

        html_pages[html_filename] = {
            "menu": menu,
            "title": title,
            "content": html_engine(post),
        }

        if menu is not None:
            if len(menu) == 1:
                markdown_menu_dict[menu[0]]["page"] = html_filename
            else:
                for keys in markdown_menu_dict[menu[0]]["pages"]:
                    if menu[1] in keys.keys():
                        keys[menu[1]] = html_filename

    # write html files
    for page, meta in html_pages.items():
        with open(docs_dir / page, mode="w") as html_file:
            html_file.write(
                render_template(
                    "__main__.html",
                    menu=markdown_menu_dict,
                    title=meta["title"],
                    date=post_date(dt_date),
                    content=meta["content"],
                )
            )

    # write main index.html
    index_html.write_text(
        render_template(
            "index.html",
            menu=markdown_menu_dict,
            date=post_date(dt_date),
            index=html_engine(markdown_index.read_text()),
        )
    )
