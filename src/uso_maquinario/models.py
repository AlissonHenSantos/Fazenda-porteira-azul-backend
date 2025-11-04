from .. import db 
from sqlalchemy import inspect
from datetime import datetime, date


class UsoMaquinario(db.Model):               
    id           = db.Column(db.String(50), primary_key=True, nullable=False, unique=True)

    idCultura    = db.Column(db.String(50), db.ForeignKey('cultura.id'), nullable=False)
    cultura      = db.relationship('Cultura', backref=db.backref('uso_maquinario', lazy=True))

    idMaquinario    = db.Column(db.String(50), db.ForeignKey('maquinario.id'), nullable=False)
    maquinario      = db.relationship('Maquinario', backref=db.backref('uso_maquinario', lazy=True))

    tempo_uso   = db.Column(db.Integer, nullable=False) 

    data_uso  = db.Column(db.Date, default=lambda: datetime.now().date())

    def toDict(self):
        result = {}
        for c in inspect(self).mapper.column_attrs:
            value = getattr(self, c.key)
            if isinstance(value, (datetime, date)):
                value = value.strftime('%d-%m-%Y')
            result[c.key] = value
        return result

    def __repr__(self):
        return f"<UsoMaquinario: {self.tempo_uso}h em {self.data_uso} - Maquinario: {self.idMaquinario}>"