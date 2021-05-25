import requests
from lesson1.parse5ka import Parse5ka, get_dir_path


class Parse5kaByCategories(Parse5ka):
    def _get_categories(self) -> list:
        categories_url = 'https://5ka.ru/api/v2/categories/'
        response = self._get_response(categories_url)
        return response.json()

    def _parse(self, url):
        categories = self._get_categories()
        for category in categories:
            goods_data = {
                'name': category['parent_group_name'],
                'code': category['parent_group_code'],
                'products': list()
            }

            params = {'categories': category['parent_group_code']}
            current_response = requests.get(self.start_url, headers=self.headers, params=params).json()
            goods_data['products'] = goods_data['products'] + current_response['results']

            while True:
                if not current_response['next']:
                    break
                else:
                    current_response = self._get_response(current_response['next']).json()
                    next_page_goods_data = current_response['results']
                    goods_data['products'] = goods_data['products'] + next_page_goods_data

            yield goods_data
            print(f"Товарная категория {category['parent_group_name']} обработана")

    def run(self):
        for goods_data in self._parse(self.start_url):
            file_name = f"{goods_data['code']}_{goods_data['name']}.json"
            file_path = self.save_dir.joinpath(file_name)
            self._save(goods_data, file_path)


if __name__ == '__main__':
    url = "https://5ka.ru/api/v2/special_offers/"
    save_dir = get_dir_path("products")
    parser = Parse5kaByCategories(url, save_dir)
    parser.run()
