from sqlalchemy.orm.exc import NoResultFound


class NotFoundError(NoResultFound):
    pass
