import json
import secrets

import sqlalchemy as sa
import sqlalchemy.orm as so

from Core.model import BaseModel
from Core.extensions import db
from Core.utils import generate_random_string
from Admin.model import Admin


class Tag(BaseModel):
    __tablename__ = BaseModel.SetTableName("tags")

    @staticmethod
    def add_Tag(tag: str):
        tag = Tag(tag)
        return tag.save()

    def __init__(self, tag: str = "", *args, **kwargs):
        content = super(*args, **kwargs).__init__()
        if tag:
            self.Name = tag

        return content

    Name: so.Mapped[str] = so.mapped_column(sa.String(512), nullable=False, unique=True)


Post2Tag = db.Table(
    BaseModel.SetTableName("posts2tags"),
    sa.Column(
        "PostID", sa.Integer, sa.ForeignKey(BaseModel.SetTableName("posts") + ".id")
    ),
    sa.Column("TagID", sa.Integer, sa.ForeignKey(Tag.id)),
)


class Post(BaseModel):
    __tablename__ = BaseModel.SetTableName("posts")

    AuthorID: so.Mapped[int] = so.mapped_column(
        sa.Integer, sa.ForeignKey(Admin.id), nullable=False, unique=False
    )  # writer -> admin
    Title: so.Mapped[str] = so.mapped_column(
        sa.String(512), nullable=False, unique=True, index=True
    )
    Content: so.Mapped[str] = so.mapped_column(sa.Text, nullable=False, unique=False)
    Images: so.Mapped[str] = so.mapped_column(
        sa.JSON, nullable=False, unique=False, default=json.dumps([])
    )
    Slug: so.Mapped[str] = so.mapped_column(
        sa.String(256), nullable=False, unique=True, index=True
    )  # short url

    ShortIntro: so.Mapped[str] = so.mapped_column(sa.Text, unique=False, nullable=False)
    ReadingTime: so.Mapped[int] = so.mapped_column(
        sa.Integer, nullable=False, unique=False, default=lambda: secrets.randbits(k=5)
    )

    Tags = so.relationship("Tag", secondary=Post2Tag, backref="GetPost", lazy="dynamic")

    def setSlug(self, slug_length: int = 6) -> bool:
        """Set unique slug for post"""
        counter = 0
        while True:
            if counter == 100:
                return False

            counter += 1
            slug = generate_random_string(slug_length)
            query = db.select(Post).filter(Post.Slug == slug)

            if not db.session.execute(query).scalar_one_or_none():
                self.Slug = slug
                return True

    def set_images(self, images: list):
        self.Images = json.dumps(images)

    def append_to_images(self, image):
        images = self.get_images()
        images.extend([image])
        self.set_images(images)

    def get_image_at(self, index: int) -> str:
        """return post image base of index"""
        images = self.get_images()
        if len(images) <= index:  # no image
            return "No-image-Found"

        return images[index]

    def get_images(self):
        """return all images"""
        return json.loads(self.Images)

    def make_url(self):
        """make blog url title link"""
        return self.Title.replace(" ", "-").replace(" ", "")

    def get_tags(self):
        """"""
        # TODO: replace it with generator because its used in template with for loop
        tags = [each.Name for each in self.Tags]
        return tags

    def to_dict(self):
        return {
            "title": self.Title,
            "slug": self.Slug,
            "title-url": self.Title.replace(" ", "-"),
            "short-intro": self.ShortIntro,
        }
