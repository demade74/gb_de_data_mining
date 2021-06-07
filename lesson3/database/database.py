from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from . import models


class Database:
    def __init__(self, db_url):
        engine = create_engine(db_url)
        models.Base.metadata.create_all(bind=engine)
        self.maker = sessionmaker(bind=engine)

    def get_or_create(self, session, model, filter_field, data):
        instance = (
            session.query(model).filter(getattr(model, filter_field) == data[filter_field]).first()
        )
        if not instance:
            instance = model(**data)
        return instance

    def add_comments(self, session, data):
        post_id = data['post_data']['id']
        comments = data['comments']

        while True:
            try:
                comment = comments.pop(0)
            except IndexError:
                break

            comment_author = {
                'name': comment['comment']['user']['full_name'],
                'url': comment['comment']['user']['url']
            }
            author = self.get_or_create(session, models.Author, 'url', comment_author)
            comment_to_db = self.get_or_create(session, models.Comment, 'id', comment['comment'])
            comment_to_db.author = author
            comment_to_db.post_id = post_id
            session.add(comment_to_db)
            comments.extend(comment['comment']['children'])

    def add_post(self, data):
        session = self.maker()
        post = self.get_or_create(session, models.Post, "id", data["post_data"])
        author = self.get_or_create(session, models.Author, "url", data["author_data"])
        post.tags.extend(
            [
                self.get_or_create(session, models.Tag, "url", tag_data)
                for tag_data in data['tags_data']
            ]
        )
        post.author = author
        session.add(post)
        self.add_comments(session, data)
        try:
            session.commit()
        except Exception:
            session.rollback()
        finally:
            session.close()
