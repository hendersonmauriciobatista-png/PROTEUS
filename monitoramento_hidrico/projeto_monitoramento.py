import json
from dataclasses import asdict, dataclass, replace
from datetime import datetime
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
PROJETO_MONITORAMENTO_PATH = DATA_DIR / "projeto_monitoramento.json"

PROJETO_ATIVO_ID = "projeto_monitoramento_principal"
STATUS_ATIVO = "ativo"
STATUS_INATIVO = "inativo"

CONTEXTOS_OPERACIONAIS = ("urbana", "rural", "industrial", "agricola")
PERFIS_OPERACIONAIS = ("urbano_saneamento", "rural", "industrial")
PERFIL_OPERACIONAL_POR_CONTEXTO = {
    "urbana": "urbano_saneamento",
    "rural": "rural",
    "industrial": "industrial",
    "agricola": "rural",
}
AREAS_OPERACIONAIS = CONTEXTOS_OPERACIONAIS
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
    perfil_operacional: str
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

        if "perfil_operacional" not in payload:
            payload["perfil_operacional"] = derivar_perfil_operacional(payload.get("area_operacional"))

        projeto = ProjetoMonitoramento(**payload)
        validar_projeto_monitoramento(projeto)
        return projeto

    def salvar(self, projeto):
        projeto = normalizar_projeto_monitoramento(projeto)
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
        perfil_operacional="urbano_saneamento",
        status=STATUS_ATIVO,
    )


def derivar_perfil_operacional(contexto_operacional):
    if contexto_operacional not in PERFIL_OPERACIONAL_POR_CONTEXTO:
        raise ValueError(f"Contexto operacional invalido: {contexto_operacional}")
    return PERFIL_OPERACIONAL_POR_CONTEXTO[contexto_operacional]


def normalizar_projeto_monitoramento(projeto):
    return replace(
        projeto,
        perfil_operacional=derivar_perfil_operacional(projeto.area_operacional),
    )


def validar_projeto_monitoramento(projeto):
    if projeto.identificador != PROJETO_ATIVO_ID:
        raise ValueError("A GP-D01B permite apenas o projeto principal ativo nesta etapa.")
    if not projeto.nome.strip():
        raise ValueError("Projeto de Monitoramento sem nome.")
    if not projeto.cliente.strip():
        raise ValueError("Projeto de Monitoramento sem cliente.")
    if projeto.area_operacional not in CONTEXTOS_OPERACIONAIS:
        raise ValueError(f"Contexto operacional invalido: {projeto.area_operacional}")
    if projeto.perfil_operacional not in PERFIS_OPERACIONAIS:
        raise ValueError(f"Perfil operacional invalido: {projeto.perfil_operacional}")
    if projeto.perfil_operacional != derivar_perfil_operacional(projeto.area_operacional):
        raise ValueError("Perfil operacional inconsistente com o contexto operacional.")
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
