from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from .models import Feirante
from .models import Agricultor
from .models import Artesa
from .models import CanalComercializacao
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import Artesa, CanalComercializacao, Feirante, Agricultor

from django.http import HttpResponse
from .models import Evento
from datetime import datetime

import base64
from django.core.files.base import ContentFile





####**************************************************************************************************************************************

def BASE(request):
    return render(request, 'base.html')
####**************************************************************************************************************************************

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = LoginForm

####**************************************************************************************************************************************

# @login_required
# def dashboard(request):
#     return render(request, 'dashboard.html')

####**************************************************************************************************************************************

from .models import Artesa, CanalComercializacao, Feirante, Agricultor, Evento

def dashboard(request):
    # Tabela
    resumo_categorias = [
        {'Categoria': 'Artesãs', 'Total': Artesa.objects.count(), 'Novos': 3},
        {'Categoria': 'Canais', 'Total': CanalComercializacao.objects.count(), 'Novos': 2},
        {'Categoria': 'Feirantes', 'Total': Feirante.objects.count(), 'Novos': 1},
        {'Categoria': 'Agricultores', 'Total': Agricultor.objects.count(), 'Novos': 5},
    ]

    # Eventos
    eventos = Evento.objects.all().order_by('data')
    calendario_eventos = [{'Data': e.data, 'Evento': e.titulo} for e in eventos]

    # Cards
    cards = [
        {'categoria': 'Artesãs', 'total': Artesa.objects.count(), 'cor': 'info', 'icon': 'fas fa-female', 'url': 'cadastrar_artesa', 'label': 'Cadastrar'},
        {'categoria': 'Canais de Comercialização', 'total': CanalComercializacao.objects.count(), 'cor': 'success', 'icon': 'fas fa-store', 'url': 'cadastrar_canal', 'label': 'Cadastrar'},
        {'categoria': 'Feirantes', 'total': Feirante.objects.count(), 'cor': 'warning', 'icon': 'fas fa-people-carry', 'url': 'cadastrar_feirante', 'label': 'Cadastrar'},
        {'categoria': 'Agricultores', 'total': Agricultor.objects.count(), 'cor': 'danger', 'icon': 'fas fa-tractor', 'url': 'cadastrar_agricultor', 'label': 'Cadastrar'},
    ]

    # Simula dados — substitua depois com queries reais
    renda = ['até R$300', 'R$301–600', 'R$601–1.000', 'R$601–1.000']
    canais = ['Feira', 'Comércio', 'Online', 'Feira']
    periodicidade = ['Semanal', 'Mensal', 'Semanal']
    credito = ['Sim', 'Não', 'Sim', 'Sim']

    grafico_renda = gerar_grafico_base64("Renda do Artesanato", list(Counter(renda).keys()), list(Counter(renda).values()))
    grafico_canais = gerar_grafico_base64("Tipos de Canais", list(Counter(canais).keys()), list(Counter(canais).values()))
    grafico_feiras = gerar_grafico_base64("Periodicidade das Feiras", list(Counter(periodicidade).keys()), list(Counter(periodicidade).values()))
    grafico_credito = gerar_grafico_base64("Acesso ao Crédito", list(Counter(credito).keys()), list(Counter(credito).values()))
    grafico_barras = gerar_grafico_base64("Comparativo Geral", [c['Categoria'] for c in resumo_categorias], [c['Total'] for c in resumo_categorias])

    graficos = [
        {'titulo': 'Renda do Artesanato', 'cor': 'info', 'icon': 'fas fa-female', 'imagem': grafico_renda},
        {'titulo': 'Tipos de Canais', 'cor': 'success', 'icon': 'fas fa-store', 'imagem': grafico_canais},
        {'titulo': 'Periodicidade das Feiras', 'cor': 'warning', 'icon': 'fas fa-people-carry', 'imagem': grafico_feiras},
        {'titulo': 'Acesso ao Crédito', 'cor': 'danger', 'icon': 'fas fa-tractor', 'imagem': grafico_credito},
    ]

    context = {
        'cards': cards,
        'graficos': graficos,
        'grafico_barras': grafico_barras,
        'resumo_categorias': resumo_categorias,
        'calendario_eventos': calendario_eventos,
    }
    return render(request, 'dashboard.html', context)



####**************************************************************************************************************************************

from django.shortcuts import render, redirect
from .models import Artesa

def cadastrar_artesa(request):
    if request.method == 'POST':
        foto_base64 = request.POST.get('foto_base64')

        artesa = Artesa(
            nome=request.POST.get('nome'),
            idade=request.POST.get('idade'),
            escolaridade=request.POST.get('escolaridade'),
            pessoas_na_casa=request.POST.get('pessoas_na_casa'),
            familiares_na_producao=request.POST.get('familiares_na_producao'),
            renda_artesanato=request.POST.get('renda_artesanato'),

            tipos_producao=', '.join(request.POST.getlist('tipos_producao[]')),
            tempo_artesanato=request.POST.get('tempo_artesanato'),
            forma_aprendizado=', '.join(request.POST.getlist('forma_aprendizado[]')),

            pontos_fortes=', '.join(request.POST.getlist('pontos_fortes[]')),
            formas_venda=', '.join(request.POST.getlist('formas_venda[]')),
            material_divulgacao=bool(request.POST.get('material_divulgacao')),
            interesse_feiras=bool(request.POST.get('interesse_feiras')),

            dificuldades_producao=', '.join(request.POST.getlist('dificuldades_producao[]')),
            dificuldades_venda=', '.join(request.POST.getlist('dificuldades_venda[]')),
            apoios_recebidos=', '.join(request.POST.getlist('apoios_recebidos[]')),

            apoio_producao=', '.join(request.POST.getlist('apoio_producao[]')),
            apoio_venda=', '.join(request.POST.getlist('apoio_venda[]')),
            fala_artesa=request.POST.get('fala_artesa'),
        )

        # Converte base64 para imagem e salva
        if foto_base64 and foto_base64.startswith('data:image'):
            format, imgstr = foto_base64.split(';base64,')
            ext = format.split('/')[-1]
            image_data = ContentFile(base64.b64decode(imgstr), name=f"{artesa.nome}_foto.{ext}")
            artesa.foto_evidencia = image_data

        artesa.save()
        return redirect('dashboard')

    return render(request, 'cadastros/cadastrar_artesa.html')


####**************************************************************************************************************************************

import json  # necessário para salvar como JSON

def cadastrar_canal(request):
    if request.method == 'POST':
        # --- Canais Identificados ---
        canais_zip = zip(
            request.POST.getlist('canal_canal[]'),
            request.POST.getlist('canal_tipo[]'),
            request.POST.getlist('canal_nome[]'),
            request.POST.getlist('canal_volume[]'),
            request.POST.getlist('canal_obs[]')
        )

        canais_identificados = []
        for canal, tipo, nome, volume, obs in canais_zip:
            if canal or nome:
                canais_identificados.append({
                    'canal': canal,
                    'tipo': tipo,
                    'nome': nome,
                    'volume': volume,
                    'observacao': obs
                })
        canais_identificados_json = json.dumps(canais_identificados)

        # --- Itinerário da Rota ---
        paradas_zip = zip(
            request.POST.getlist('parada_ponto[]'),
            request.POST.getlist('parada_tempo[]'),
            request.POST.getlist('parada_obs[]')
        )

        rota_itinerario = []
        for ponto, tempo, obs in paradas_zip:
            if ponto or tempo or obs:
                rota_itinerario.append({
                    'ponto': ponto,
                    'tempo': tempo,
                    'observacao': obs
                })
        rota_itinerario_json = json.dumps(rota_itinerario)

        # --- Transporte e Embalagem ---
        transporte_zip = zip(
            request.POST.getlist('transporte_tipo[]'),
            request.POST.getlist('embalagem_tipo[]'),
            request.POST.getlist('transporte_obs[]')
        )

        transporte_embalagem = []
        for transporte, embalagem, obs in transporte_zip:
            if transporte or embalagem or obs:
                transporte_embalagem.append({
                    'transporte': transporte,
                    'embalagem': embalagem,
                    'observacao': obs
                })
        transporte_embalagem_json = json.dumps(transporte_embalagem)

        # --- Produtores Inseridos ---
        produtores_zip = zip(
            request.POST.getlist('produtor_nome[]'),
            request.POST.getlist('produtor_comunidade[]')
        )

        produtores_inseridos = []
        for nome, comunidade in produtores_zip:
            if nome or comunidade:
                produtores_inseridos.append({
                    'nome': nome,
                    'comunidade': comunidade
                })
        produtores_inseridos_json = json.dumps(produtores_inseridos)

        # --- Captura segura para pontos_parada ---
        pontos_parada = request.POST.get('pontos_parada', '').strip()
        if not pontos_parada:
            pontos_parada = 'Não informado'

        # --- Salvar tudo no banco ---
        canal = CanalComercializacao(
            responsavel=request.POST.get('responsavel'),
            data=request.POST.get('data'),
            comunidade=request.POST.get('comunidade'),
            nome_entrevistado=request.POST.get('nome_entrevistado'),
            canais_identificados=canais_identificados_json,
            rota_nome=request.POST.get('rota_nome'),
            rota_itinerario=rota_itinerario_json,
            pontos_parada=pontos_parada,
            transporte_embalagem=transporte_embalagem_json,
            produtores_inseridos=produtores_inseridos_json
        )
        canal.save()
        return redirect('dashboard')

    return render(request, 'cadastros/cadastrar_canal.html')




####**************************************************************************************************************************************

import json
import base64
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from .models import Feirante

def cadastrar_feirante(request):
    if request.method == 'POST':
        foto_base64 = request.POST.get('foto_base64')

        feirante = Feirante(
            nome_feira=request.POST.get('nome_feira'),
            local=request.POST.get('local'),
            periodicidade=request.POST.get('periodicidade'),
            produtos=request.POST.get('produtos'),
            volume=request.POST.get('volume'),

            beneficios=json.dumps(request.POST.getlist('beneficios[]')),
            contribuicao=json.dumps(request.POST.getlist('contribuicao[]')),
            fortalecimento=json.dumps(request.POST.getlist('fortalecimento[]')),
            produtos_mais_vendidos=json.dumps(request.POST.getlist('produtos_aceitacao[]')),
            estrutura_apropriada=request.POST.get('estrutura_feira'),

            dificuldades=json.dumps(request.POST.getlist('dificuldades[]')),
            comunicacao=request.POST.get('comunicacao'),
            apoio_institucional=request.POST.get('apoio_institucional'),
            problemas_aceitacao=request.POST.get('problemas_aceitacao'),
            sugestoes=request.POST.get('sugestoes')
        )

        # Salva a imagem se vier via base64
        if foto_base64 and foto_base64.startswith('data:image'):
            format, imgstr = foto_base64.split(';base64,')
            ext = format.split('/')[-1]
            image_data = ContentFile(base64.b64decode(imgstr), name=f"{feirante.nome_feira}_foto.{ext}")
            feirante.foto_evidencia = image_data

        feirante.save()
        return redirect('dashboard')  # ou outro destino

    return render(request, 'cadastros/cadastrar_feirante.html')


####**************************************************************************************************************************************


def cadastrar_agricultor(request):
    nome_entrevistador = request.user.get_full_name() or request.user.username
    if not nome_entrevistador.strip():
        nome_entrevistador = request.user.username

    if request.method == 'POST':
        # Captura e formata os custos principais (checkboxes)
        custos = request.POST.getlist('custos_principais[]')
        custos_str = ", ".join(custos) if custos else "Nenhum"

        agricultor = Agricultor(
            local_feira=request.POST.get('local_feira'),
            data=request.POST.get('data'),
            entrevistador=nome_entrevistador,
            numero_ficha=request.POST.get('numero_ficha'),

            idade=request.POST.get('idade'),
            sexo=request.POST.get('sexo'),
            escolaridade=request.POST.get('escolaridade'),
            cidade_origem=request.POST.get('cidade_origem'),
            tempo_feira=request.POST.get('tempo_feira'),
            varias_feiras=bool(request.POST.get('varias_feiras')),

            trabalha_familiares=bool(request.POST.get('trabalha_familiares')),
            qtd_familiares=request.POST.get('qtd_familiares'),
            grau_parentesco=request.POST.get('grau_parentesco'),
            criancas_ajudam=bool(request.POST.get('criancas_ajudam')),
            atividades_criancas=request.POST.get('atividades_criancas'),
            idosos_ajudam=bool(request.POST.get('idosos_ajudam')),
            atividades_idosos=request.POST.get('atividades_idosos'),

            produto_principal=request.POST.get('produto_principal'),
            origem_produto=request.POST.get('origem_produto'),
            faturamento=request.POST.get('faturamento'),
            custos_principais=custos_str,
            renda_varia=bool(request.POST.get('renda_varia')),
            meses_bons=request.POST.get('meses_bons'),
            meses_fracos=request.POST.get('meses_fracos'),

            acesso=request.POST.get('acesso'),
            agua=bool(request.POST.get('agua')),
            banheiro=bool(request.POST.get('banheiro')),
            higiene=request.POST.get('higiene'),
            seguranca=bool(request.POST.get('seguranca')),
            motivo_inseguranca=request.POST.get('motivo_inseguranca'),

            associacao=bool(request.POST.get('associacao')),
            nome_associacao=request.POST.get('nome_associacao'),
            capacitacao=bool(request.POST.get('capacitacao')),
            capacitador=request.POST.get('capacitador'),
            apoio_publico=request.POST.get('apoio_publico') or '',
            acesso_credito=bool(request.POST.get('acesso_credito')),
            instituicao_credito=request.POST.get('instituicao_credito'),
        )
        agricultor.save()
        return redirect('dashboard')

    # Enviar listas para o template (caso queira usá-las em loop no HTML)
    contexto = {
        'opcoes_acesso': ['Muito bom', 'Bom', 'Regular', 'Ruim', 'Muito ruim'],
        'opcoes_higiene': ['Boa', 'Regular', 'Ruim'],
    }
    return render(request, 'cadastros/cadastrar_agricultor.html', contexto)

####**************************************************************************************************************************************

def listar_artesas(request):
    artesas = Artesa.objects.all().order_by('-id')
    return render(request, 'cadastros/listar_artesas.html', {'artesas': artesas})
####**************************************************************************************************************************************

from django.shortcuts import render
import json
from .models import CanalComercializacao

def listar_canais(request):
    canais = CanalComercializacao.objects.all().order_by('-data')

    for canal in canais:
        try:
            canal.transporte_embalagem = json.loads(canal.transporte_embalagem or '[]')
        except:
            canal.transporte_embalagem = []

    return render(request, 'cadastros/listar_canais.html', {'canais': canais})

####**************************************************************************************************************************************

import json
from .models import Feirante

def listar_feirantes(request):
    feirantes = Feirante.objects.all()

    for f in feirantes:
        try:
            f.beneficios_lista = json.loads(f.beneficios or '[]')
        except:
            f.beneficios_lista = ['[Erro ao carregar]']

    return render(request, 'cadastros/listar_feirantes.html', {'feirantes': feirantes})

####**************************************************************************************************************************************

def listar_agricultores(request):
    agricultores = Agricultor.objects.all()
    return render(request, 'cadastros/listar_agricultores.html', {'agricultores': agricultores})
####**************************************************************************************************************************************

from django.shortcuts import redirect

def cadastrar_evento(request):
    if request.method == 'POST':
        Evento.objects.create(
            data=request.POST.get('data'),
            titulo=request.POST.get('titulo'),
            local=request.POST.get('local'),
            descricao=request.POST.get('descricao')
        )
        return redirect('/eventos/cadastrar/?sucesso=1')
    return render(request, 'eventos/cadastrar_evento.html')

####**************************************************************************************************************************************

def listar_eventos(request):
    eventos = Evento.objects.order_by('data')
    return render(request, 'eventos/listar_eventos.html', {'eventos': eventos})
####**************************************************************************************************************************************

def relatorio_geral(request):
    return render(request, 'relatorios/relatorio_geral.html')
####**************************************************************************************************************************************

def relatorio_pdf(request):
    return HttpResponse("Relatório PDF gerado (exemplo)", content_type="application/pdf")

####**************************************************************************************************************************************

from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from datetime import date
from .models import Artesa, CanalComercializacao, Feirante, Agricultor

def relatorio_pdf(request):
    resumo_categorias = [
        {'Categoria': 'Artesãs', 'Total': Artesa.objects.count(), 'Novos': 3},
        {'Categoria': 'Canais', 'Total': CanalComercializacao.objects.count(), 'Novos': 2},
        {'Categoria': 'Feirantes', 'Total': Feirante.objects.count(), 'Novos': 1},
        {'Categoria': 'Agricultores', 'Total': Agricultor.objects.count(), 'Novos': 5},
    ]

    calendario_eventos = [
        {'Data': '2025-05-03', 'Evento': 'Feira Local - Bairro A'},
        {'Data': '2025-05-10', 'Evento': 'Capacitação Artesanato'},
        {'Data': '2025-05-17', 'Evento': 'Encontro de Agricultores'},
        {'Data': '2025-05-24', 'Evento': 'Entrega de Insumos'},
        {'Data': '2025-05-31', 'Evento': 'Evento de Comercialização'},
    ]

    context = {
        'resumo_categorias': resumo_categorias,
        'calendario_eventos': calendario_eventos,
        'data_hoje': date.today(),
    }

    html_string = render_to_string('relatorio_pdf.html', context)
    html = HTML(string=html_string)
    pdf_file = html.write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="relatorio_extensao.pdf"'
    return response

from django.shortcuts import render, get_object_or_404, redirect
from .models import Evento

def visualizar_evento(request, id):
    evento = get_object_or_404(Evento, id=id)
    return render(request, 'eventos/visualizar_evento.html', {'evento': evento})

def editar_evento(request, id):
    evento = get_object_or_404(Evento, id=id)
    if request.method == 'POST':
        evento.data = request.POST.get('data')
        evento.titulo = request.POST.get('titulo')
        evento.local = request.POST.get('local')
        evento.descricao = request.POST.get('descricao')
        evento.save()
        return redirect('listar_eventos')
    return render(request, 'eventos/editar_evento.html', {'evento': evento})

def excluir_evento(request, id):
    evento = get_object_or_404(Evento, id=id)
    if request.method == 'POST':
        evento.delete()
        return redirect('listar_eventos')
    return render(request, 'eventos/confirmar_exclusao.html', {'evento': evento})


from django.contrib.auth.models import User  # ou CustomUser, se for personalizado
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

def listar_usuarios(request):
    usuarios = User.objects.all()
    return render(request, 'usuarios/listar_usuarios.html', {'usuarios': usuarios})


from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages

def adicionar_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Usuário já existe.')
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password,
                is_active=True
            )
            messages.success(request, 'Usuário criado com sucesso.')
            return redirect('listar_usuarios')

    return render(request, 'usuarios/adicionar_usuario.html')



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.models import User

def editar_usuario(request, usuario_id):
    usuario = get_object_or_404(User, id=usuario_id)
    if request.method == 'POST':
        usuario.first_name = request.POST.get('first_name')
        usuario.last_name = request.POST.get('last_name')
        usuario.email = request.POST.get('email')
        usuario.is_active = bool(request.POST.get('is_active'))
        usuario.save()
        messages.success(request, 'Usuário atualizado com sucesso!')
        return redirect('listar_usuarios')
    return render(request, 'usuarios/editar_usuario.html', {'usuario': usuario})



def excluir_usuario(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    usuario.delete()
    messages.success(request, 'Usuário removido com sucesso!')
    return redirect('listar_usuarios')


import matplotlib
matplotlib.use('Agg')  # <--- ESSA LINHA RESOLVE O ERRO
import matplotlib.pyplot as plt
import io
import base64
from collections import Counter

def gerar_grafico_base64(titulo, labels, dados):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(labels, dados, color='skyblue')
    ax.set_title(titulo)
    ax.set_ylabel('Quantidade')
    ax.set_xlabel('Categorias')
    ax.tick_params(axis='x', rotation=30)

    plt.tight_layout()
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close(fig)
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode('utf-8')


