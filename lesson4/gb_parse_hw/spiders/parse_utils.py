from urllib.parse import unquote
from base64 import b64decode
import re


def get_author_info(response):
    marker = "window.transitState = decodeURIComponent"
    id_pattern = re.compile(r"(\"youlaId\"),\"([a-zA-z|\d]+)")
    phone_pattern = re.compile(r"(\"phone\"),(\"[a-zA-Z0-9]+==\")")
    author_id = ''

    for script in response.css("script"):
        try:
            script_str = script.css("::text").extract_first()
            if marker in script_str:
                decoded_script_str = unquote(script_str, errors='replace')
                author_id_list = re.findall(id_pattern, decoded_script_str)
                phone = re.search(phone_pattern, decoded_script_str)
                if author_id_list and len(author_id_list) == 2:
                    author_id = author_id_list[1][1]
                if phone:
                    phone = phone.group(2)

                return (
                    response.urljoin(f"/user/{author_id}").replace("auto.", "", 1) if author_id else None,
                    b64decode(b64decode(phone)).decode('utf-8') if phone else None
                )
        except TypeError:
            continue

