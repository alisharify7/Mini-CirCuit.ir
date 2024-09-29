import json

import sqlalchemy as sa
import sqlalchemy.orm as so

from Core.model import BaseModel
from Auth.model import User


class OrderTypes(BaseModel):
    """Order Types"""

    __tablename__ = BaseModel.SetTableName("order-types")
    Name: so.Mapped[str] = so.mapped_column(
        sa.String(126), nullable=False, unique=True, index=True
    )
    Orders = so.relationship("Order", backref="Type", lazy="dynamic")

    TYPES = {
        "buy-aboard": "خرید از خارچ",
        "pcb": "سفارش مدار چاپی",
    }

    @classmethod
    def get_order(cls, type: str):
        """get order type if not exists in db create it and return its id"""
        if not type in cls.TYPES:
            raise RuntimeError("invalid type is passed for orders,\n")

        if not (T := cls.query.filter_by(Name=type).first()):
            T = cls()
            T.NAME = type
            T.SetPublicKey()
            T.save()
            return T.id
        else:
            return T.id


class Order(BaseModel):
    """Orders"""

    __tablename__ = BaseModel.SetTableName("orders")

    Name: so.Mapped[str] = so.mapped_column(
        sa.String(512), nullable=False, unique=False
    )
    Description: so.Mapped[str] = so.mapped_column(
        sa.String(4096), nullable=True, unique=False
    )

    Attr: so.Mapped[str] = so.mapped_column(
        sa.JSON, unique=False, nullable=False, default=json.dumps([])
    )
    Files: so.Mapped[str] = so.mapped_column(
        sa.JSON, unique=False, nullable=True, default=json.dumps([])
    )

    UserID: so.Mapped[int] = so.mapped_column(
        sa.Integer, sa.ForeignKey(User.id), nullable=False
    )
    TypeID: so.Mapped[int] = so.mapped_column(
        sa.Integer, sa.ForeignKey(OrderTypes.id), nullable=False
    )
    PaymentStatus: so.Mapped[bool] = so.mapped_column(
        sa.Boolean, nullable=False, default=False, unique=False
    )

    ORDER_STATUS = {
        "processing": "در حال پردازش",
        "ready-for-sending": "آماده ارسال",
        "send-by-post": "ارسال توسط پست",
        "stopped": "متوقف شده",
        "complete": "اتمام یافته",
    }
    ORDER_STATUS_KEYS = list(ORDER_STATUS.keys())

    Status: so.Mapped[str] = so.mapped_column(
        sa.String(512), nullable=False, unique=False, default=ORDER_STATUS_KEYS[0]
    )

    Messages = so.relationship("OrderMessages", backref="Order", lazy="dynamic")

    def is_complete(self):
        return self.Status == Order.ORDER_STATUS_KEYS[-1]

    def is_stopped(self):
        return self.Status == Order.ORDER_STATUS_KEYS[-2]

    def set_files(self, files: list):
        self.Files = json.dumps(files)

    def append_to_files(self, file):
        self.Files = json.dumps(json.loads(self.Files).extend([file]))

    def get_files(self):
        return json.loads(self.Files)


class OrderMessages(BaseModel):
    __tablename__ = BaseModel.SetTableName("order-messages")
    Messages: so.Mapped[str] = so.mapped_column(
        sa.String(2096), unique=False, nullable=False
    )

    Files: so.Mapped[str] = so.mapped_column(
        sa.JSON, unique=False, nullable=True, default=json.dumps([])
    )

    OrderID: so.Mapped[int] = so.mapped_column(
        sa.Integer, sa.ForeignKey(Order.id), nullable=False
    )
    is_admin: so.Mapped[bool] = so.mapped_column(
        sa.Boolean, nullable=False, unique=False, default=False
    )
    Seen: so.Mapped[bool] = so.mapped_column(
        sa.Boolean, nullable=False, unique=False, default=False
    )

    def set_files(self, files: list):
        self.Files = json.dumps(files)

    def append_to_files(self, file):
        self.Files = json.dumps(json.loads(self.Files).extend([file]))

    def get_files(self):
        return json.loads(self.Files)
