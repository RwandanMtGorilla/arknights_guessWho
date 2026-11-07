from contextlib import contextmanager
from pathlib import Path
from tempfile import NamedTemporaryFile

from downloader import download_all_avatars
from extract import extract_operators_info, save_operators_to_json
from request_prts import fetch_operators_html, save_html


@contextmanager
def staged_file(project_dir, suffix):
    with NamedTemporaryFile(dir=project_dir, suffix=suffix, delete=False) as file:
        path = Path(file.name)
    try:
        yield path
    finally:
        path.unlink(missing_ok=True)


def main():
    project_dir = Path(__file__).resolve().parent
    try:
        with staged_file(project_dir, ".html") as html_file, staged_file(project_dir, ".json") as json_file:
            print("[1/3] 获取 PRTS 干员一览")
            html = fetch_operators_html()
            if not html or not save_html(html, html_file):
                print("更新失败：无法获取或保存干员一览页面。")
                return 1

            print("[2/3] 提取干员数据")
            operators = extract_operators_info(html_file)
            if len(operators) < 30:
                print(f"更新失败：仅提取到 {len(operators)} 名干员，游戏开局需要至少 30 名。")
                return 1
            save_operators_to_json(operators, json_file)

            print("[3/3] 下载缺少的干员头像")
            if not download_all_avatars(json_file, project_dir / "avatars"):
                print("更新失败：有头像未下载成功。可重新运行以补齐缺少的头像。")
                return 1

            html_file.replace(project_dir / "input.html")
            json_file.replace(project_dir / "operators_data.json")
    except OSError as error:
        print(f"更新失败：{error}")
        return 1

    print(f"更新完成，共 {len(operators)} 名干员。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
