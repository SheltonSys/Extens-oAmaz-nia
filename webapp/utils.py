import matplotlib.pyplot as plt
import base64
from io import BytesIO

def gerar_grafico_base64(titulo, labels, dados):
    # Garante que as listas estejam sincronizadas e seguras
    if not labels or not dados or len(labels) != len(dados):
        labels = ['Sem Dados']
        dados = [0]

    fig, ax = plt.subplots(figsize=(6, 4))

    bars = ax.bar(labels, dados, color='skyblue', edgecolor='black')

    # Adiciona os valores sobre as barras
    for bar in bars:
        altura = bar.get_height()
        ax.annotate(f'{int(altura)}',
                    xy=(bar.get_x() + bar.get_width() / 2, altura),
                    xytext=(0, 5),  # Ajuste de deslocamento vertical
                    textcoords="offset points",
                    ha='center', va='bottom',
                    fontsize=9, fontweight='bold')

    ax.set_title(titulo)
    ax.set_ylabel('Total')
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=30, ha='right')

    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    plt.close(fig)

    return base64.b64encode(buffer.getvalue()).decode('utf-8')
