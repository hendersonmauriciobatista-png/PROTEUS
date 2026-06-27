from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class PerfilOperacional:
    codigo: str
    nome: str
    descricao: str = ""


@dataclass(frozen=True)
class CategoriaParametro:
    codigo: str
    nome: str
    descricao: str = ""


@dataclass(frozen=True)
class ParametroHidrico:
    codigo: str
    nome: str
    categoria: str
    unidade: Optional[str] = None
    unidade_medida: Optional[str] = None
    tipo_valor: str = "numerico"
    aplicabilidade_perfis: list[str] = field(default_factory=list)
    metodo_analise: Optional[str] = None
    frequencia_recomendada: Optional[str] = None
    observacoes_tecnicas: Optional[str] = None
    limite_observacional: Optional[dict] = None
    descricao: str = ""


@dataclass
class ConfiguracaoOperacional:
    identificador: str
    nome: str
    perfil_operacional_base: str
    categorias_habilitadas: list[str] = field(default_factory=list)
    parametros_habilitados: list[str] = field(default_factory=list)
    observacoes: str = ""


@dataclass(frozen=True)
class ResultadoAvaliacaoObservacional:
    parametro_id: str
    valor_avaliado: object
    status: str
    mensagem: str
    severidade: str
    origem_limite: str
    observacoes: str = ""
