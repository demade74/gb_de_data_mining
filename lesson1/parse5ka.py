from pathlib import Path
import json
import time
import requests


class Parse5ka:
    headers = {"User-Agent": "Philipp Kirkorov"}

    def __init__(self, start_url: str, save_dir: Path):
        self.start_url = start_url
        self.save_dir = save_dir

    def _get_response(self, url: str) -> requests.Response:
        while True:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response
            time.sleep(0.2)

    def run(self):
        for product in self._parse(self.start_url):
            file_name = f"{product['id']}.json"
            file_path = self.save_dir.joinpath(file_name)
            self._save(product, file_path)

    def _parse(self, url):
        while url:
            response = self._get_response(url)
            data = response.json()
            url = data["next"]
            for product in data["results"]:
                yield product

    def _save(self, data: dict, file_path: Path):
        file_path.write_text(json.dumps(data, ensure_ascii=False))


def get_dir_path(dir_name: str) -> Path:
    dir_path = Path(__file__).parent.joinpath(dir_name)
    if not dir_path.exists():
        dir_path.mkdir()
    return dir_path


if __name__ == "__main__":
    url = "https://5ka.ru/api/v2/special_offers/"
    save_dir = get_dir_path("products")
    parser = Parse5ka(url, save_dir)
    parser.run()
