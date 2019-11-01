from .githubutils import get_tree


def get_items_in_tree(ghub):
    items = []
    for i in ghub.context.cache["tree"]:
        items.append((i["path"], i["type"]))
    return items
