import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# .envがあったらload_dotenv()を実行
if os.path.exists(".env"):
    from dotenv import load_dotenv

    load_dotenv()

DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}"

Base = declarative_base()


class PullRequest(Base):
    __tablename__ = "pull_requests"

    id = Column(Integer, primary_key=True)
    repository = Column(String)
    number = Column(Integer)
    title = Column(String)
    assignee = Column(String)
    target_branch = Column(String)
    source_branch = Column(String)
    first_commit_at = Column(DateTime)
    merged_at = Column(DateTime)
    num_commits = Column(Integer)


class Comment(Base):
    __tablename__ = "comments"

    comment_id = Column(Integer, primary_key=True)
    assignee = Column(String)
    commenter = Column(String)
    body = Column(String)
    created_at = Column(DateTime)
    pull_id = Column(Integer)


def connect_db():
    # エンジンの作成
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)

    # セッションの作成
    Session = sessionmaker(bind=engine)
    session = Session()

    print("Connected to the database.")
    return session
