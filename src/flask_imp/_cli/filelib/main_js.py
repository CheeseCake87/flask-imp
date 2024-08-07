from pathlib import Path


def main_js(
    main_js_: Path,
) -> str:
    return f"""\
console.log('This log is from the file {main_js_}')
"""
