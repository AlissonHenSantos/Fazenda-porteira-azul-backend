from .. import db 
from sqlalchemy import inspect


class CotacaoCultura(db.Model):               
    id           = db.Column(db.String(50), primary_key=True, nullable=False, unique=True)

    value        = db.Column(db.Double(100), nullable=False)
    
    idCultura    = db.Column(db.String(50), db.ForeignKey('cultura.id'), nullable=False)
    cultura      = db.relationship('Cultura', backref=db.backref('cotacoes', lazy=True))

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }

    def __repr__(self):
        return f"<Cotacao: {self.value} - Cultura: {self.idCultura}>"