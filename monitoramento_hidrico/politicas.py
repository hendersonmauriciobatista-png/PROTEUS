import json
from pathlib import Path

from .models import PoliticaAvaliacao


BASE_DIR = Path(__file__).resolve().parent.parent
POLITICAS_PATH = BASE_DIR / "data" / "monitoramento_hidrico_politicas.json"

TIPO_OBSERVACIONAL = "observacional"
TIPO_NORMATIVA_FUTURA = "normativa_futura"
TIPO_INTERNA_FUTURA = "interna_futura"

MOTOR_OBSERVACIONAL = "avaliacao_observacional"


class PolicyEngine:
    def __init__(self, politicas_path=POLITICAS_PATH, politicas=None):
        self.politicas_path = Path(politicas_path)
        self._politicas = politicas

    def listar_politicas(self):
        if self._politicas is not None:
            return list(self._politicas)

        with self.politicas_path.open("r", encoding="utf-8") as file:
            payload = json.load(file)

        return [PoliticaAvaliacao(**item) for item in payload.get("politicas", [])]

    def selecionar_politica(self, perfil_operacional=None, categoria=None, parametro_id=None):
        politicas = self.listar_politicas()
        candidatas = [
            politica
            for politica in politicas
            if _politica_aplicavel(politica, perfil_operacional, categoria, parametro_id)
        ]

        if not candidatas:
            return _politica_observacional_padrao()

        return sorted(
            candidatas,
            key=lambda politica: (_peso_especificidade(politica), politica.prioridade),
            reverse=True,
        )[0]


def listar_politicas_disponiveis(path=POLITICAS_PATH):
    return PolicyEngine(path).listar_politicas()


def selecionar_politica_avaliacao(perfil_operacional=None, categoria=None, parametro_id=None, path=POLITICAS_PATH):
    return PolicyEngine(path).selecionar_politica(perfil_operacional, categoria, parametro_id)


def _politica_aplicavel(politica, perfil_operacional, categoria, parametro_id):
    if politica.perfil_operacional and politica.perfil_operacional != perfil_operacional:
        return False
    if politica.categoria and politica.categoria != categoria:
        return False
    if politica.parametro_id and politica.parametro_id != parametro_id:
        return False
    return True


def _peso_especificidade(politica):
    peso = 0
    if politica.perfil_operacional:
        peso += 1
    if politica.categoria:
        peso += 2
    if politica.parametro_id:
        peso += 4
    return peso


def _politica_observacional_padrao():
    return PoliticaAvaliacao(
        identificador="politica_observacional_padrao",
        nome="Politica Observacional Padrao",
        tipo=TIPO_OBSERVACIONAL,
        motor_destino=MOTOR_OBSERVACIONAL,
        prioridade=0,
        observacoes="Politica padrao para selecionar o motor observacional sem executar avaliacao.",
    )
