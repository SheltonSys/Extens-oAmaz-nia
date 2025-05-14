from django.db import models

# 1. Artesãs
class Artesa(models.Model):
    nome = models.CharField(max_length=100)
    idade = models.IntegerField()
    escolaridade = models.CharField(max_length=50)
    pessoas_na_casa = models.IntegerField()
    familiares_na_producao = models.IntegerField()
    renda_artesanato = models.CharField(max_length=50)

    tipos_producao = models.TextField()
    tempo_artesanato = models.CharField(max_length=50)
    forma_aprendizado = models.CharField(max_length=100)

    pontos_fortes = models.TextField()
    formas_venda = models.TextField()
    material_divulgacao = models.BooleanField()
    interesse_feiras = models.BooleanField()

    dificuldades_producao = models.TextField()
    dificuldades_venda = models.TextField()
    apoios_recebidos = models.TextField()

    apoio_producao = models.TextField()
    apoio_venda = models.TextField()
    fala_artesa = models.TextField(blank=True)

    data_cadastro = models.DateTimeField(auto_now_add=True)
######################***********************************************************************************************************

# 2. Canais de comercialização
class CanalComercializacao(models.Model):
    responsavel = models.CharField(max_length=100)
    data = models.DateField()
    comunidade = models.CharField(max_length=100)
    nome_entrevistado = models.CharField(max_length=100)

    canais_identificados = models.TextField()
    rota_nome = models.CharField(max_length=100)
    rota_itinerario = models.TextField()
    pontos_parada = models.TextField()
    transporte_embalagem = models.TextField()
    produtores_inseridos = models.TextField()

    data_cadastro = models.DateTimeField(auto_now_add=True)
######################***********************************************************************************************************

# 3. Feirantes
class Feirante(models.Model):
    nome_feira = models.CharField(max_length=100)
    local = models.CharField(max_length=100)
    periodicidade = models.CharField(max_length=50)
    produtos = models.TextField()
    volume = models.CharField(max_length=50)

    beneficios = models.TextField()
    contribuicao = models.TextField()
    fortalecimento = models.TextField()
    produtos_mais_vendidos = models.TextField()
    estrutura_apropriada = models.CharField(max_length=255)

    dificuldades = models.TextField()
    comunicacao = models.CharField(max_length=100)
    apoio_institucional = models.TextField()
    problemas_aceitacao = models.TextField()
    sugestoes = models.TextField()

    data_cadastro = models.DateTimeField(auto_now_add=True)
######################***********************************************************************************************************

# 4. Agricultores
class Agricultor(models.Model):
    local_feira = models.CharField(max_length=100)
    data = models.DateField()
    entrevistador = models.CharField(max_length=100)
    numero_ficha = models.CharField(max_length=50)

    idade = models.IntegerField()
    sexo = models.CharField(max_length=20)
    escolaridade = models.CharField(max_length=50)
    cidade_origem = models.CharField(max_length=100)
    tempo_feira = models.CharField(max_length=50)
    varias_feiras = models.BooleanField()

    trabalha_familiares = models.BooleanField()
    qtd_familiares = models.IntegerField()
    grau_parentesco = models.TextField()
    criancas_ajudam = models.BooleanField()
    atividades_criancas = models.TextField(blank=True)
    idosos_ajudam = models.BooleanField()
    atividades_idosos = models.TextField(blank=True)

    produto_principal = models.CharField(max_length=100)
    origem_produto = models.CharField(max_length=50)
    faturamento = models.CharField(max_length=50)
    custos_principais = models.TextField()
    renda_varia = models.BooleanField()
    meses_bons = models.TextField()
    meses_fracos = models.TextField()

    acesso = models.CharField(max_length=50)
    agua = models.BooleanField()
    banheiro = models.BooleanField()
    higiene = models.CharField(max_length=50)
    seguranca = models.BooleanField()
    motivo_inseguranca = models.TextField(blank=True)

    associacao = models.BooleanField()
    nome_associacao = models.CharField(max_length=100, blank=True)
    capacitacao = models.BooleanField()
    capacitador = models.CharField(max_length=100, blank=True)
    apoio_publico = models.TextField()
    acesso_credito = models.BooleanField()
    instituicao_credito = models.CharField(max_length=100, blank=True)

    data_cadastro = models.DateTimeField(auto_now_add=True)
######################***********************************************************************************************************

class Evento(models.Model):
    data = models.DateField()
    titulo = models.CharField(max_length=255)
    local = models.CharField(max_length=255)
    descricao = models.TextField(blank=True)


    def __str__(self):
        return f"{self.data} - {self.evento}"
######################***********************************************************************************************************