import re
from markupsafe import escape
from slugify import slugify


def safe_str(text: str) -> str:
    regex = r"(?:<color.+?>(.+?)<\/color>|<(?:!|\/?[a-zA-Z]+).*?\/?>)"
    subst = "\\1"
    text = re.sub(regex, subst, text, 0, re.MULTILINE)
    return escape(text.strip())


def safe_tag(text: str, tag_name: str) -> str:
    tag_name = tag_name.replace("/", "")
    regex = f"(?:<{tag_name}.+?>(.+?)<\/{tag_name}>|<(?:!|\/?[a-zA-Z]+).*?\/?>)"
    regex = re.compile(regex, re.MULTILINE)
    subst = "\\1"
    text = re.sub(regex, subst, text, 0)
    return escape(text.strip())


def safe_name(text: str) -> str:
    text = text.strip()
    if not text:
        return ''

    regex = r"<(\/?[a-zA-Z0-9]+).*?\/?>"
    matches = re.finditer(regex, text, re.MULTILINE)
    VALID_TAGS = [
        "color",
        "/color",
        "b",
        "/b",
        "i",
        "/i",
    ]
    for m in matches:
        tag = m.group(1)
        if tag not in VALID_TAGS:
            text = safe_tag(text, tag)
    return text


def slug_html(text: str, max_length=60, separator="-"):
    text =  re.compile(r'<[^>]+>').sub("", text)
    return slugify(text, max_length=60, separator=separator)


if __name__ == "__main__":
    # test_cases = [
    #     "<color=#FF99FF>H</color><color=#FF99CC>U</color><color=#FF9999>Ấ</color><color=#FF9966>N</color>",
    #     "<color=#FF99FF>HU</a><color=#FF99CC>ẤN</a>",
    #     "<color=#16b6f0><b>Bỉ Ngạn</b></color>",
    #     "<color=#775BFF>F. <b>ᑎuage</b></color>",
    #     "<color=black><i>#CùiMía ᵁˢ </i></color>",
    #     "<b><color=#82cafa>Jeremie</color></b>",
    #     "<i><color=#FFCC00>NguyênIMT</color></i>",
    #     "<color=#FFFF00>Đ Ẹ T </color>",
    #     "<color=#6666FF>❥Hắc෴Quỷ✧</color>",
    #     "<color=#6666FF>❥Hắc෴Quỷ✧</color>",
    #     "<marquee>❥Hắc෴Quỷ✧</marquee>",
    #     "<h1>❥Hắc෴Quỷ✧</h1>",
    #     "❥Hắc෴Quỷ✧",
    #     "thỏ con 🐷🐷",
    #     "ภาสกร คนสูง",
    #     "Khoa Pham",
    # ]

    test_cases = [
        "Giày quân đội",
        "Giày quân đội",
        "Giày chạy nhẹ",
        "Giày chạy nhẹ",
        "Chân giả",
        "Giày trượt nhiều lớp",
        "Giày trượt nhiều lớp",
        "Ủng cao",
        "Ủng cao",
        "Ủng vĩnh cữu",
    ]

    # for text in test_cases:
    #     text = safe_name(text)
    #     print(text[:60])
    #     print("-" * 20)

    #     print(safe_str(text[:60]))
    #     print("-" * 20)

    # <[^>]*>

    for text in test_cases:
        # print(slugify(text, regex_pattern="<[^>]*>", max_length=60))
        print(slug_html(text, separator="_"))