from .. import db
from datetime import datetime
from sqlalchemy import inspect

class CotacaoCultura(db.Model):
    __tablename__ = 'cotacao_cultura'
    
    id = db.Column(db.String(50), primary_key=True, nullable=False, unique=True)
    idCultura = db.Column(db.String(50), db.ForeignKey('cultura.id'), nullable=False)
    
    precoAtual = db.Column(db.Float, nullable=False)
    precoAlta = db.Column(db.Float, nullable=True)
    precoBaixa = db.Column(db.Float, nullable=True)
    
    dataCriacao = db.Column(db.DateTime, default=datetime.utcnow)
    dataAtualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    cultura = db.relationship('Cultura', backref=db.backref('cotacoes', lazy=True))
    
    def toDict(self):
        result = {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
        
        if self.cultura:
            result['nomeCultura'] = getattr(self.cultura, 'nome', None)
        
        if isinstance(result.get('dataCriacao'), datetime):
            result['dataCriacao'] = result['dataCriacao'].isoformat()
        if isinstance(result.get('dataAtualizacao'), datetime):
            result['dataAtualizacao'] = result['dataAtualizacao'].isoformat()
        
        return result

    def __repr__(self):
        return f"<CotacaoCultura: {self.idCultura} - R$ {self.precoAtual}>"