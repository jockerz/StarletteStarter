from starlette_babel import LazyString


def convert_lazy_string(data: dict | list | str):
    if isinstance(data, dict):
        return {
            key: convert_lazy_string(value) for key, value in data.items()
        }
    elif isinstance(data, list):
        return [convert_lazy_string(data)]
    elif isinstance(data, LazyString):
        # Convert LazyString
        return str(data)
    return data
