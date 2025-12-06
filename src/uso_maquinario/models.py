from .. import db 
from sqlalchemy import inspect

class UsoMaquinario(db.Model):               
    __tablename__ = 'uso_maquinario'
    
    id            = db.Column(db.String(50), primary_key=True, nullable=False, unique=True)
    idMaquinario  = db.Column(db.String(50), db.ForeignKey('maquinario.id'), nullable=False)
    idFuncionario = db.Column(db.String(50), db.ForeignKey('funcionario.id'), nullable=False)
    data_inicio   = db.Column(db.DateTime, nullable=False)
    data_fim      = db.Column(db.DateTime, nullable=True)

    maquinario    = db.relationship('Maquinario', backref='usos')
    funcionario   = db.relationship('Funcionario', backref='usos_maquinario')

    def toDict(self):
        return {
            'id': self.id,
            'idMaquinario': self.idMaquinario,
            'idFuncionario': self.idFuncionario,
            'data_inicio': self.data_inicio.isoformat() if self.data_inicio else None,
            'data_fim': self.data_fim.isoformat() if self.data_fim else None,
        }

    def __repr__(self):
        return f'<UsoMaquinario {self.id}>'