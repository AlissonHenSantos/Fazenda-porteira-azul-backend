from .. import db 
from sqlalchemy import inspect
from datetime import datetime, date


class HorasFuncionario(db.Model):               
    id           = db.Column(db.String(50), primary_key=True, nullable=False, unique=True)

    horas        = db.Column(db.Integer, nullable=False)

    data        = db.Column(db.Date, default=datetime.now)

    idFuncionario    = db.Column(db.String(50), db.ForeignKey('funcionario.id'), nullable=False)
    funcionario      = db.relationship('Funcionario', backref=db.backref('horas_trabalhadas', lazy=True))

    def toDict(self):
        result = {}
        for c in inspect(self).mapper.column_attrs:
            value = getattr(self, c.key)
            if isinstance(value, (datetime, date)):
                value = value.strftime('%d-%m-%Y')
            result[c.key] = value
        return result

    def __repr__(self):
        return f"<HorasFuncionario: {self.horas}h em {self.data} - Funcionário: {self.idFuncionario}>"