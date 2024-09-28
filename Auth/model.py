import enum
import json

import sqlalchemy as sa
import sqlalchemy.orm as so

from werkzeug.security import generate_password_hash, check_password_hash

from Core.extensions import db
from Core.model import BaseModel



class User(BaseModel):
    """
        Users Model Table
    """
    __tablename__ = BaseModel.SetTableName("users")
    FirstName: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=True, unique=False)
    LastName: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=True, unique=False)

    Username: so.Mapped[str] = so.mapped_column(sa.String(128), nullable=False, unique=True)
    Password: so.Mapped[str] = so.mapped_column(sa.String(162), nullable=False, unique=True)
    Email: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=False, unique=True)

    Address: so.Mapped[str] = so.mapped_column(sa.String(2048), nullable=True, unique=False)
    PhoneNumber: so.Mapped[str] = so.mapped_column(sa.String(14), nullable=True, unique=True)

    Active: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False, nullable=False, unique=False)


    Tickets = db.relationship("Ticket", backref="User", lazy="dynamic")
    Orders = db.relationship("Order", backref="User", lazy="dynamic")

    def to_dict(self):
        return {
            "Username": self.Username,
            "FirstName": self.FirstName or "NULL",
            "LastName": self.LastName or "NULL",
            "Address": self.Address or "NULL",
            "Email": self.Email,
            "PublicKey": self.PublicKey,
            "Status": "Active" if self.Active else "inactive",
            "CreatedTime": self.CreatedTime
        }

    def getName(self, unique=False):
        """This Method Return Users Full name <f,l>"""
        if unique:
            return f"{self.FirstName} {self.LastName} - {self.PublicKey}"

        return f"{self.FirstName} {self.LastName}"

    def setPassword(self, password: str) -> None:
        self.Password = generate_password_hash(password, method="scrypt")

    def checkPassword(self, password: str) -> bool:
        return check_password_hash(pwhash=self.Password, password=password)

    def setUsername(self, username: str) -> bool:
        if db.session.execute(db.select(User).filter_by(Username=username)).scalar_one_or_none():
            return False
        else:
            self.Username = username
            return True

    def setPhonenumber(self, phone: str) -> bool:
        if db.session.execute(db.select(User).filter_by(PhoneNumber=phone)).scalar_one_or_none():
            return False
        else:
            self.PhoneNumber = phone
            return True

    def setEmail(self, email: str) -> bool:
        if db.session.execute(db.select(User).filter_by(Email=email)).scalar_one_or_none():
            return False
        else:
            self.Email = email
            return True

    def setActivate(self):
        self.Active = True




class StenCilOrder(BaseModel):
    __tablename__ = BaseModel.SetTableName("stencil-orders")

    def fill_from_form(self, form):
        self.Type = form.TYPE.data
        self.Size = form.SIZE.data
        self.Side = form.SIDE.data
        self.Quantity = form.QUANTITY.data
        self.Thickness = form.THICKNESS.data
        self.Fiducials = form.FIDUCIALS.data
        self.OtherRequest = form.REQUEST.data
        self.File = form.FILE.data if form.FILE.data else None

    class EnumBases(enum.Enum):
        @classmethod
        def has_value(cls, value):
            return value in cls._value2member_map_

    class StenCilTypes(EnumBases):
        FRAMEWORK = "FRAMEWORK"
        NON_FRAMEWORK = "NON_FRAMEWORK"

    Type:so.Mapped[str] = so.mapped_column(sa.String(256), unique=False, nullable=False)
    @so.validates("Type")
    def validate_type(self, key, value):
        if self.StenCilTypes.has_value(value):
            return value
        else:
            raise ValueError("invalid stencil type ")


    class StenCilSizes(EnumBases):
        FRAMEWORK_37X47 = "FRAMEWORK_37X47"
        FRAMEWORK_42X52 = "FRAMEWORK_42X52"
        FRAMEWORK_55X65 = "FRAMEWORK_55X65"
        FRAMEWORK_73_6X73_6 = "FRAMEWORK_73.6x73.6"

        NON_FRAMEWORK_28x38 = "NON_FRAMEWORK_28X38"
        NON_FRAMEWORK_32x42 = "NON_FRAMEWORK_32X42"
        NON_FRAMEWORK_44x54 = "NON_FRAMEWORK_44X54"
        NON_FRAMEWORK_60x60 = "NON_FRAMEWORK_60X60"

    Size: so.Mapped[str] = so.mapped_column(sa.String(256), unique=False, nullable=False)
    @so.validates("Size")
    def validate_size(self, key, value):
        if self.StenCilSizes.has_value(value):
            return value
        else:
            raise ValueError("invalid stencil size")

    class StenCilSides(EnumBases):
        TOP = "TOP"
        BOTTOM = "BOTTOM"
        TOP_PLUS_BOTTOM = "TOP + BOTTOM"
        TOP_AND_BOTTOM = "TOP & BOTTOM"

    Side: so.Mapped[str] = so.mapped_column(sa.String(256), unique=False, nullable=False)
    @so.validates("Side")
    def validate_side(self, key, value):
        if self.StenCilSides.has_value(value):
            return value
        else:
            raise ValueError("invalid stencil side")


    Quantity: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False, unique=False)
    @so.validates("Quantity")
    def validate_quantity(self, key, value):
        """quantity between 0-100"""
        if (10001 > value >= 0):
           return value
        else:
            raise ValueError("quantity must between 0-100")

    class StenCilThickness(EnumBases):
        SIZE_0_08 = "0.08MM"
        SIZE_0_10 = "0.10MM"
        SIZE_0_12 = "0.12MM"
        SIZE_0_15 = "0.15MM"

        SIZE_0_2 = "0.2MM"
        SIZE_0_3 = "0.3MM"
        SIZE_0_25 = "0.25MM"

    Thickness: so.Mapped[str] = so.mapped_column(sa.String(256), unique=False, nullable=False)
    @so.validates("Thickness")
    def validate_thickness(self, key, value):
        if self.StenCilThickness.has_value(value):
            return value
        else:
            raise ValueError("invalid stencil Thickness")


    class StenCilFiducials(EnumBases):
        NONE = "NONE"
        HALF_LASERED = "HALF_LASERED"
        LASRRED_THOUGH = "LASRRED_THOUGH"

    Fiducials: so.Mapped[str] = so.mapped_column(sa.String(256), unique=False, nullable=False)
    @so.validates("Fiducials")
    def validate_fiducials(self, key, value):
        if self.StenCilFiducials.has_value(value):
            return value
        else:
            raise ValueError("invalid stencil Fiducials")


    STATUS_ENUM = {
        "cancelled": "لغو شده",
        "completed": "تکمیل شده",
        "progressing": "در حال پردازش",
        "waited for accepted": "در انتظار تایید",
    }

    Status: so.Mapped[str] = so.mapped_column(sa.String(256), unique=False, nullable=False, default=list(STATUS_ENUM.keys())[2])
    @so.validates("Status")
    def validate_status(self, key, value):
        if value not in self.STATUS_ENUM:
            raise ValueError("invalid key passed")
        return value

    def get_status(self):
        """Return Persian status of order, uses in templates"""
        return self.STATUS_ENUM.get(self.Status, "NULL")




    OtherRequest: so.Mapped[str] = so.mapped_column(sa.String(2048), nullable=True, unique=False)
    File: so.Mapped[str] = so.mapped_column(sa.JSON, unique=False, nullable=True, default=json.dumps([]))
    Address: so.Mapped[str] = so.mapped_column(sa.String(2048), nullable=False, unique=False)


    UserID: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey(User.id), unique=False, nullable=False)





class Ticket(BaseModel):
    __tablename__ = BaseModel.SetTableName("tickets")
    Title: so.Mapped[str] = so.mapped_column(sa.String(64), nullable=False, unique=False)
    Caption: so.Mapped[str] = so.mapped_column(sa.String(512), nullable=False, unique=False)
    Status: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)
    File: so.Mapped[str] = so.mapped_column(sa.String(1024), unique=True, nullable=True)

    UserID: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey(User.id), nullable=False, unique=False)
    Answer = db.relationship("AnswerTicket", backref="GetTicket", lazy=True)

    def setTitle(self, title: str) -> None:
        self.Title = title

    def setCaption(self, caption: str) -> None:
        self.Caption = caption

    def setUserID(self, user: User) -> None:
        self.UserID = user.id

    def setAnswerStatus(self) -> None:
        self.Status = True

    def getAnswer(self):
        return self.Answer or False


class AnswerTicket(BaseModel):
    __tablename__ = BaseModel.SetTableName("answer-tickets")
    Message: so.Mapped[str] = so.mapped_column(sa.String(512), nullable=False, unique=False)

    AdminID: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey(BaseModel.SetTableName("admins") + ".id"),
                                               nullable=False, unique=False)
    TicketID: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey(BaseModel.SetTableName("tickets") + ".id"),
                                                nullable=True, unique=False)

    def setMessage(self, message: str) -> None:
        self.Message = message

    def setTicket(self, ticket: Ticket) -> None:
        """
        Set TicketID in Foreignkey Column
        ticket: Ticket class Model Instance
        """
        self.TicketID = ticket.id

    def setAdmin(self, admin) -> None:
        """
        Set AdminID in Foreignkey Column
        admin: Admin class Model Instance
        """
        self.AdminID = admin.id


class NewsLetter(BaseModel):
    __tablename__ = BaseModel.SetTableName("news-letters")
    Email: so.Mapped[str] = so.mapped_column(sa.String(1024), nullable=False, unique=True)
    VerifiedAT: so.Mapped[str] = so.mapped_column(sa.DateTime, nullable=False, unique=False)
