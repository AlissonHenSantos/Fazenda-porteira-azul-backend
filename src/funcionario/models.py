from .. import db 
from sqlalchemy import inspect


class Funcionario(db.Model):               
    id           = db.Column(db.String(50), primary_key=True, nullable=False, unique=True)

    nome        = db.Column(db.String(100), nullable=False, unique=True)

    idCultura    = db.Column(db.String(50), db.ForeignKey('cultura.id'), nullable=False)
    cultura      = db.relationship('Cultura', backref=db.backref('funcionarios', lazy=True))

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }

    def __repr__(self):
        return "<%r>" % self.nome