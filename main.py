"""
Sistema de Cotação e Gestão de Fretes - Design Patterns
Desenvolvido por: Rafael Zink
"""

# ============================================================================
# DOMAIN - Entidades do domínio
# ============================================================================

from dataclasses import dataclass
from typing import List
from abc import ABC, abstractmethod
from datetime import datetime, timedelta


@dataclass
class Pacote:
    """Representa um pacote a ser entregue"""
    peso_kg: float
    volume_m3: float
    origem: str
    destino: str
    zona: str  # "local", "regional", "nacional"


@dataclass
class Entrega:
    """Representa uma entrega completa"""
    pacote: Pacote
    valor_frete: float
    prazo_dias: int
    transportadora: str
    detalhes: List[str]

    def __str__(self):
        detalhes_str = "\n    ".join(self.detalhes) if self.detalhes else "Nenhum"
        return f"""
╔══════════════════════════════════════════════════════════════
║ COTAÇÃO DE ENTREGA
╠══════════════════════════════════════════════════════════════
║ Origem: {self.pacote.origem}
║ Destino: {self.pacote.destino}
║ Zona: {self.pacote.zona}
║ Peso: {self.pacote.peso_kg} kg
║ Volume: {self.pacote.volume_m3} m³
║ ─────────────────────────────────────────────────────────────
║ Transportadora: {self.transportadora}
║ Prazo: {self.prazo_dias} dias úteis
║ Valor do Frete: R$ {self.valor_frete:.2f}
║ ─────────────────────────────────────────────────────────────
║ Detalhes adicionais:
║     {detalhes_str}
╚══════════════════════════════════════════════════════════════
"""


# ============================================================================
# STRATEGY PATTERN - Estratégias de cálculo de frete
# ============================================================================

class FreteStrategy(ABC):
    """Interface para estratégias de cálculo de frete"""

    @abstractmethod
    def calcular(self, pacote: Pacote) -> float:
        pass

    @abstractmethod
    def get_nome(self) -> str:
        pass


class FretePorZona(FreteStrategy):
    """Calcula frete baseado na zona de entrega"""

    def __init__(self):
        self.tabela_zonas = {
            "local": 15.00,
            "regional": 35.00,
            "nacional": 80.00
        }

    def calcular(self, pacote: Pacote) -> float:
        return self.tabela_zonas.get(pacote.zona, 50.00)

    def get_nome(self) -> str:
        return "Frete por Zona"


class FretePorPeso(FreteStrategy):
    """Calcula frete baseado no peso"""

    def __init__(self):
        self.valor_por_kg = 8.50
        self.taxa_base = 10.00

    def calcular(self, pacote: Pacote) -> float:
        return self.taxa_base + (pacote.peso_kg * self.valor_por_kg)

    def get_nome(self) -> str:
        return "Frete por Peso"


class FretePorVolume(FreteStrategy):
    """Calcula frete baseado no volume"""

    def __init__(self):
        self.valor_por_m3 = 120.00
        self.taxa_base = 12.00

    def calcular(self, pacote: Pacote) -> float:
        return self.taxa_base + (pacote.volume_m3 * self.valor_por_m3)

    def get_nome(self) -> str:
        return "Frete por Volume"


class FreteJanelaExpresso(FreteStrategy):
    """Calcula frete para entrega expressa (janela de tempo)"""

    def __init__(self):
        self.multiplicador_expresso = 2.5
        self.frete_base = FretePorZona()

    def calcular(self, pacote: Pacote) -> float:
        return self.frete_base.calcular(pacote) * self.multiplicador_expresso

    def get_nome(self) -> str:
        return "Frete Expresso (Janela)"


# ============================================================================
# DECORATOR PATTERN - Serviços adicionais ao frete
# ============================================================================

class FreteComponent(ABC):
    """Componente base para decoradores de frete"""

    @abstractmethod
    def calcular_custo(self) -> float:
        pass

    @abstractmethod
    def get_descricao(self) -> List[str]:
        pass


class FreteBasico(FreteComponent):
    """Frete básico sem adicionais"""

    def __init__(self, valor_base: float, estrategia_nome: str):
        self.valor_base = valor_base
        self.estrategia_nome = estrategia_nome

    def calcular_custo(self) -> float:
        return self.valor_base

    def get_descricao(self) -> List[str]:
        return [f"Frete calculado por: {self.estrategia_nome}"]


class FreteDecorator(FreteComponent):
    """Decorador base para serviços adicionais"""

    def __init__(self, frete: FreteComponent):
        self._frete = frete

    def calcular_custo(self) -> float:
        return self._frete.calcular_custo()

    def get_descricao(self) -> List[str]:
        return self._frete.get_descricao()


class PedagioDecorator(FreteDecorator):
    """Adiciona custo de pedágios"""

    def __init__(self, frete: FreteComponent, numero_pedagios: int = 3):
        super().__init__(frete)
        self.numero_pedagios = numero_pedagios
        self.valor_pedagio = 8.50

    def calcular_custo(self) -> float:
        custo_pedagios = self.numero_pedagios * self.valor_pedagio
        return self._frete.calcular_custo() + custo_pedagios

    def get_descricao(self) -> List[str]:
        descricoes = self._frete.get_descricao()
        descricoes.append(f"+ Pedágios ({self.numero_pedagios}x): R$ {self.numero_pedagios * self.valor_pedagio:.2f}")
        return descricoes


class SeguroDecorator(FreteDecorator):
    """Adiciona seguro à carga"""

    def __init__(self, frete: FreteComponent, valor_declarado: float = 1000.00):
        super().__init__(frete)
        self.valor_declarado = valor_declarado
        self.percentual_seguro = 0.02  # 2% do valor declarado

    def calcular_custo(self) -> float:
        custo_seguro = self.valor_declarado * self.percentual_seguro
        return self._frete.calcular_custo() + custo_seguro

    def get_descricao(self) -> List[str]:
        descricoes = self._frete.get_descricao()
        custo_seguro = self.valor_declarado * self.percentual_seguro
        descricoes.append(f"+ Seguro (R$ {self.valor_declarado:.2f}): R$ {custo_seguro:.2f}")
        return descricoes


class EmbalagemEspecialDecorator(FreteDecorator):
    """Adiciona embalagem especial"""

    def __init__(self, frete: FreteComponent, tipo: str = "reforçada"):
        super().__init__(frete)
        self.tipo = tipo
        self.valores = {
            "reforçada": 25.00,
            "térmica": 45.00,
            "antiestática": 55.00
        }

    def calcular_custo(self) -> float:
        custo_embalagem = self.valores.get(self.tipo, 25.00)
        return self._frete.calcular_custo() + custo_embalagem

    def get_descricao(self) -> List[str]:
        descricoes = self._frete.get_descricao()
        custo = self.valores.get(self.tipo, 25.00)
        descricoes.append(f"+ Embalagem {self.tipo}: R$ {custo:.2f}")
        return descricoes


# ============================================================================
# FACTORY METHOD PATTERN - Criação de transportadoras por SLA
# ============================================================================

class Transportadora(ABC):
    """Produto abstrato - transportadora"""

    @abstractmethod
    def get_nome(self) -> str:
        pass

    @abstractmethod
    def get_prazo_dias(self) -> int:
        pass

    @abstractmethod
    def get_multiplicador_preco(self) -> float:
        pass


class TransportadoraEconomica(Transportadora):
    """Transportadora econômica - prazo maior"""

    def get_nome(self) -> str:
        return "TransLog Econômica"

    def get_prazo_dias(self) -> int:
        return 10

    def get_multiplicador_preco(self) -> float:
        return 1.0


class TransportadoraPadrao(Transportadora):
    """Transportadora padrão - prazo médio"""

    def get_nome(self) -> str:
        return "ExpressLog Padrão"

    def get_prazo_dias(self) -> int:
        return 5

    def get_multiplicador_preco(self) -> float:
        return 1.3


class TransportadoraExpresso(Transportadora):
    """Transportadora expressa - prazo rápido"""

    def get_nome(self) -> str:
        return "RapidLog Express"

    def get_prazo_dias(self) -> int:
        return 2

    def get_multiplicador_preco(self) -> float:
        return 1.8


class TransportadoraFactory(ABC):
    """Creator abstrato - fábrica de transportadoras"""

    @abstractmethod
    def criar_transportadora(self) -> Transportadora:
        pass

    def processar_entrega(self, pacote: Pacote, frete_base: float) -> tuple:
        """Template method que usa a factory"""
        transportadora = self.criar_transportadora()
        valor_final = frete_base * transportadora.get_multiplicador_preco()
        prazo = transportadora.get_prazo_dias()
        return transportadora.get_nome(), valor_final, prazo


class FactoryEconomica(TransportadoraFactory):
    """Fábrica para SLA econômico"""

    def criar_transportadora(self) -> Transportadora:
        return TransportadoraEconomica()


class FactoryPadrao(TransportadoraFactory):
    """Fábrica para SLA padrão"""

    def criar_transportadora(self) -> Transportadora:
        return TransportadoraPadrao()


class FactoryExpresso(TransportadoraFactory):
    """Fábrica para SLA expresso"""

    def criar_transportadora(self) -> Transportadora:
        return TransportadoraExpresso()


# ============================================================================
# SINGLETON PATTERN - Configuração e Log centralizados
# ============================================================================

class ConfiguracaoSistema:
    """Singleton para configurações do sistema"""

    _instancia = None
    _inicializado = False

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
        return cls._instancia

    def __init__(self):
        if not ConfiguracaoSistema._inicializado:
            self.versao = "1.0.0"
            self.nome_sistema = "SysLog - Sistema de Cotação de Fretes"
            self.desenvolvedor = "[Seu Nome Aqui]"
            self.max_tentativas = 3
            self.timeout_segundos = 30
            ConfiguracaoSistema._inicializado = True

    def get_info(self) -> str:
        return f"{self.nome_sistema} v{self.versao}"

    def get_desenvolvedor(self) -> str:
        return self.desenvolvedor


class LogSistema:
    """Singleton para logging centralizado"""

    _instancia = None
    _inicializado = False

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
        return cls._instancia

    def __init__(self):
        if not LogSistema._inicializado:
            self.logs = []
            LogSistema._inicializado = True

    def registrar(self, mensagem: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {mensagem}"
        self.logs.append(log_entry)
        print(f"🔹 LOG: {mensagem}")

    def get_logs(self) -> List[str]:
        return self.logs.copy()


# ============================================================================
# APP - Serviço principal e Menu
# ============================================================================

class ServicoFrete:
    """Serviço principal que integra todos os padrões"""

    def __init__(self):
        self.config = ConfiguracaoSistema()
        self.log = LogSistema()
        self.estrategias = {
            "1": FretePorZona(),
            "2": FretePorPeso(),
            "3": FretePorVolume(),
            "4": FreteJanelaExpresso()
        }
        self.factories = {
            "1": FactoryEconomica(),
            "2": FactoryPadrao(),
            "3": FactoryExpresso()
        }

    def cotar_entrega(self, pacote: Pacote, opcao_estrategia: str,
                      opcao_sla: str, servicos_adicionais: List[str]) -> Entrega:
        """Caso de uso principal: cotar uma entrega"""

        self.log.registrar(f"Iniciando cotação: {pacote.origem} → {pacote.destino}")

        # 1. STRATEGY: Escolher estratégia de cálculo
        estrategia = self.estrategias.get(opcao_estrategia, FretePorZona())
        valor_base = estrategia.calcular(pacote)
        self.log.registrar(f"Estratégia '{estrategia.get_nome()}': R$ {valor_base:.2f}")

        # 2. DECORATOR: Aplicar serviços adicionais
        frete_component = FreteBasico(valor_base, estrategia.get_nome())

        if "pedagio" in servicos_adicionais:
            frete_component = PedagioDecorator(frete_component)
            self.log.registrar("Adicionado: Pedágios")

        if "seguro" in servicos_adicionais:
            frete_component = SeguroDecorator(frete_component, valor_declarado=1500.00)
            self.log.registrar("Adicionado: Seguro")

        if "embalagem" in servicos_adicionais:
            frete_component = EmbalagemEspecialDecorator(frete_component, "reforçada")
            self.log.registrar("Adicionado: Embalagem especial")

        valor_com_servicos = frete_component.calcular_custo()
        detalhes = frete_component.get_descricao()

        # 3. FACTORY METHOD: Criar transportadora por SLA
        factory = self.factories.get(opcao_sla, FactoryPadrao())
        nome_transp, valor_final, prazo = factory.processar_entrega(pacote, valor_com_servicos)
        self.log.registrar(f"Transportadora: {nome_transp} - Prazo: {prazo} dias")

        entrega = Entrega(
            pacote=pacote,
            valor_frete=valor_final,
            prazo_dias=prazo,
            transportadora=nome_transp,
            detalhes=detalhes
        )

        self.log.registrar(f"Cotação finalizada: R$ {valor_final:.2f}")
        return entrega


def menu_principal():
    """Menu interativo CLI"""
    config = ConfiguracaoSistema()
    log = LogSistema()
    servico = ServicoFrete()

    while True:
        print("\n" + "=" * 70)
        print(f"  {config.get_info()}")
        print("=" * 70)
        print("\n📦 MENU PRINCIPAL")
        print("1. Cotar Entrega")
        print("2. Ver Logs do Sistema")
        print("3. Sair")
        print("\n" + "-" * 70)
        print(f"Desenvolvido por: {config.get_desenvolvedor()}")
        print("-" * 70)

        opcao = input("\n➤ Escolha uma opção: ").strip()

        if opcao == "1":
            cotar_entrega_interativa(servico)
        elif opcao == "2":
            mostrar_logs(log)
        elif opcao == "3":
            print("\n👋 Encerrando sistema. Até logo!")
            break
        else:
            print("\n❌ Opção inválida!")


def cotar_entrega_interativa(servico: ServicoFrete):
    """Fluxo interativo de cotação"""
    print("\n" + "=" * 70)
    print("📦 NOVA COTAÇÃO DE ENTREGA")
    print("=" * 70)

    # Dados do pacote
    print("\n📍 Dados do Pacote:")
    origem = input("Origem: ").strip() or "São Paulo, SP"
    destino = input("Destino: ").strip() or "Rio de Janeiro, RJ"

    print("\nZonas disponíveis: local, regional, nacional")
    zona = input("Zona: ").strip() or "regional"

    try:
        peso = float(input("Peso (kg): ").strip() or "5.0")
        volume = float(input("Volume (m³): ").strip() or "0.1")
    except ValueError:
        print("❌ Valores inválidos! Usando padrões.")
        peso, volume = 5.0, 0.1

    pacote = Pacote(peso, volume, origem, destino, zona)

    # Estratégia de frete
    print("\n💰 Escolha a Estratégia de Cálculo:")
    print("1. Por Zona")
    print("2. Por Peso")
    print("3. Por Volume")
    print("4. Expresso (Janela)")
    estrategia = input("Opção: ").strip() or "1"

    # SLA (Factory)
    print("\n🚚 Escolha o SLA (Prazo):")
    print("1. Econômico (10 dias)")
    print("2. Padrão (5 dias)")
    print("3. Expresso (2 dias)")
    sla = input("Opção: ").strip() or "2"

    # Decorators (serviços)
    print("\n➕ Serviços Adicionais (separe por vírgula):")
    print("Opções: pedagio, seguro, embalagem")
    servicos_str = input("Serviços: ").strip()
    servicos = [s.strip() for s in servicos_str.split(",") if s.strip()]

    # Processar cotação
    print("\n⏳ Processando cotação...")
    entrega = servico.cotar_entrega(pacote, estrategia, sla, servicos)
    print(entrega)

    input("\n✅ Pressione ENTER para continuar...")


def mostrar_logs(log: LogSistema):
    """Exibe logs do sistema"""
    print("\n" + "=" * 70)
    print("📋 LOGS DO SISTEMA")
    print("=" * 70)
    logs = log.get_logs()
    if logs:
        for entry in logs[-10:]:  # Últimos 10 logs
            print(entry)
    else:
        print("Nenhum log registrado ainda.")
    input("\n✅ Pressione ENTER para continuar...")


# ============================================================================
# PONTO DE ENTRADA
# ============================================================================

if __name__ == "__main__":
    menu_principal()