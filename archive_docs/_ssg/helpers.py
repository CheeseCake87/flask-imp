import re
from datetime import datetime
from pathlib import Path

from pytz import timezone

local_tz = timezone("Europe/London")


def pytz_dt_now() -> datetime:
    return datetime.now(local_tz)


def pytz_dt_epoch() -> float:
    return pytz_dt_now().timestamp()


def pytz_dt_now_str(mask: str = "%Y-%m-%d %H:%M:%S %z") -> str:
    return datetime.now(local_tz).strftime(mask)


def pytz_dt_to_str(pytz_dt: datetime, mask: str = "%Y-%m-%d %H:%M:%S %z") -> str:
    return pytz_dt.strftime(mask)


def pytz_dt_str_to_dt(pytz_dt_str: str) -> datetime:
    """
    :param pytz_dt_str: "2020-01-01 00:00:00 +0000"
    """
    return datetime.strptime(pytz_dt_str, "%Y-%m-%d %H:%M:%S %z")


def post_date(pytz_dt: datetime) -> str:
    return pytz_dt.strftime("%a, %d %b %Y")


def switch_date(content, new_date):
    pattern = re.compile(r'date="(.*?)"', re.IGNORECASE)
    return pattern.sub(f'date="{new_date}"', content)


def get_relative_files_in_the_docs_folder(docs_dir: Path) -> list:
    _ = []
    for f in docs_dir.glob("*.html"):
        if f.stem == "index":
            continue
        _.append(f.stem)

    return _


def excessive_br_cleanup(base_xml: str) -> str:
    return base_xml.replace("</p><br/>", "</p>").replace("<ol><br/>", "<ol>")
