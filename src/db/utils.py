from .conn import Base, engine

_all_tables_created = False

def db_method(f):
    """
    Decorator for DB related methods.
    Creates the tables if they don't exist
    before executing the method itself.
    """
    def wrapper(*args, **kwargs):
        global _all_tables_created
        if not _all_tables_created:
            Base.metadata.create_all(engine)
            _all_tables_created = True
        res = f(*args, **kwargs)
        if not res:
            return res
        return [dict(row) for row in res]
    return wrapper
