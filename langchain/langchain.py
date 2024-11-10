

























def get_langchain(langchain):
    """
    Get the language chain from the given language chain string.
    """
    return langchain.split('-')


def get_langchain_string(langchain):
    """
    Get the language chain string from the given language chain.
    """
    return '-'.join(langchain)

get_langchain_string(['en', 'us']) # 'en-us'