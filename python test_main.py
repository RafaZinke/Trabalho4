
import unittest
from main import (
    Pacote,
    FretePorZona, FretePorPeso, FretePorVolume, FreteJanelaExpresso,
    FreteBasico, PedagioDecorator, SeguroDecorator, EmbalagemEspecialDecorator,
    FactoryEconomica, FactoryPadrao, FactoryExpresso,
    ConfiguracaoSistema, LogSistema,
    ServicoFrete
)


class TestStrategyPattern(unittest.TestCase):
    """Testes do padrão Strategy - Troca dinâmica de estratégias"""

    def setUp(self):
        self.pacote = Pacote(
            peso_kg=10.0,
            volume_m3=0.5,
            origem="São Paulo",
            destino="Curitiba",
            zona="regional"
        )

    def test_troca_dinamica_estrategias(self):
        """Verifica que diferentes estratégias produzem resultados diferentes"""
        estrategia_zona = FretePorZona()
        estrategia_peso = FretePorPeso()
        estrategia_volume = FretePorVolume()

        valor_zona = estrategia_zona.calcular(self.pacote)
        valor_peso = estrategia_peso.calcular(self.pacote)
        valor_volume = estrategia_volume.calcular(self.pacote)

        # Cada estratégia deve dar valor diferente
        self.assertNotEqual(valor_zona, valor_peso)
        self.assertNotEqual(valor_peso, valor_volume)
        self.assertNotEqual(valor_zona, valor_volume)

        # Valores devem ser positivos
        self.assertGreater(valor_zona, 0)
        self.assertGreater(valor_peso, 0)
        self.assertGreater(valor_volume, 0)

    def test_estrategia_por_zona(self):
        """Testa cálculo específico da estratégia por zona"""
        estrategia = FretePorZona()

        # Zona regional deve custar 35.00
        self.assertEqual(estrategia.calcular(self.pacote), 35.00)

        # Zona local
        pacote_local = Pacote(5.0, 0.2, "SP", "SP", "local")
        self.assertEqual(estrategia.calcular(pacote_local), 15.00)

        # Zona nacional
        pacote_nacional = Pacote(5.0, 0.2, "SP", "Manaus", "nacional")
        self.assertEqual(estrategia.calcular(pacote_nacional), 80.00)

    def test_estrategia_por_peso(self):
        """Testa cálculo baseado em peso"""
        estrategia = FretePorPeso()

        # 10kg * 8.50 + 10.00 base = 95.00
        resultado = estrategia.calcular(self.pacote)
        esperado = 10.0 + (10.0 * 8.50)
        self.assertEqual(resultado, esperado)

    def test_estrategia_por_volume(self):
        """Testa cálculo baseado em volume"""
        estrategia = FretePorVolume()

        # 0.5m³ * 120.00 + 12.00 base = 72.00
        resultado = estrategia.calcular(self.pacote)
        esperado = 12.0 + (0.5 * 120.00)
        self.assertEqual(resultado, esperado)

    def test_estrategia_expresso(self):
        """Testa estratégia com multiplicador expresso"""
        estrategia = FreteJanelaExpresso()
        resultado = estrategia.calcular(self.pacote)

        # Deve ser 2.5x o frete por zona (35.00 * 2.5 = 87.50)
        esperado = 35.00 * 2.5
        self.assertEqual(resultado, esperado)


class TestDecoratorPattern(unittest.TestCase):
    """Testes do padrão Decorator - Composição de serviços"""

    def setUp(self):
        self.valor_base = 50.00
        self.frete_basico = FreteBasico(self.valor_base, "Teste")

    def test_frete_basico_sem_decorators(self):
        """Testa frete básico sem decoradores"""
        self.assertEqual(self.frete_basico.calcular_custo(), self.valor_base)
        self.assertEqual(len(self.frete_basico.get_descricao()), 1)

    def test_pedagio_decorator(self):
        """Testa adição de pedágios"""
        frete_com_pedagio = PedagioDecorator(self.frete_basico, numero_pedagios=3)

        # 50.00 + (3 * 8.50) = 75.50
        esperado = 50.00 + (3 * 8.50)
        self.assertEqual(frete_com_pedagio.calcular_custo(), esperado)

        # Deve ter 2 descrições (base + pedágio)
        self.assertEqual(len(frete_com_pedagio.get_descricao()), 2)

    def test_seguro_decorator(self):
        """Testa adição de seguro"""
        frete_com_seguro = SeguroDecorator(self.frete_basico, valor_declarado=1000.00)

        # 50.00 + (1000.00 * 0.02) = 70.00
        esperado = 50.00 + (1000.00 * 0.02)
        self.assertEqual(frete_com_seguro.calcular_custo(), esperado)

    def test_embalagem_decorator(self):
        """Testa adição de embalagem especial"""
        frete_com_embalagem = EmbalagemEspecialDecorator(self.frete_basico, "reforçada")

        # 50.00 + 25.00 = 75.00
        esperado = 50.00 + 25.00
        self.assertEqual(frete_com_embalagem.calcular_custo(), esperado)

    def test_composicao_multiplos_decorators(self):
        """Testa empilhamento de múltiplos decoradores"""
        # Aplicar 3 decoradores em sequência
        frete = self.frete_basico
        frete = PedagioDecorator(frete, 2)  # +17.00
        frete = SeguroDecorator(frete, 500.00)  # +10.00
        frete = EmbalagemEspecialDecorator(frete, "térmica")  # +45.00

        # 50.00 + 17.00 + 10.00 + 45.00 = 122.00
        esperado = 50.00 + 17.00 + 10.00 + 45.00
        self.assertEqual(frete.calcular_custo(), esperado)

        # Deve ter 4 descrições (base + 3 serviços)
        self.assertEqual(len(frete.get_descricao()), 4)

    def test_ordem_decorators_nao_importa_valor(self):
        """Verifica que ordem dos decorators não afeta valor final"""
        # Ordem 1: Pedágio -> Seguro
        frete1 = PedagioDecorator(self.frete_basico, 1)
        frete1 = SeguroDecorator(frete1, 1000.00)

        # Ordem 2: Seguro -> Pedágio
        frete2 = SeguroDecorator(self.frete_basico, 1000.00)
        frete2 = PedagioDecorator(frete2, 1)

        # Valores finais devem ser iguais
        self.assertEqual(frete1.calcular_custo(), frete2.calcular_custo())


class TestFactoryMethodPattern(unittest.TestCase):
    """Testes do padrão Factory Method - Criação de transportadoras"""

    def setUp(self):
        self.pacote = Pacote(5.0, 0.2, "SP", "RJ", "regional")
        self.valor_base = 100.00

    def test_factory_economica(self):
        """Testa criação de transportadora econômica"""
        factory = FactoryEconomica()
        nome, valor, prazo = factory.processar_entrega(self.pacote, self.valor_base)

        self.assertEqual(nome, "TransLog Econômica")
        self.assertEqual(prazo, 10)
        self.assertEqual(valor, self.valor_base * 1.0)  # Sem multiplicador

    def test_factory_padrao(self):
        """Testa criação de transportadora padrão"""
        factory = FactoryPadrao()
        nome, valor, prazo = factory.processar_entrega(self.pacote, self.valor_base)

        self.assertEqual(nome, "ExpressLog Padrão")
        self.assertEqual(prazo, 5)
        self.assertEqual(valor, self.valor_base * 1.3)

    def test_factory_expresso(self):
        """Testa criação de transportadora expressa"""
        factory = FactoryExpresso()
        nome, valor, prazo = factory.processar_entrega(self.pacote, self.valor_base)

        self.assertEqual(nome, "RapidLog Express")
        self.assertEqual(prazo, 2)
        self.assertEqual(valor, self.valor_base * 1.8)

    def test_diferentes_factories_diferentes_resultados(self):
        """Verifica que factories diferentes criam produtos diferentes"""
        factory_eco = FactoryEconomica()
        factory_pad = FactoryPadrao()
        factory_exp = FactoryExpresso()

        _, valor_eco, prazo_eco = factory_eco.processar_entrega(self.pacote, self.valor_base)
        _, valor_pad, prazo_pad = factory_pad.processar_entrega(self.pacote, self.valor_base)
        _, valor_exp, prazo_exp = factory_exp.processar_entrega(self.pacote, self.valor_base)

        # Valores devem ser diferentes
        self.assertNotEqual(valor_eco, valor_pad)
        self.assertNotEqual(valor_pad, valor_exp)

        # Prazos devem ser diferentes
        self.assertNotEqual(prazo_eco, prazo_pad)
        self.assertNotEqual(prazo_pad, prazo_exp)

        # Prazo expresso < padrão < econômico
        self.assertLess(prazo_exp, prazo_pad)
        self.assertLess(prazo_pad, prazo_eco)

    def test_facil_adicionar_nova_factory(self):
        """Demonstra facilidade de adicionar nova factory"""
        # Simula adição de nova factory sem modificar código existente
        from main import TransportadoraFactory, Transportadora

        class TransportadoraSuperExpresso(Transportadora):
            def get_nome(self):
                return "Ultra Express"

            def get_prazo_dias(self):
                return 1

            def get_multiplicador_preco(self):
                return 2.5

        class FactorySuperExpresso(TransportadoraFactory):
            def criar_transportadora(self):
                return TransportadoraSuperExpresso()

        factory = FactorySuperExpresso()
        nome, valor, prazo = factory.processar_entrega(self.pacote, self.valor_base)

        self.assertEqual(nome, "Ultra Express")
        self.assertEqual(prazo, 1)
        self.assertEqual(valor, self.valor_base * 2.5)


class TestSingletonPattern(unittest.TestCase):
    """Testes do padrão Singleton - Unicidade de instâncias"""

    def test_configuracao_singleton_unicidade(self):
        """Verifica que ConfiguracaoSistema sempre retorna mesma instância"""
        config1 = ConfiguracaoSistema()
        config2 = ConfiguracaoSistema()
        config3 = ConfiguracaoSistema()

        # Todas devem ser a mesma instância (mesmo id)
        self.assertIs(config1, config2)
        self.assertIs(config2, config3)
        self.assertEqual(id(config1), id(config2))
        self.assertEqual(id(config2), id(config3))

    def test_log_singleton_unicidade(self):
        """Verifica que LogSistema sempre retorna mesma instância"""
        log1 = LogSistema()
        log2 = LogSistema()
        log3 = LogSistema()

        self.assertIs(log1, log2)
        self.assertIs(log2, log3)

    def test_singleton_mantem_estado(self):
        """Verifica que Singleton mantém estado entre chamadas"""
        log1 = LogSistema()
        log1.registrar("Teste 1")

        log2 = LogSistema()
        log2.registrar("Teste 2")

        # Ambas instâncias devem ter os 2 logs
        self.assertGreaterEqual(len(log1.get_logs()), 2)
        self.assertGreaterEqual(len(log2.get_logs()), 2)
        self.assertEqual(log1.get_logs(), log2.get_logs())

    def test_configuracao_valores_consistentes(self):
        """Verifica consistência de valores em múltiplas chamadas"""
        config1 = ConfiguracaoSistema()
        versao1 = config1.versao
        dev1 = config1.desenvolvedor

        config2 = ConfiguracaoSistema()
        versao2 = config2.versao
        dev2 = config2.desenvolvedor

        self.assertEqual(versao1, versao2)
        self.assertEqual(dev1, dev2)


class TestIntegracaoCompleta(unittest.TestCase):
    """Testes de integração entre todos os padrões"""

    def test_fluxo_completo_cotacao(self):
        """Testa fluxo completo usando todos os padrões"""
        servico = ServicoFrete()

        pacote = Pacote(
            peso_kg=15.0,
            volume_m3=0.8,
            origem="São Paulo",
            destino="Rio de Janeiro",
            zona="regional"
        )

        # Cotar com Strategy por zona, Decorator com pedágio, Factory padrão
        entrega = servico.cotar_entrega(
            pacote=pacote,
            opcao_estrategia="1",  # Por zona
            opcao_sla="2",  # Padrão
            servicos_adicionais=["pedagio", "seguro"]
        )

        # Verificações
        self.assertIsNotNone(entrega)
        self.assertGreater(entrega.valor_frete, 0)
        self.assertGreater(entrega.prazo_dias, 0)
        self.assertIsNotNone(entrega.transportadora)
        self.assertGreater(len(entrega.detalhes), 0)

    def test_diferentes_combinacoes(self):
        """Testa múltiplas combinações de padrões"""
        servico = ServicoFrete()

        pacote = Pacote(8.0, 0.3, "Curitiba", "Florianópolis", "local")

        # Combinação 1: Peso + Expresso + Embalagem
        entrega1 = servico.cotar_entrega(pacote, "2", "3", ["embalagem"])

        # Combinação 2: Volume + Econômico + Todos serviços
        entrega2 = servico.cotar_entrega(pacote, "3", "1", ["pedagio", "seguro", "embalagem"])

        # Valores devem ser diferentes
        self.assertNotEqual(entrega1.valor_frete, entrega2.valor_frete)
        self.assertNotEqual(entrega1.prazo_dias, entrega2.prazo_dias)


class TestCasosBorda(unittest.TestCase):
    """Testes de casos extremos e validações"""

    def test_pacote_peso_zero(self):
        """Testa comportamento com peso zero"""
        pacote = Pacote(0, 0.1, "SP", "RJ", "local")
        estrategia = FretePorPeso()
        valor = estrategia.calcular(pacote)
        self.assertGreater(valor, 0)  # Deve ter taxa base

    def test_decorator_sem_servicos(self):
        """Testa que decorator funciona sem serviços adicionais"""
        servico = ServicoFrete()
        pacote = Pacote(5.0, 0.2, "SP", "RJ", "regional")

        entrega = servico.cotar_entrega(pacote, "1", "2", [])
        self.assertGreater(entrega.valor_frete, 0)

    def test_zona_invalida(self):
        """Testa comportamento com zona inválida"""
        pacote = Pacote(5.0, 0.2, "SP", "RJ", "zona_inexistente")
        estrategia = FretePorZona()
        valor = estrategia.calcular(pacote)
        self.assertEqual(valor, 50.00)  # Valor padrão


def run_tests():
    """Executa todos os testes e mostra relatório"""
    print("\n" + "=" * 70)
    print(" EXECUTANDO TESTES UNITÁRIOS")
    print("=" * 70 + "\n")

    # Criar suite de testes
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Adicionar todos os testes
    suite.addTests(loader.loadTestsFromTestCase(TestStrategyPattern))
    suite.addTests(loader.loadTestsFromTestCase(TestDecoratorPattern))
    suite.addTests(loader.loadTestsFromTestCase(TestFactoryMethodPattern))
    suite.addTests(loader.loadTestsFromTestCase(TestSingletonPattern))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegracaoCompleta))
    suite.addTests(loader.loadTestsFromTestCase(TestCasosBorda))

    # Executar testes
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Relatório final
    print("\n" + "=" * 70)
    print(" RELATÓRIO DE TESTES")
    print("=" * 70)
    print(f" Testes executados: {result.testsRun}")
    print(f" Sucessos: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f" Falhas: {len(result.failures)}")
    print(f" Erros: {len(result.errors)}")
    print("=" * 70 + "\n")

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)