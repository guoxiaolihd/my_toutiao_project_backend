import datetime

from mongoengine import *
import config

connect("yesterday_toutiao")


# 字典形式转换为列表用于数据的返回
class CustomQuerySet(QuerySet):
    def to_public_json(self):
        result = []
        try:
            for doc in self:
                jsonDic = doc.to_public_json()
                result.append(jsonDic)
        except:
            print('error')
        return result


# 用户信息
class User(Document):
    mobile = StringField(max_length=11, unique=True)
    name = StringField(required=True, unique=True)
    code = StringField(required=True)
    created = DateTimeField(required=True, default=datetime.datetime.now())
    photo = StringField(required=True)
    gender = IntField(required=True)
    intro = StringField(required=True)
    email = StringField(required=True, unique=True)

    def to_public_json(self):
        data = {
            "mobile": self.mobile,
            "name": self.name,
            "created": self.created.strftime("%Y-%m-%d %H:%M:%S"),
            "photo": self.photo,
            "gender": self.gender,
            "intro": self.intro,
            "email": self.email
        }

        return data


# 添加频道的信息（id+name）
class Channel(Document):
    name = StringField(max_length=120, required=True)

    meta = {'queryset_class': CustomQuerySet}

    def to_public_json(self):
        data = {
            "id": str(self.id),
            "name": self.name,
        }
        return data


# 图片信息(id+url+是否收藏)
class Img(Document):
    user = ReferenceField(User, reverse_delete_rule=CASCADE)
    url = StringField(max_length=200, required=True)
    is_collected = BooleanField(required=True, default=False)

    meta = {'queryset_class': CustomQuerySet}

    def to_public_json(self):
        data = {
            "id": str(self.id),
            "url": config.base_url + self.url,
            "is_collected": self.is_collected
        }
        return data
