# build in
import math

# libs
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, IntegerField, FileField
from wtforms.validators import DataRequired, InputRequired, NumberRange

from Core.extensions import RedisServer


class PCBLayerUtils:
    def __init__(self, layer, area):
        self.layer = layer
        self.area = area
        self.day = 0
        self.price = 0


    def get_price(self):
        if self.layer == 1:
            self.cons = 200  # constant price
            if self.area > 0 and self.area <= 3.0:
                self.price += (self.area) * 441
                self.day += 6
            elif self.area >= 3.1 and self.area <= 10.0:
                self.price += (self.area) * 357
                self.day += 9
            elif self.area >= 10.1 and self.area <= 30.0:
                self.price += (self.area) * 336
                self.day += 10
            elif self.area >= 30.1 and self.area <= 50.0:
                self.price += (self.area) * 320
                self.day += 12
            elif self.area >= 50.1 and self.area <= 100.0:
                self.price += (self.area) * 310
                self.day += 14
            else:
                self.price += (self.area) * 300
                self.day += 16

        elif self.layer == 2:
            self.cons = 300
            if  self.area > 0 and self.area <= 3.0:
                self.price += (self.area) * 600
                self.day += 6
            elif self.area >= 3.1 and self.area <= 10.0:
                self.price += (self.area) * 540
                self.day += 10
            elif self.area >= 10.1 and self.area <= 30.0:
                self.price += (self.area) * 430
                self.day += 12
            elif self.area >= 30.1 and self.area <= 50.0:
                self.price += (self.area) * 410
                self.day += 14
            elif self.area >= 50.1 and self.area <= 100.0:
                self.price += (self.area) * 390
                self.day += 16
            else:
                self.price += (self.area) * 380
                self.day += 18

        elif self.layer == 4:
            self.cons = 800
            if  self.area > 0 and self.area <= 3.0:
                self.price += (self.area) * 850
                self.day += 7
            elif self.area >= 3.1 and self.area <= 10.0:
                self.price += (self.area) * 800
                self.day += 11
            elif self.area >= 10.1 and self.area <= 30.0:
                self.price += (self.area) * 700
                self.day += 14
            elif self.area >= 30.1 and self.area <= 50.0:
                self.price += (self.area) * 680
                self.day += 16
            elif self.area >= 50.1 and self.area <= 100.0:
                self.price += (self.area) * 650
                self.day += 18
            else:
                self.price += (self.area) * 630
                self.day += 20

        elif self.layer == 6:
            self.cons = 1500
            if  self.area > 0 and self.area <= 3.0:
                self.price += (self.area) * 1300
                self.day += 8
            elif self.area >= 3.1 and self.area <= 10.0:
                self.price += (self.area) * 1155
                self.day += 12
            elif self.area >= 10.1 and self.area <= 30.0:
                self.price += (self.area) * 1050
                self.day += 14
            elif self.area >= 30.1 and self.area <= 50.0:
                self.price += (self.area) * 966
                self.day += 16
            elif self.area >= 50.1 and self.area <= 100.0:
                self.price += (self.area) * 945
                self.day += 18
            else:
                self.price += (self.area) * 920
                self.day += 20

        elif self.layer == 8:
            self.cons = 1800
            if  self.area > 0 and self.area <= 3.0:
                self.price += (self.area) * 1700
                self.day += 9
            elif self.area >= 3.1 and self.area <= 10.0:
                self.price += (self.area) * 1550
                self.day += 12
            elif self.area >= 10.1 and self.area <= 30.0:
                self.price += (self.area) * 1450
                self.day += 15
            elif self.area >= 30.1 and self.area <= 50.0:
                self.price += (self.area) * 1350
                self.day += 16
            elif self.area >= 50.1 and self.area <= 100.0:
                self.price += (self.area) * 1300
                self.day += 18
            else:
                self.price += (self.area) * 1260
                self.day += 20

        return {"price": self.price, "day": self.day, "constant_price": self.cons}

class OrderICForm(FlaskForm):
    def validate(self):
        content = super().validate()
        if content:
            # base rules
            if self.Width.data < 10 or self.Length.data < 10:
                self.Width.errors = "طول باید ححداقل 10 میلبی متر باشد"
                self.Length.errors = "عرض حداقل باید 10 میلی متر باشد"
                return False
            return content
        else:
            return content

    def parse_errors(self):
        # TODO: instead of retuning form.errors return a persian message
        # form.parse_errors()
        ...


    Length = IntegerField(
        label="عرض ( بر حسب میلی متر)",
        validators=[
            DataRequired(message="ورود داده در این فیلد الزامی است"),
            InputRequired(message="ورود داده در این فیلد الزامی است"),
        ],
        render_kw={
            "placeholder":"عرض بر حسب میلی متر mm",
            "class":"form-control",
            "style": "direction:rtl !important"
        }
    )

    Width = IntegerField(
        label="طول ( بر حسب میلی متر)",
        validators=[
            DataRequired(message="ورود داده در این فیلد الزامی است"),
            InputRequired(message="ورود داده در این فیلد الزامی است"),

        ],
        render_kw={
            "placeholder":"طول بر حسب میلی متر mm",
            "class":"form-control",
            "style": "direction:rtl !important"
        }
    )

    Quantity = IntegerField(
        label="تعداد",
        validators=[
            DataRequired(message="ورود داده در این فیلد الزامی است"),
            InputRequired(message="ورود داده در این فیلد الزامی است"),
            NumberRange(min=1, max=1000000, message="حداقل تعداد سفارش 1 و حداکثر 1000000 عدد می باشد")
        ],
        render_kw={
            "placeholder": "تعداد درخواستی",
            "class": "form-control",
            "style": "direction:rtl !important"
        }
    )
    ThicknessCHOICES = {
        "all": [0.5, 0.6,0.8, 1, 1.2, 1.6, 2],
        "ratio": {
            "2": 1.2,
            "else": 1
        }
    }
    Thickness = SelectField(
        label="ضخامت مدار چاپی (بر حسب میلی متر)",
        choices=[f"{each} mm" for each in ThicknessCHOICES.get("all", [])],
        validators=[
            DataRequired(message="ورود داده در این فیلد الزامی است"),
            InputRequired(message="ورود داده در این فیلد الزامی است")
        ],
        render_kw={
            "placeholder": "ضخامت مدار چاپی(برحسب میلی متر)",
            "class": "form-control text-muted",
            "style": "direction:ltr !important"
        }
    )

    LayerNumber = SelectField(
        label="تعداد لایه های برد",
        choices=[f"{each} Layer" for each in [1,2,4,6,8]],
        validators=[
            DataRequired(message="ورود داده در این فیلد الزامی است"),
            InputRequired(message="ورود داده در این فیلد الزامی است")
        ],
        render_kw={
            "placeholder": "تعداد لایه",
            "class": "form-control text-muted",
            "style": "direction:ltr !important"
        }
    )

    FiberType = SelectField(
        label="نوع فیبر مدار",
        choices=["FR-4", "Other"],
        validators=[
            DataRequired(message="ورود داده در این فیلد الزامی است"),
            InputRequired(message="ورود داده در این فیلد الزامی است")
        ],
        render_kw={
            "placeholder": "نوع فیبر مدار چاپی",
            "class": "form-control text-muted",
            "style": "direction:ltr !important"
        }
    )

    MetalThicknessCHOICES = {
        "all": [1, 2],
        "ratio": {
            "2": 1.2,
            "1": 1,
            "else": 1
        }
    }

    MetalThickness = SelectField(
        label="ضخامت مس نهایی",
        choices=[f"{each} oz" for each in MetalThicknessCHOICES.get("all", [])],
        validators=[
            DataRequired(message="ورود داده در این فیلد الزامی است"),
            InputRequired(message="ورود داده در این فیلد الزامی است")
        ],
        render_kw={
            "placeholder": "ضخامت مس",
            "class": "form-control text-muted",
            "style": "direction:ltr !important"
        }
    )

    PanelStatusCHOICES = ["Panel", "Single"]
    PanelStatus = SelectField(
        label=f"نوع پنل ({', '.join(PanelStatusCHOICES)})",
        choices=PanelStatusCHOICES,
        validators=[
            DataRequired(message="ورود داده در این فیلد الزامی است"),
            InputRequired(message="ورود داده در این فیلد الزامی است")
        ],
        render_kw={
            "placeholder": "نوع پنل مدار",
            "class": "form-control text-muted",
            "style": "direction:ltr !important"
        }
    )

    FinalCover = SelectField(
        label="نوع پوشش نهایی",
        choices=["HASL", "COPPER", "ENIG"],
        validators=[
            DataRequired(message="ورود داده در این فیلد الزامی است"),
            InputRequired(message="ورود داده در این فیلد الزامی است")
        ],
        render_kw={
            "placeholder": "نوع پوشش نهایی",
            "class": "form-control text-muted",
            "style": "direction:ltr !important"
        }
    )

    PrintColor = SelectField(
        label="رنگ چاپ مدار",
        choices=["Green", "Yellow", "White", "Red", "Black/Dark", "Blue", "Orange"],
        validators=[
            DataRequired(message="ورود داده در این فیلد الزامی است"),
            InputRequired(message="ورود داده در این فیلد الزامی است")
        ],
        render_kw={
            "placeholder": "رنگ جاپ مدار",
            "class": "form-control text-muted",
            "style": "direction:ltr !important"
        }
    )

    ProductHelperColor = SelectField(
        label="رنگ چاپ راهنمای قطعات",
        choices=["White", "Yellow", "Green", "Red", "Black/Dark", "Blue", "Orange"],
        validators=[
            DataRequired(message="ورود داده در این فیلد الزامی است"),
            InputRequired(message="ورود داده در این فیلد الزامی است")
        ],
        render_kw={
            "placeholder": "رنگ چاپ راهنمای قطعات",
            "class": "form-control text-muted",
            "style": "direction:ltr !important"
        }
    )

    LayerPositionCHOICES = {
        "all": ["Default", "Other"],
        "ratio": {
            "Default": 1,
            "Other": 1.2,
            "else": 1.2
        }
    }
    LayerPosition = SelectField(
        label="مدل لایه چینی",
        choices=LayerPositionCHOICES.get("all", []),
        validators=[
            DataRequired(message="ورود داده در این فیلد الزامی است"),
            InputRequired(message="ورود داده در این فیلد الزامی است")
        ],
        render_kw={
            "placeholder": "مدل لایه چینی",
            "class": "form-control text-muted",
            "style": "direction:ltr !important"
        }
    )

    MicrosectionTest = SelectField(
        label="تست میکروسکشن (Microsection Test)",
        choices=["Yes", "No"],
        default="No",
        validators=[
            DataRequired(message="ورود داده در این فیلد الزامی است"),
            InputRequired(message="ورود داده در این فیلد الزامی است")
        ],
        render_kw={
            "placeholder": "تست میکروسکشن",
            "class": "form-control text-muted",
            "style": "direction:ltr !important"
        }
    )

    ElectricalTest = SelectField(
        label="تست الکتریکال (Electrical Test)",
        choices=["Yes", "No"],
        default="No",
        validators=[
            DataRequired(message="ورود داده در این فیلد الزامی است"),
            InputRequired(message="ورود داده در این فیلد الزامی است")
        ],
        render_kw={
            "placeholder": "تست الکتریکال",
            "class": "form-control text-muted",
            "style": "direction:ltr !important"
        }
    )

    File = FileField(
        validators=[

        ],
        render_kw={
            "class": "form-control mb-3",
            "placeholder": "فایل",
        }
    )


    Submit = SubmitField(
        render_kw={
            "value" : "مشاهده قیمت",
            "class": "btn btn-primary w-100 my-2"
        }
    )

    def calculate_price(self):
        day = 0
        price = 0
        message = ""

        cny_price = RedisServer.get("currency_price")
        if cny_price:
            cny_price.decode("utf-8")
            cny_price = int(cny_price)
            message+="<br>"+f"قیمت حال ارز چین: {cny_price}" + "<br>"
        else:
            message+="قیمت ارز چین: عدم ارتباط با سرویس قیمت لحظه ای" + "<br>"
            cny_price = False

        qty = self.Quantity.data
        area = (self.Width.data * self.Length.data) / 1000000

        message += f"<br>مساحت یک برد: {area}<br>"
        message += f"<br>مساحت تمام بردها:  مساحت یک برد * تعداد <br>"
        message += f"<br>مساحت تمام بردها: {area*qty}<br>"


        boardThickness = self.Thickness.data.split(" mm")[0]
        boardThicknessRatio = self.ThicknessCHOICES.get("ratio")["else"] if boardThickness not in self.ThicknessCHOICES.get("ratio") else self.ThicknessCHOICES.get("ratio")[boardThickness]
        message += f"<br>ضریب ضخامت مدارچاپی: {boardThicknessRatio}<br>"


        metalThickness = self.MetalThickness.data.split(" oz")[0]
        metal_ratio = self.MetalThicknessCHOICES.get("ratio")["else"] if metalThickness not in self.MetalThicknessCHOICES.get("ratio") else self.MetalThicknessCHOICES.get("ratio")[metalThickness]
        message += f"<br>ضریب ضخامت مس نهایی: {metal_ratio}<br>"

        layer = self.LayerNumber.data.split(" Layer")[0]
        layer = int(layer)
        is_fiber_fr4 = self.FiberType.data == "FR-4"
        if not is_fiber_fr4:
            message += f"<br> نوع فیبر الباقی می باشد امکان دارد در قیمت نهایی کمی بیشتر باشد:  <br>"



        result = PCBLayerUtils(layer=layer, area=area)
        result = result.get_price()
        price += result["price"]
        constant_price = result["constant_price"]
        day += result["day"]

        if self.FinalCover.data == "ENIG":
            price += (140 * qty)
            message += f"\پوشش نهایی ENIG می باشد 140 یوان به قیمت نهایی اضافه شد (به ازای هر عدد برد )<br>"

        if self.PrintColor.data.lower() != "green":
            message += f"\رنگ های به جز سبر مبلغ 40 یوان به قیمت اضافه می کند (به ازای هر عدد برد )<br>"
            price += (40 * qty)

        if self.ProductHelperColor.data.lower() != "white":
            message += f"\رنگ چاپ راهنمای قطعات به جز سفید شامل 20 یوان اضافه می باشد (به ازای هر عدد برد )<br>"
            price += (20 * qty)

        lazyerPosition = self.LayerPosition.data
        lazyerPositionRatio = self.LayerPositionCHOICES.get("ratio")["else"] if lazyerPosition not in self.LayerPositionCHOICES.get("all") else self.LayerPositionCHOICES.get("ratio")[lazyerPosition]
        message += f"<br>ضریب لایه چینی: {lazyerPositionRatio}<br>"

        if self.MicrosectionTest.data.lower() == "yes":
            message += f"<br> تست میکروسکشن مبلغ 40 یوان به سفارش اضافه می کند (به ازای هر عدد برد ) <br>"
            price += (40 )

        price *= lazyerPositionRatio
        price *= metal_ratio
        price *= boardThicknessRatio
        price *= qty
        price += constant_price
        day += 8

        price *= 1.3
        price = math.ceil(price)

        if cny_price:
            message += f"<br>قیمت به یوان: {price}<br>"
            price *= cny_price
            price = "{:,.0f}".format(price)
            price = f" {price} ریال "
        else:
            price = f"{price} یوان چین "


        return (price, day, message)

