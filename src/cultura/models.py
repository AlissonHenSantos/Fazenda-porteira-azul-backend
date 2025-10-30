from .. import db 
from sqlalchemy import inspect


class Cultura(db.Model):               
    id           = db.Column(db.String(50), primary_key=True, nullable=False, unique=True)

    nome        = db.Column(db.String(100), nullable=False, unique=True)

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }

    def __repr__(self):
        return "<%r>" % self.nome