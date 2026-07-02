import json
from dataclasses import asdict, dataclass, replace
from datetime import datetime
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
PROJETO_MONITORAMENTO_PATH = DATA_DIR / "projeto_monitoramento.json"
DOSSIE_FINAL_PROJETO_PATH = DATA_DIR / "dossie_final_projeto.json"

PROJETO_ATIVO_ID = "projeto_monitoramento_principal"
DOSSIE_FINAL_ID = "dossie_final_projeto_monitoramento_principal"
STATUS_ATIVO = "ativo"
STATUS_ENCERRADO = "encerrado"
STATUS_ARQUIVADO = "arquivado"
STATUS_LEGADO_INATIVO = "inativo"

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
STATUS_PROJETO = (STATUS_ATIVO, STATUS_ENCERRADO, STATUS_ARQUIVADO)


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


@dataclass(frozen=True)
class DossierFinal:
    identificador: str
    identificador_projeto: str
    projeto_nome: str
    cliente: str
    contexto_operacional: str
    perfil_operacional: str
    periodo_inicio: str = ""
    periodo_fim: str = ""
    data_encerramento: str = ""
    status_projeto: str = STATUS_ENCERRADO


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
        if payload.get("status") == STATUS_LEGADO_INATIVO:
            payload["status"] = STATUS_ENCERRADO

        projeto = ProjetoMonitoramento(**payload)
        validar_projeto_monitoramento(projeto)
        return projeto

    def salvar(self, projeto):
        projeto = normalizar_projeto_monitoramento(projeto)
        validar_projeto_monitoramento(projeto)
        status_atual = self._status_persistido()
        if status_atual is None and projeto.status != STATUS_ATIVO:
            raise ValueError("Projeto novo deve nascer como ativo.")
        if status_atual is not None:
            validar_transicao_status(status_atual, projeto.status)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w", encoding="utf-8") as file:
            json.dump(asdict(projeto), file, ensure_ascii=False, indent=2)
            file.write("\n")
        return projeto

    def _status_persistido(self):
        if not self.path.exists():
            return None
        with self.path.open("r", encoding="utf-8") as file:
            payload = json.load(file)
        status = payload.get("status", STATUS_ATIVO)
        if status == STATUS_LEGADO_INATIVO:
            return STATUS_ENCERRADO
        return status


class DossierFinalStore:
    def __init__(self, path=DOSSIE_FINAL_PROJETO_PATH):
        self.path = Path(path)

    def carregar(self):
        if not self.path.exists():
            return None
        with self.path.open("r", encoding="utf-8") as file:
            payload = json.load(file)
        dossie = DossierFinal(**payload)
        validar_dossier_final(dossie)
        return dossie

    def salvar(self, dossie):
        validar_dossier_final(dossie)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w", encoding="utf-8") as file:
            json.dump(asdict(dossie), file, ensure_ascii=False, indent=2)
            file.write("\n")
        return dossie


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


def dossier_final_do_projeto(
    projeto,
    periodo_inicio="",
    periodo_fim="",
    data_encerramento="",
):
    if projeto.status not in (STATUS_ENCERRADO, STATUS_ARQUIVADO):
        raise ValueError("Dossie Final exige Projeto encerrado.")
    return DossierFinal(
        identificador=DOSSIE_FINAL_ID,
        identificador_projeto=projeto.identificador,
        projeto_nome=projeto.nome,
        cliente=projeto.cliente,
        contexto_operacional=projeto.area_operacional,
        perfil_operacional=projeto.perfil_operacional,
        periodo_inicio=periodo_inicio,
        periodo_fim=periodo_fim,
        data_encerramento=data_encerramento,
        status_projeto=projeto.status,
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


def encerrar_projeto(projeto):
    validar_transicao_status(projeto.status, STATUS_ENCERRADO)
    return replace(projeto, status=STATUS_ENCERRADO)


def arquivar_projeto(projeto):
    validar_transicao_status(projeto.status, STATUS_ARQUIVADO)
    return replace(projeto, status=STATUS_ARQUIVADO)


def validar_transicao_status(status_atual, novo_status):
    if status_atual not in STATUS_PROJETO:
        raise ValueError(f"Status atual de projeto invalido: {status_atual}")
    if novo_status not in STATUS_PROJETO:
        raise ValueError(f"Novo status de projeto invalido: {novo_status}")
    if status_atual == novo_status:
        return True
    transicoes_permitidas = {
        STATUS_ATIVO: (STATUS_ENCERRADO,),
        STATUS_ENCERRADO: (STATUS_ARQUIVADO,),
        STATUS_ARQUIVADO: (),
    }
    if novo_status not in transicoes_permitidas[status_atual]:
        raise ValueError(f"Transicao de status invalida: {status_atual} -> {novo_status}")
    return True


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


def validar_dossier_final(dossie):
    if dossie.identificador != DOSSIE_FINAL_ID:
        raise ValueError("Identificador de Dossie Final invalido.")
    if dossie.identificador_projeto != PROJETO_ATIVO_ID:
        raise ValueError("Dossie Final deve estar associado ao Projeto principal.")
    if not dossie.projeto_nome.strip():
        raise ValueError("Dossie Final sem nome de Projeto.")
    if not dossie.cliente.strip():
        raise ValueError("Dossie Final sem cliente.")
    if dossie.contexto_operacional not in CONTEXTOS_OPERACIONAIS:
        raise ValueError(f"Contexto operacional invalido: {dossie.contexto_operacional}")
    if dossie.perfil_operacional not in PERFIS_OPERACIONAIS:
        raise ValueError(f"Perfil operacional invalido: {dossie.perfil_operacional}")
    if dossie.perfil_operacional != derivar_perfil_operacional(dossie.contexto_operacional):
        raise ValueError("Perfil operacional inconsistente com o contexto operacional.")
    if dossie.status_projeto not in (STATUS_ENCERRADO, STATUS_ARQUIVADO):
        raise ValueError("Dossie Final exige Projeto encerrado ou arquivado.")
    return True


def carregar_projeto_ativo(path=PROJETO_MONITORAMENTO_PATH):
    return ProjetoMonitoramentoStore(path).carregar()


def salvar_projeto_ativo(projeto, path=PROJETO_MONITORAMENTO_PATH):
    return ProjetoMonitoramentoStore(path).salvar(projeto)


def carregar_dossier_final(path=DOSSIE_FINAL_PROJETO_PATH):
    return DossierFinalStore(path).carregar()


def salvar_dossier_final(dossie, path=DOSSIE_FINAL_PROJETO_PATH):
    return DossierFinalStore(path).salvar(dossie)
