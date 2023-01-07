from sqlalchemy.exc import SQLAlchemyError


class ConflictError(SQLAlchemyError):
    pass


class VersionConflictError(ConflictError):
    pass
