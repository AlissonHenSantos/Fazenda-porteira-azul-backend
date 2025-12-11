import os

from . import create_app
app = create_app(os.getenv("CONFIG_MODE"))


@app.route('/')
def hello():
    return "Hello World!"

from .user import urls
from .cultura import urls
from .maquinario import urls
from .funcionario import urls
from .horas_funcionario import urls
from .uso_maquinario import urls
from .custo_producao import urls
from .cotacao_cultura import urls
from .analise_venda import urls as analise_urls
from .historico_sazonalidade import urls as sazonalidade_urls
from .alerta_venda import urls as alerta_urls




if __name__ == "__main__":
    app.run()