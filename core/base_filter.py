from sqlalchemy.sql import Select


class BaseFilter:
    def apply_on_query(self, query: Select) -> Select:
        return query
