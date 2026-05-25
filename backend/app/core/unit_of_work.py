from sqlmodel import Session


class BaseUnitOfWork:
    """Base Unit of Work class that manages repositories"""

    def __init__(self, session: Session):
        self.session = session

    def commit(self) -> None:
        """Commit all changes"""
        self.session.commit()

    def rollback(self) -> None:
        """Rollback all changes"""
        self.session.rollback()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.rollback()
        else:
            self.commit()
