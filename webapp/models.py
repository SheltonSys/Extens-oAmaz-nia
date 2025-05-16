from django.db import models

# 1. Artesãs
class Artesa(models.Model):
    nome = models.CharField(max_length=100)
    idade = models.IntegerField()
    escolaridade = models.CharField(max_length=50)
    pessoas_na_casa = models.IntegerField()
    familiares_na_producao = models.IntegerField()
    renda_artesanato = models.CharField(max_length=50)

    tipos_producao = models.TextField(null=True, blank=True)
    tempo_artesanato = models.CharField(max_length=50, null=True, blank=True)
    forma_aprendizado = models.CharField(max_length=100, null=True, blank=True)

    pontos_fortes = models.TextField(null=True, blank=True)
    formas_venda = models.TextField(null=True, blank=True)
    material_divulgacao = models.BooleanField(default=False)
    interesse_feiras = models.BooleanField(default=False)

    dificuldades_producao = models.TextField(null=True, blank=True)
    dificuldades_venda = models.TextField(null=True, blank=True)
    apoios_recebidos = models.TextField(null=True, blank=True)

    apoio_producao = models.TextField(null=True, blank=True)
    apoio_venda = models.TextField(null=True, blank=True)
    fala_artesa = models.TextField(null=True, blank=True)

    foto_evidencia = models.ImageField(upload_to='artesas/fotos/', null=True, blank=True)

    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome


######################***********************************************************************************************************

from django.db import models

class CanalComercializacao(models.Model):
    responsavel = models.CharField(max_length=100)
    data = models.DateField()
    comunidade = models.CharField(max_length=100)
    nome_entrevistado = models.CharField(max_length=100)

    # Campos estruturados em formato JSON
    canais_identificados = models.TextField(null=True, blank=True)       # Lista de canais (JSON)
    rota_nome = models.CharField(max_length=100, null=True, blank=True)
    rota_itinerario = models.TextField(null=True, blank=True)            # Lista de paradas (JSON)
    transporte_embalagem = models.TextField(null=True, blank=True)       # Lista de transportes/embalagens (JSON)
    produtores_inseridos = models.TextField(null=True, blank=True)       # Lista de produtores (JSON)

    # Campos simples adicionais
    pontos_parada = models.TextField(null=True, blank=True)

    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.responsavel} - {self.comunidade} ({self.data.strftime('%d/%m/%Y')})"



######################***********************************************************************************************************

from django.db import models

class Feirante(models.Model):
    nome_feira = models.CharField(max_length=100)
    local = models.CharField(max_length=100)
    periodicidade = models.CharField(max_length=50)
    produtos = models.TextField()
    volume = models.CharField(max_length=50)

    beneficios = models.TextField()  # JSON - múltiplas opções
    contribuicao = models.TextField()  # JSON
    fortalecimento = models.TextField()  # JSON
    produtos_mais_vendidos = models.TextField()  # JSON
    estrutura_apropriada = models.CharField(max_length=255)  # radio button

    dificuldades = models.TextField()  # JSON
    comunicacao = models.CharField(max_length=100)  # radio button
    apoio_institucional = models.TextField(null=True, blank=True)
    problemas_aceitacao = models.TextField(null=True, blank=True)
    sugestoes = models.TextField(null=True, blank=True)

    foto_evidencia = models.ImageField(upload_to='feirantes/fotos/', null=True, blank=True)

    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome_feira


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
    custos_principais = models.TextField(blank=True, null=False, default='')
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
    apoio_publico = models.TextField(blank=True, null=True)
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