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

from django.shortcuts import render
from .models import Artesa, CanalComercializacao, Feirante, Agricultor, Evento

def dashboard(request):
    # Resumo para tabela
    resumo_categorias = [
        {'Categoria': 'Artesãs', 'Total': Artesa.objects.count(), 'Novos': 3},
        {'Categoria': 'Canais', 'Total': CanalComercializacao.objects.count(), 'Novos': 2},
        {'Categoria': 'Feirantes', 'Total': Feirante.objects.count(), 'Novos': 1},
        {'Categoria': 'Agricultores', 'Total': Agricultor.objects.count(), 'Novos': 5},
    ]

    # Busca eventos do banco ordenados por data
    eventos = Evento.objects.all().order_by('data')
    calendario_eventos = [
        {'Data': e.data, 'Evento': e.titulo} for e in eventos
    ]

    # Cards principais
    cards = [
        {'categoria': 'Artesãs', 'total': Artesa.objects.count(), 'cor': 'info', 'icon': 'fas fa-female', 'url': 'cadastrar_artesa', 'label': 'Cadastrar'},
        {'categoria': 'Canais de Comercialização', 'total': CanalComercializacao.objects.count(), 'cor': 'success', 'icon': 'fas fa-store', 'url': 'cadastrar_canal', 'label': 'Cadastrar'},
        {'categoria': 'Feirantes', 'total': Feirante.objects.count(), 'cor': 'warning', 'icon': 'fas fa-people-carry', 'url': 'cadastrar_feirante', 'label': 'Cadastrar'},
        {'categoria': 'Agricultores', 'total': Agricultor.objects.count(), 'cor': 'danger', 'icon': 'fas fa-tractor', 'url': 'cadastrar_agricultor', 'label': 'Cadastrar'},
    ]

    # Gráficos simulados
    graficos = [
        {'titulo': 'Renda do Artesanato', 'cor': 'info', 'icon': 'fas fa-female', 'imagem': '<base64>'},
        {'titulo': 'Tipos de Canais', 'cor': 'success', 'icon': 'fas fa-store', 'imagem': '<base64>'},
        {'titulo': 'Periodicidade das Feiras', 'cor': 'warning', 'icon': 'fas fa-people-carry', 'imagem': '<base64>'},
        {'titulo': 'Acesso ao Crédito', 'cor': 'danger', 'icon': 'fas fa-tractor', 'imagem': '<base64>'},
    ]

    context = {
        'cards': cards,
        'graficos': graficos,
        'grafico_barras': '<base64>',
        'resumo_categorias': resumo_categorias,
        'calendario_eventos': calendario_eventos,
    }
    return render(request, 'dashboard.html', context)


####**************************************************************************************************************************************

def cadastrar_artesa(request):
    if request.method == 'POST':
        artesa = Artesa(
            nome=request.POST.get('nome'),
            idade=request.POST.get('idade'),
            escolaridade=request.POST.get('escolaridade'),
            pessoas_na_casa=request.POST.get('pessoas_na_casa'),
            familiares_na_producao=request.POST.get('familiares_na_producao'),
            renda_artesanato=request.POST.get('renda_artesanato'),

            tipos_producao=request.POST.get('tipos_producao'),
            tempo_artesanato=request.POST.get('tempo_artesanato'),
            forma_aprendizado=request.POST.get('forma_aprendizado'),

            pontos_fortes=request.POST.get('pontos_fortes'),
            formas_venda=request.POST.get('formas_venda'),
            material_divulgacao=bool(request.POST.get('material_divulgacao')),
            interesse_feiras=bool(request.POST.get('interesse_feiras')),

            dificuldades_producao=request.POST.get('dificuldades_producao'),
            dificuldades_venda=request.POST.get('dificuldades_venda'),
            apoios_recebidos=request.POST.get('apoios_recebidos'),

            apoio_producao=request.POST.get('apoio_producao'),
            apoio_venda=request.POST.get('apoio_venda'),
            fala_artesa=request.POST.get('fala_artesa'),
        )
        artesa.save()
        return redirect('dashboard')  # redirecionar após o cadastro
    return render(request, 'cadastros/cadastrar_artesa.html')
####**************************************************************************************************************************************

def cadastrar_canal(request):
    if request.method == 'POST':
        canal = CanalComercializacao(
            responsavel=request.POST.get('responsavel'),
            data=request.POST.get('data'),
            comunidade=request.POST.get('comunidade'),
            nome_entrevistado=request.POST.get('nome_entrevistado'),
            canais_identificados=request.POST.get('canais_identificados'),
            rota_nome=request.POST.get('rota_nome'),
            rota_itinerario=request.POST.get('rota_itinerario'),
            pontos_parada=request.POST.get('pontos_parada'),
            transporte_embalagem=request.POST.get('transporte_embalagem'),
            produtores_inseridos=request.POST.get('produtores_inseridos')
        )
        canal.save()
        return redirect('dashboard')
    return render(request, 'cadastros/cadastrar_canal.html')
####**************************************************************************************************************************************

def cadastrar_feirante(request):
    if request.method == 'POST':
        feirante = Feirante(
            nome_feira=request.POST.get('nome_feira'),
            local=request.POST.get('local'),
            periodicidade=request.POST.get('periodicidade'),
            produtos=request.POST.get('produtos'),
            volume=request.POST.get('volume'),

            beneficios=request.POST.get('beneficios'),
            contribuicao=request.POST.get('contribuicao'),
            fortalecimento=request.POST.get('fortalecimento'),
            produtos_mais_vendidos=request.POST.get('produtos_mais_vendidos'),
            estrutura_apropriada=request.POST.get('estrutura_apropriada'),

            dificuldades=request.POST.get('dificuldades'),
            comunicacao=request.POST.get('comunicacao'),
            apoio_institucional=request.POST.get('apoio_institucional'),
            problemas_aceitacao=request.POST.get('problemas_aceitacao'),
            sugestoes=request.POST.get('sugestoes')
        )
        feirante.save()
        return redirect('dashboard')
    return render(request, 'cadastros/cadastrar_feirante.html')
####**************************************************************************************************************************************


def cadastrar_agricultor(request):
    if request.method == 'POST':
        agricultor = Agricultor(
            local_feira=request.POST.get('local_feira'),
            data=request.POST.get('data'),
            entrevistador=request.POST.get('entrevistador'),
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
            custos_principais=request.POST.get('custos_principais'),
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
            apoio_publico=request.POST.get('apoio_publico'),
            acesso_credito=bool(request.POST.get('acesso_credito')),
            instituicao_credito=request.POST.get('instituicao_credito'),
        )
        agricultor.save()
        return redirect('dashboard')
    return render(request, 'cadastros/cadastrar_agricultor.html')
####**************************************************************************************************************************************

def listar_artesas(request):
    artesas = Artesa.objects.all().order_by('-id')
    return render(request, 'cadastros/listar_artesas.html', {'artesas': artesas})
####**************************************************************************************************************************************

def listar_canais(request):
    canais = CanalComercializacao.objects.all()
    return render(request, 'cadastros/listar_canais.html', {'canais': canais})
####**************************************************************************************************************************************

def listar_feirantes(request):
    feirantes = Feirante.objects.all()
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
