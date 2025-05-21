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

from collections import Counter
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Artesa, CanalComercializacao, Feirante, Agricultor, Evento
from .utils import gerar_grafico_base64


# Função segura para geração de gráficos
def gerar_grafico_seguro(titulo, lista):
    contador = Counter(lista)
    if contador:
        labels, valores = zip(*contador.items())
    else:
        labels, valores = ['Sem Dados'], [0]
    return gerar_grafico_base64(titulo, list(labels), list(valores))


@login_required
def dashboard(request):
    user = request.user

    # Consulta por permissão
    if user.is_superuser:
        artesas_qs = Artesa.objects.all()
        canais_qs = CanalComercializacao.objects.all()
        feirantes_qs = Feirante.objects.all()
        agricultores_qs = Agricultor.objects.all()
        eventos_qs = Evento.objects.all()
    else:
        artesas_qs = Artesa.objects.filter(responsavel=user)
        canais_qs = CanalComercializacao.objects.filter(responsavel=user)
        feirantes_qs = Feirante.objects.filter(responsavel=user)
        agricultores_qs = Agricultor.objects.filter(responsavel=user)
        eventos_qs = Evento.objects.filter(responsavel=user)

    # Resumo
    resumo_categorias = [
        {'Categoria': 'Artesãs', 'Total': artesas_qs.count(), 'Novos': 3},
        {'Categoria': 'Canais', 'Total': canais_qs.count(), 'Novos': 2},
        {'Categoria': 'Feirantes', 'Total': feirantes_qs.count(), 'Novos': 1},
        {'Categoria': 'Agricultores', 'Total': agricultores_qs.count(), 'Novos': 5},
    ]

    # Calendário
    calendario_eventos = [{'Data': e.data, 'Evento': e.titulo} for e in eventos_qs.order_by('data')]

    # Cards visuais
    cards = [
        {'categoria': 'Artesãs', 'total': artesas_qs.count(), 'cor': 'info', 'icon': 'fas fa-female', 'url': 'cadastrar_artesa', 'label': 'Cadastrar'},
        {'categoria': 'Canais de Comercialização', 'total': canais_qs.count(), 'cor': 'success', 'icon': 'fas fa-store', 'url': 'cadastrar_canal', 'label': 'Cadastrar'},
        {'categoria': 'Feirantes', 'total': feirantes_qs.count(), 'cor': 'warning', 'icon': 'fas fa-people-carry', 'url': 'cadastrar_feirante', 'label': 'Cadastrar'},
        {'categoria': 'Agricultores', 'total': agricultores_qs.count(), 'cor': 'danger', 'icon': 'fas fa-tractor', 'url': 'cadastrar_agricultor', 'label': 'Cadastrar'},
    ]

    # Listas para gráficos
    renda_list = list(artesas_qs.values_list('renda_artesanato', flat=True))

    canais_list = []
    import json  # no topo do arquivo

    for canal in canais_qs:
        try:
            identificados = canal.canais_identificados
            if isinstance(identificados, str):
                identificados = json.loads(identificados)

            for d in identificados:
                if isinstance(d, dict):
                    canal_tipo = (d.get('canal') or '') + (d.get('tipo') or '')
                    if canal_tipo.strip():
                        canais_list.append(canal_tipo)
        except Exception:
            continue


    periodicidade_list = list(feirantes_qs.values_list('periodicidade', flat=True))
    credito_list = ['Sim' if a.acesso_credito else 'Não' for a in agricultores_qs]

    # Gráficos
    # Gráficos de pizza e barras
    grafico_renda = gerar_grafico_seguro("Renda do Artesanato", renda_list)
    grafico_canais = gerar_grafico_seguro("Tipos de Canais", canais_list)
    grafico_feiras = gerar_grafico_seguro("Periodicidade das Feiras", periodicidade_list)
    grafico_credito = gerar_grafico_seguro("Acesso ao Crédito", credito_list)

    categorias = [c['Categoria'] for c in resumo_categorias]
    totais = [c['Total'] for c in resumo_categorias]
    grafico_barras = gerar_grafico_base64("Comparativo Geral", categorias, totais)



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

from django.core.files.base import ContentFile
import base64
from django.urls import reverse
from django.shortcuts import redirect

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

        # Responsável (usuário logado)
        artesa.responsavel = request.user

        # Foto
        if foto_base64 and foto_base64.startswith('data:image'):
            format, imgstr = foto_base64.split(';base64,')
            ext = format.split('/')[-1]
            image_data = ContentFile(base64.b64decode(imgstr), name=f"{artesa.nome}_foto.{ext}")
            artesa.foto_evidencia = image_data

        artesa.save()
        return redirect(reverse('cadastrar_artesa') + '?sucesso=1')

    return render(request, 'cadastros/cadastrar_artesa.html')


from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

@csrf_exempt
def sincronizar_artesa(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        nova = Artesa(
            nome=data.get('nome'),
            idade=data.get('idade'),
            escolaridade=data.get('escolaridade'),
            pessoas_na_casa=data.get('pessoas_na_casa'),
            familiares_na_producao=data.get('familiares_na_producao'),
            renda_artesanato=data.get('renda_artesanato'),
            tipos_producao=', '.join(data.get('tipos_producao', [])),
            tempo_artesanato=data.get('tempo_artesanato'),
            forma_aprendizado=', '.join(data.get('forma_aprendizado', [])),
            pontos_fortes=', '.join(data.get('pontos_fortes', [])),
            formas_venda=', '.join(data.get('formas_venda', [])),
            material_divulgacao=bool(data.get('material_divulgacao')),
            interesse_feiras=bool(data.get('interesse_feiras')),
            dificuldades_producao=', '.join(data.get('dificuldades_producao', [])),
            dificuldades_venda=', '.join(data.get('dificuldades_venda', [])),
            apoios_recebidos=', '.join(data.get('apoios_recebidos', [])),
            apoio_producao=', '.join(data.get('apoio_producao', [])),
            apoio_venda=', '.join(data.get('apoio_venda', [])),
            fala_artesa=data.get('fala_artesa'),
            responsavel=request.user if request.user.is_authenticated else None
        )

        nova.save()
        return JsonResponse({"status": "ok"})




####**************************************************************************************************************************************

import json  # necessário para salvar como JSON
from django.shortcuts import render, redirect
from .models import CanalComercializacao

def cadastrar_canal(request):
    if request.method == 'POST':
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

        canal = CanalComercializacao(
            responsavel=request.user,  # ⬅ usuário logado
            data=request.POST.get('data'),
            comunidade=request.POST.get('comunidade'),
            nome_entrevistado=request.POST.get('nome_entrevistado'),
            canais_identificados=json.dumps(canais_identificados),
            rota_nome=request.POST.get('rota_nome'),
            rota_itinerario=json.dumps(rota_itinerario),
            transporte_embalagem=json.dumps(transporte_embalagem),
            produtores_inseridos=json.dumps(produtores_inseridos),
        )
        canal.save()
        return redirect('dashboard')

    return render(request, 'cadastros/cadastrar_canal.html')





import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import CanalComercializacao

@csrf_exempt
def sincronizar_canal(request):
    if request.method == 'POST':
        try:
            dados = json.loads(request.body.decode('utf-8'))

            def parse_lista(campo):
                return dados.get(campo, []) if isinstance(dados.get(campo), list) else []

            canais_identificados = [
                {"canal": c, "tipo": t, "nome": n, "volume": v, "observacao": o}
                for c, t, n, v, o in zip(
                    parse_lista("canal_canal"),
                    parse_lista("canal_tipo"),
                    parse_lista("canal_nome"),
                    parse_lista("canal_volume"),
                    parse_lista("canal_obs"),
                )
            ]

            rota_itinerario = [
                {"ponto": p, "tempo": t, "observacao": o}
                for p, t, o in zip(
                    parse_lista("parada_ponto"),
                    parse_lista("parada_tempo"),
                    parse_lista("parada_obs"),
                )
            ]

            transporte_embalagem = [
                {"transporte": t, "embalagem": e, "observacao": o}
                for t, e, o in zip(
                    parse_lista("transporte_tipo"),
                    parse_lista("embalagem_tipo"),
                    parse_lista("transporte_obs"),
                )
            ]

            produtores_inseridos = [
                {"nome": n, "comunidade": c}
                for n, c in zip(
                    parse_lista("produtor_nome"),
                    parse_lista("produtor_comunidade"),
                )
            ]

            canal = CanalComercializacao(
                responsavel=request.user if request.user.is_authenticated else None,  # ⬅ aqui também
                data=dados.get("data"),
                comunidade=dados.get("comunidade", ""),
                nome_entrevistado=dados.get("nome_entrevistado", ""),
                canais_identificados=json.dumps(canais_identificados),
                rota_nome=dados.get("rota_nome", ""),
                rota_itinerario=json.dumps(rota_itinerario),
                transporte_embalagem=json.dumps(transporte_embalagem),
                produtores_inseridos=json.dumps(produtores_inseridos),
            )
            canal.save()

            return JsonResponse({"status": "ok", "mensagem": "Canal sincronizado com sucesso."})
        except Exception as e:
            return JsonResponse({"status": "erro", "mensagem": str(e)}, status=400)

    return JsonResponse({"status": "erro", "mensagem": "Método não permitido."}, status=405)






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
            sugestoes=request.POST.get('sugestoes'),

            responsavel=request.user  # ← atribuição correta
        )

        if foto_base64 and foto_base64.startswith('data:image'):
            format, imgstr = foto_base64.split(';base64,')
            ext = format.split('/')[-1]
            image_data = ContentFile(base64.b64decode(imgstr), name=f"{feirante.nome_feira}_foto.{ext}")
            feirante.foto_evidencia = image_data

        feirante.save()
        return redirect('dashboard')

    return render(request, 'cadastros/cadastrar_feirante.html')



from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import Feirante

@csrf_exempt
def sincronizar_feirante(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        feirante = Feirante(
            nome_feira=data.get('nome_feira'),
            local=data.get('local'),
            periodicidade=data.get('periodicidade'),
            produtos=data.get('produtos'),
            volume=data.get('volume'),
            beneficios=json.dumps(data.get('beneficios', [])),
            contribuicao=json.dumps(data.get('contribuicao', [])),
            fortalecimento=json.dumps(data.get('fortalecimento', [])),
            produtos_mais_vendidos=json.dumps(data.get('produtos_aceitacao', [])),
            estrutura_apropriada=data.get('estrutura_feira'),
            dificuldades=json.dumps(data.get('dificuldades', [])),
            comunicacao=data.get('comunicacao'),
            apoio_institucional=data.get('apoio_institucional'),
            problemas_aceitacao=data.get('problemas_aceitacao'),
            sugestoes=data.get('sugestoes'),
            responsavel=request.user if request.user.is_authenticated else None  # ← incluso para vincular
        )

        feirante.save()
        return JsonResponse({"status": "ok"})

####**************************************************************************************************************************************


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Agricultor

@login_required
def cadastrar_agricultor(request):
    nome_entrevistador = request.user.get_full_name() or request.user.username
    if not nome_entrevistador.strip():
        nome_entrevistador = request.user.username

    if request.method == 'POST':
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
            responsavel=request.user  # ✅ aqui é o ponto principal
        )
        agricultor.save()
        return redirect('dashboard')

    contexto = {
        'opcoes_acesso': ['Muito bom', 'Bom', 'Regular', 'Ruim', 'Muito ruim'],
        'opcoes_higiene': ['Boa', 'Regular', 'Ruim'],
    }
    return render(request, 'cadastros/cadastrar_agricultor.html', contexto)




from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import Agricultor

@csrf_exempt
def sincronizar_agricultor(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        agricultor = Agricultor(
            local_feira=data.get('local_feira'),
            data=data.get('data'),
            entrevistador=data.get('entrevistador'),
            numero_ficha=data.get('numero_ficha'),
            idade=data.get('idade'),
            sexo=data.get('sexo'),
            escolaridade=data.get('escolaridade'),
            cidade_origem=data.get('cidade_origem'),
            tempo_feira=data.get('tempo_feira'),
            varias_feiras=data.get('varias_feiras') == '1',
            trabalha_familiares=data.get('trabalha_familiares') == '1',
            qtd_familiares=data.get('qtd_familiares'),
            grau_parentesco=data.get('grau_parentesco'),
            criancas_ajudam=data.get('criancas_ajudam') == '1',
            atividades_criancas=data.get('atividades_criancas'),
            idosos_ajudam=data.get('idosos_ajudam') == '1',
            atividades_idosos=data.get('atividades_idosos'),
            produto_principal=data.get('produto_principal'),
            origem_produto=data.get('origem_produto'),
            faturamento=data.get('faturamento'),
            custos_principais=", ".join(data.get('custos_principais', [])),
            renda_varia=data.get('renda_varia') == '1',
            meses_bons=data.get('meses_bons'),
            meses_fracos=data.get('meses_fracos'),
            acesso=data.get('acesso'),
            agua=data.get('agua') == '1',
            banheiro=data.get('banheiro') == '1',
            higiene=data.get('higiene'),
            seguranca=data.get('seguranca') == '1',
            motivo_inseguranca=data.get('motivo_inseguranca'),
            associacao=data.get('associacao') == '1',
            nome_associacao=data.get('nome_associacao'),
            capacitacao=data.get('capacitacao') == '1',
            capacitador=data.get('capacitador'),
            apoio_publico=", ".join(data.get('apoio_publico', [])),
            acesso_credito=data.get('acesso_credito') == '1',
            instituicao_credito=data.get('instituicao_credito'),
            responsavel=request.user if request.user.is_authenticated else None  # ✅ atribuição segura
        )

        agricultor.save()
        return JsonResponse({"status": "ok"})

####**************************************************************************************************************************************

from django.contrib.auth.decorators import login_required

@login_required
def listar_artesas(request):
    if request.user.is_superuser:
        artesas = Artesa.objects.all().order_by('-id')
    else:
        artesas = Artesa.objects.filter(responsavel=request.user).order_by('-id')
    
    return render(request, 'cadastros/listar_artesas.html', {'artesas': artesas})

####**************************************************************************************************************************************

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import json
from .models import CanalComercializacao

@login_required
def listar_canais(request):
    if request.user.is_superuser:
        canais = CanalComercializacao.objects.all().order_by('-data')
    else:
        canais = CanalComercializacao.objects.filter(responsavel=request.user).order_by('-data')

    for canal in canais:
        try:
            canal.transporte_embalagem = json.loads(canal.transporte_embalagem or '[]')
        except:
            canal.transporte_embalagem = []

        try:
            canal.rota_itinerario = json.loads(canal.rota_itinerario or '[]')
        except:
            canal.rota_itinerario = []

        try:
            canal.canais_identificados = json.loads(canal.canais_identificados or '[]')
        except:
            canal.canais_identificados = []

        try:
            canal.produtores_inseridos = json.loads(canal.produtores_inseridos or '[]')
        except:
            canal.produtores_inseridos = []

    return render(request, 'cadastros/listar_canais.html', {'canais': canais})



####**************************************************************************************************************************************

from django.contrib.auth.decorators import login_required
import json
from .models import Feirante

@login_required
def listar_feirantes(request):
    if request.user.is_superuser:
        feirantes = Feirante.objects.all()
    else:
        feirantes = Feirante.objects.filter(responsavel=request.user)

    for f in feirantes:
        try:
            f.beneficios_lista = json.loads(f.beneficios or '[]')
        except:
            f.beneficios_lista = ['[Erro ao carregar]']

    return render(request, 'cadastros/listar_feirantes.html', {'feirantes': feirantes})


####**************************************************************************************************************************************

from django.contrib.auth.decorators import login_required
from .models import Agricultor

@login_required
def listar_agricultores(request):
    if request.user.is_superuser:
        agricultores = Agricultor.objects.all()
    else:
        agricultores = Agricultor.objects.filter(responsavel=request.user)

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

from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect

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
                password=password
            )
            # Força como usuário comum, sem acesso ao painel
            user.is_superuser = False
            user.is_staff = False
            user.is_active = True
            user.save()

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


def excluir_usuario(request, usuario_id):
    usuario = get_object_or_404(User, id=usuario_id)
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


from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Agricultor, Artesa, CanalComercializacao, Feirante, Evento
from datetime import datetime
import json

def relatorio_dinamico(request):
    comunidade = request.GET.get('comunidade', '')
    tipo = request.GET.get('tipo', '')
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    responsavel_id = request.GET.get('responsavel')

    canais = CanalComercializacao.objects.all()
    agricultores = Agricultor.objects.all()
    feirantes = Feirante.objects.all()
    artesas = Artesa.objects.all()
    eventos = Evento.objects.all()

    # Filtro por responsável
    if responsavel_id:
        canais = canais.filter(responsavel_id=responsavel_id)
        agricultores = agricultores.filter(responsavel_id=responsavel_id)
        feirantes = feirantes.filter(responsavel_id=responsavel_id)
        artesas = artesas.filter(responsavel_id=responsavel_id)
        eventos = eventos.filter(responsavel_id=responsavel_id)

    # Filtro por comunidade/local
    if comunidade:
        canais = canais.filter(comunidade__icontains=comunidade)
        agricultores = agricultores.filter(cidade_origem__icontains=comunidade)
        feirantes = feirantes.filter(local__icontains=comunidade)
        eventos = eventos.filter(local__icontains=comunidade)

    # Intervalo de datas
    try:
        data_inicio_dt = datetime.strptime(data_inicio, "%Y-%m-%d").date() if data_inicio else None
        data_fim_dt = datetime.strptime(data_fim, "%Y-%m-%d").date() if data_fim else None
    except ValueError:
        data_inicio_dt = data_fim_dt = None

    if data_inicio_dt and data_fim_dt:
        canais = canais.filter(data__range=(data_inicio_dt, data_fim_dt))
        agricultores = agricultores.filter(data__range=(data_inicio_dt, data_fim_dt))
        eventos = eventos.filter(data__range=(data_inicio_dt, data_fim_dt))
    elif data_inicio_dt:
        canais = canais.filter(data__gte=data_inicio_dt)
        agricultores = agricultores.filter(data__gte=data_inicio_dt)
        eventos = eventos.filter(data__gte=data_inicio_dt)
    elif data_fim_dt:
        canais = canais.filter(data__lte=data_fim_dt)
        agricultores = agricultores.filter(data__lte=data_fim_dt)
        eventos = eventos.filter(data__lte=data_fim_dt)

    # Filtro por tipo/produto/evento
    if tipo:
        canais_filtrados = []
        for c in canais:
            try:
                identificados = json.loads(c.canais_identificados or '[]')
                if any(tipo.lower() in (d.get('canal', '') + d.get('tipo', '')).lower() for d in identificados if isinstance(d, dict)):
                    canais_filtrados.append(c)
            except Exception:
                continue
        canais = canais_filtrados

        agricultores = agricultores.filter(produto_principal__icontains=tipo)
        feirantes = feirantes.filter(produtos__icontains=tipo)
        artesas = artesas.filter(tipos_producao__icontains=tipo)
        eventos = eventos.filter(titulo__icontains=tipo)

    # Comunidades únicas
    comunidades = sorted(set(
        list(CanalComercializacao.objects.values_list('comunidade', flat=True)) +
        list(Agricultor.objects.values_list('cidade_origem', flat=True)) +
        list(Feirante.objects.values_list('local', flat=True)) +
        list(Evento.objects.values_list('local', flat=True))
    ))

    # Tipos/produtos/eventos únicos
    tipos_raw = set()
    tipos_raw.update(Agricultor.objects.values_list('produto_principal', flat=True))
    tipos_raw.update(Evento.objects.values_list('titulo', flat=True))

    for a in Artesa.objects.all():
        if a.tipos_producao:
            if isinstance(a.tipos_producao, list):
                tipos_raw.update(a.tipos_producao)
            else:
                tipos_raw.update(map(str.strip, a.tipos_producao.split(',')))

    for c in CanalComercializacao.objects.all():
        try:
            for canal in json.loads(c.canais_identificados or '[]'):
                if isinstance(canal, dict):
                    tipos_raw.add(canal.get('canal', '').strip())
                    tipos_raw.add(canal.get('tipo', '').strip())
        except Exception:
            continue

    tipos = sorted(set(filter(None, tipos_raw)))

    usuarios = User.objects.filter(is_active=True).order_by('first_name')

    # Converte tipos_producao (string) em lista para cada artesã
    for a in artesas:
        if a.tipos_producao:
            a.producoes_lista = [p.strip() for p in a.tipos_producao.split(',')]
        else:
            a.producoes_lista = []


    context = {
        'canais': canais,
        'agricultores': agricultores,
        'feirantes': feirantes,
        'artesas': artesas,
        'eventos': eventos,
        'comunidades': comunidades,
        'tipos': tipos,
        'usuarios': usuarios
    }

    return render(request, 'relatorios/relatorio_dinamico.html', context)

