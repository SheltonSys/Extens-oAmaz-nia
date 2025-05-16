from django.contrib import admin
from .models import CanalComercializacao
import json
from django.utils.html import format_html

@admin.register(CanalComercializacao)
class CanalComercializacaoAdmin(admin.ModelAdmin):
    list_display = ['responsavel', 'comunidade', 'data', 'exibir_canais_qtd']
    readonly_fields = ['exibir_canais_identificados', 'exibir_rota_itinerario', 'exibir_transporte_embalagem']

    fieldsets = (
        (None, {
            'fields': (
                'responsavel', 'data', 'comunidade', 'nome_entrevistado',
                'exibir_canais_identificados',
                'rota_nome', 'exibir_rota_itinerario',
                'pontos_parada', 'exibir_transporte_embalagem',
                'produtores_inseridos',
            )
        }),
    )

    def exibir_canais_qtd(self, obj):
        try:
            canais = json.loads(obj.canais_identificados or '[]')
            return f"{len(canais)} canais"
        except:
            return "0"
    exibir_canais_qtd.short_description = "Canais"

    def exibir_canais_identificados(self, obj):
        try:
            canais = json.loads(obj.canais_identificados or '[]')
            html = "<ul style='padding-left:18px;'>"
            for c in canais:
                html += f"<li><strong>{c['nome']}</strong> – {c['canal']} ({c['tipo']})<br><em>R$ {c['volume']} | {c['observacao']}</em></li>"
            html += "</ul>"
            return format_html(html)
        except:
            return "Nenhum canal registrado."
    exibir_canais_identificados.short_description = "Canais Identificados"

    def exibir_rota_itinerario(self, obj):
        try:
            paradas = json.loads(obj.rota_itinerario or '[]')
            html = "<ul style='padding-left:18px;'>"
            for p in paradas:
                html += f"<li><strong>{p['ponto']}</strong> – {p['tempo']}<br><em>{p['observacao']}</em></li>"
            html += "</ul>"
            return format_html(html)
        except:
            return "Nenhuma parada registrada."
    exibir_rota_itinerario.short_description = "Itinerário da Rota"

    def exibir_transporte_embalagem(self, obj):
        try:
            transportes = json.loads(obj.transporte_embalagem or '[]')
            html = "<ul style='padding-left:18px;'>"
            for t in transportes:
                html += f"<li><strong>{t['transporte']}</strong> | {t['embalagem']}<br><em>{t['observacao']}</em></li>"
            html += "</ul>"
            return format_html(html)
        except:
            return "Nenhum transporte registrado."
    exibir_transporte_embalagem.short_description = "Transporte e Embalagem"
########################################################################################################################################################

from django.contrib import admin
from .models import Feirante
import json
from django.utils.html import format_html, format_html_join


@admin.register(Feirante)
class FeiranteAdmin(admin.ModelAdmin):
    list_display = ('nome_feira', 'local', 'periodicidade', 'data_cadastro')
    readonly_fields = (
        'visualizar_beneficios',
        'visualizar_contribuicao',
        'visualizar_fortalecimento',
        'visualizar_produtos_vendidos',
        'visualizar_dificuldades',
    )
    fields = (
        'nome_feira', 'local', 'periodicidade', 'produtos', 'volume',
        'visualizar_beneficios',
        'visualizar_contribuicao',
        'visualizar_fortalecimento',
        'visualizar_produtos_vendidos',
        'estrutura_apropriada',
        'visualizar_dificuldades',
        'comunicacao', 'apoio_institucional',
        'problemas_aceitacao', 'sugestoes', 'data_cadastro'
    )

    def render_json_list(self, obj, field_name):
        try:
            items = json.loads(getattr(obj, field_name) or "[]")
            if isinstance(items, list):
                return format_html_join(
                    '<br>',
                    '<li>{}</li>',
                    ((item,) for item in items)
                )
            return format_html('<pre>{}</pre>', items)
        except Exception as e:
            return format_html('<span style="color: red;">Erro ao carregar</span>')

    def visualizar_beneficios(self, obj):
        return self.render_json_list(obj, 'beneficios')
    visualizar_beneficios.short_description = "Benefícios Percebidos"

    def visualizar_contribuicao(self, obj):
        return self.render_json_list(obj, 'contribuicao')
    visualizar_contribuicao.short_description = "Contribuição da Feira"

    def visualizar_fortalecimento(self, obj):
        return self.render_json_list(obj, 'fortalecimento')
    visualizar_fortalecimento.short_description = "Fortalecimento Comunitário"

    def visualizar_produtos_vendidos(self, obj):
        return self.render_json_list(obj, 'produtos_mais_vendidos')
    visualizar_produtos_vendidos.short_description = "Produtos com Mais Saída"

    def visualizar_dificuldades(self, obj):
        return self.render_json_list(obj, 'dificuldades')
    visualizar_dificuldades.short_description = "Dificuldades para Participar"
########################################################################################################################################################

from django.contrib import admin
from .models import Artesa
import json
from django.utils.html import format_html, format_html_join


@admin.register(Artesa)
class ArtesaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'idade', 'renda_artesanato', 'data_cadastro')
    readonly_fields = (
        'visualizar_tipos_producao',
        'visualizar_forma_aprendizado',
        'visualizar_pontos_fortes',
        'visualizar_formas_venda',
        'visualizar_dificuldades_producao',
        'visualizar_dificuldades_venda',
        'visualizar_apoios_recebidos',
        'visualizar_apoio_producao',
        'visualizar_apoio_venda',
    )
    fields = (
        'nome', 'idade', 'escolaridade',
        'pessoas_na_casa', 'familiares_na_producao', 'renda_artesanato',

        'visualizar_tipos_producao', 'tempo_artesanato', 'visualizar_forma_aprendizado',
        'visualizar_pontos_fortes', 'visualizar_formas_venda',
        'material_divulgacao', 'interesse_feiras',

        'visualizar_dificuldades_producao', 'visualizar_dificuldades_venda',
        'visualizar_apoios_recebidos', 'visualizar_apoio_producao', 'visualizar_apoio_venda',

        'fala_artesa', 'data_cadastro'
    )

    def render_json_list(self, obj, field_name):
        try:
            items = json.loads(getattr(obj, field_name) or "[]")
            if isinstance(items, list):
                return format_html_join('<br>', '<li>{}</li>', ((item,) for item in items))
            return format_html('<pre>{}</pre>', items)
        except Exception:
            return format_html('<span style="color:red;">[Erro ao carregar]</span>')

    def visualizar_tipos_producao(self, obj):
        return self.render_json_list(obj, 'tipos_producao')
    visualizar_tipos_producao.short_description = "Tipos de Produção"

    def visualizar_forma_aprendizado(self, obj):
        return self.render_json_list(obj, 'forma_aprendizado')
    visualizar_forma_aprendizado.short_description = "Forma de Aprendizado"

    def visualizar_pontos_fortes(self, obj):
        return self.render_json_list(obj, 'pontos_fortes')
    visualizar_pontos_fortes.short_description = "Pontos Fortes"

    def visualizar_formas_venda(self, obj):
        return self.render_json_list(obj, 'formas_venda')
    visualizar_formas_venda.short_description = "Formas de Venda"

    def visualizar_dificuldades_producao(self, obj):
        return self.render_json_list(obj, 'dificuldades_producao')
    visualizar_dificuldades_producao.short_description = "Dificuldades na Produção"

    def visualizar_dificuldades_venda(self, obj):
        return self.render_json_list(obj, 'dificuldades_venda')
    visualizar_dificuldades_venda.short_description = "Dificuldades na Venda"

    def visualizar_apoios_recebidos(self, obj):
        return self.render_json_list(obj, 'apoios_recebidos')
    visualizar_apoios_recebidos.short_description = "Apoios Recebidos"

    def visualizar_apoio_producao(self, obj):
        return self.render_json_list(obj, 'apoio_producao')
    visualizar_apoio_producao.short_description = "Apoios para Produção"

    def visualizar_apoio_venda(self, obj):
        return self.render_json_list(obj, 'apoio_venda')
    visualizar_apoio_venda.short_description = "Apoios para Venda"
