from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base

class DbInteraction:
    db = create_engine('sqlite:///book.db')
    Session = sessionmaker(db)
    session = Session()
    Base = declarative_base()



    class Book(Base):
        __tablename__ = 'books'

        id = Column( Integer, primary_key=True, autoincrement=True)
        title = Column( String(100), nullable=False)
        author = Column(String(100), nullable=False)
        year = Column(Integer, nullable=False)
        stock = Column(Integer, nullable=False)

        def __init__(self, title, author, year, stock):
            self.title = title
            self.author = author
            self.year = year
            self.stock = stock
            DbInteraction.create_base()

    class User(Base):
        __tablename__ = 'users'
        id = Column(Integer, primary_key=True, autoincrement=True)
        name = Column(String(100), nullable=False)
        email = Column(String(100), nullable=False)

        def __init__(self, name, email):
            self.name = name
            self.email = email
            DbInteraction.create_base()
    class Leased(Base):
        __tablename__ = 'leased'

        rental_id = Column(Integer, primary_key=True, autoincrement=True)
        owner_id = Column(Integer, ForeignKey('users.id'))
        book_id = Column(Integer, ForeignKey('books.id'))
        amount = Column(Integer, nullable=False)
        acquisition = Column(Integer, nullable=False)
        return_date = Column(Integer, nullable=False)
        status = Column(Boolean, nullable=False)

        def __init__(self, amount, owner_id, book_id, acquisition, return_date, status):
            self.amount = amount
            self.owner_id = owner_id
            self.book_id = book_id
            self.acquisition = acquisition
            self.return_date = return_date
            self.status = status
            DbInteraction.create_base()

    @staticmethod
    def create_base():
        DbInteraction.Base.metadata.create_all(bind=DbInteraction.db)

    Base.metadata.create_all(bind=db)
