from .githubutils import get_tree, get_blob
from base64 import b64decode


def get_items_in_tree(ghub):
    items = []
    for i in ghub.context.cache["tree"]:
        items.append((i["path"], i["type"]))
    return items


def get_blob_content(ghub, blob_url):
    response = get_blob(ghub, blob_url)
    content = response["content"]
    content = b64decode(content).decode("utf-8")
    return content
