def row_to_dict(f):
    def wrapper(*args, **kwargs):
        res = f(*args, **kwargs)
        try:
            return [
                {
                    k: v
                    for k, v in row.__dict__.items()
                    if k != "_sa_instance_state"
                }
                for row in res
            ]
        except AttributeError:
            return [
                {
                    k: v
                    for k, v in dict(row).items()
                    if k != "_sa_instance_state"
                }
                for row in res
            ]
        raise RuntimeError("Unexpected error parsing result rows")
    return wrapper
