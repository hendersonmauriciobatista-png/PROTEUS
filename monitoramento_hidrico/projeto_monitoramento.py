import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
PROJETO_MONITORAMENTO_PATH = DATA_DIR / "projeto_monitoramento.json"

PROJETO_ATIVO_ID = "projeto_monitoramento_principal"
STATUS_ATIVO = "ativo"
STATUS_INATIVO = "inativo"

AREAS_OPERACIONAIS = ("urbana", "rural", "industrial", "agricola")
PONTOS_PRINCIPAIS_COLETA = ("rio", "poco", "reservatorio", "eta", "lago", "outro")
STATUS_PROJETO = (STATUS_ATIVO, STATUS_INATIVO)


@dataclass(frozen=True)
class ProjetoMonitoramento:
    identificador: str
    nome: str
    cliente: str
    area_operacional: str
    ponto_principal_coleta: str
    coletor_responsavel: str
    data_criacao: str
    status: str = STATUS_ATIVO


class ProjetoMonitoramentoStore:
    def __init__(self, path=PROJETO_MONITORAMENTO_PATH):
        self.path = Path(path)

    def carregar(self):
        if not self.path.exists():
            projeto = projeto_monitoramento_padrao()
            self.salvar(projeto)
            return projeto

        with self.path.open("r", encoding="utf-8") as file:
            payload = json.load(file)

        projeto = ProjetoMonitoramento(**payload)
        validar_projeto_monitoramento(projeto)
        return projeto

    def salvar(self, projeto):
        validar_projeto_monitoramento(projeto)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w", encoding="utf-8") as file:
            json.dump(asdict(projeto), file, ensure_ascii=False, indent=2)
            file.write("\n")
        return projeto


def projeto_monitoramento_padrao(criado_em=None):
    return ProjetoMonitoramento(
        identificador=PROJETO_ATIVO_ID,
        nome="Projeto de Monitoramento Principal",
        cliente="Cliente nao informado",
        area_operacional="urbana",
        ponto_principal_coleta="outro",
        coletor_responsavel="Coletor nao informado",
        data_criacao=criado_em or datetime.now().isoformat(timespec="seconds"),
        status=STATUS_ATIVO,
    )


def validar_projeto_monitoramento(projeto):
    if projeto.identificador != PROJETO_ATIVO_ID:
        raise ValueError("A GP-D01B permite apenas o projeto principal ativo nesta etapa.")
    if not projeto.nome.strip():
        raise ValueError("Projeto de Monitoramento sem nome.")
    if not projeto.cliente.strip():
        raise ValueError("Projeto de Monitoramento sem cliente.")
    if projeto.area_operacional not in AREAS_OPERACIONAIS:
        raise ValueError(f"Area operacional invalida: {projeto.area_operacional}")
    if projeto.ponto_principal_coleta not in PONTOS_PRINCIPAIS_COLETA:
        raise ValueError(f"Ponto principal de coleta invalido: {projeto.ponto_principal_coleta}")
    if not projeto.coletor_responsavel.strip():
        raise ValueError("Projeto de Monitoramento sem coletor responsavel.")
    if not projeto.data_criacao.strip():
        raise ValueError("Projeto de Monitoramento sem data de criacao.")
    if projeto.status not in STATUS_PROJETO:
        raise ValueError(f"Status de projeto invalido: {projeto.status}")
    return True


def carregar_projeto_ativo(path=PROJETO_MONITORAMENTO_PATH):
    return ProjetoMonitoramentoStore(path).carregar()


def salvar_projeto_ativo(projeto, path=PROJETO_MONITORAMENTO_PATH):
    return ProjetoMonitoramentoStore(path).salvar(projeto)

