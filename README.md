# Processamento de Imagens 2024/2

Repositório de códigos da disciplina Processamento de Imagens. Aqui você encontrará os códigos das atividades práticas feitas ao longo do semestre.

Professora: Glenda Botelho

Acadêmicos: [Antonio André](https://github.com/andrebarceloschagas/) e [Sophia Prado](https://github.com/sophiaprado1/)

---

Os códigos são escritos em Python e foram testados na versão 3.13.

Recomenda-se usar o ambiente virtual do Python para instalar as bibliotecas.

```bash
python -m venv venv
source venv/bin/activate
```

Para instalar as bibliotecas necessárias, você pode usar o seguinte comando:

```bash
pip install -r requirements.txt
```

Bibliotecas utilizadas:

- contourpy==1.3.0
- cycler==0.12.1
- fonttools==4.54.1
- kiwisolver==1.4.7
- matplotlib==3.9.2
- numpy==2.1.1
- packaging==24.1
- pillow==10.4.0
- pyparsing==3.1.4
- python-dateutil==2.9.0.post0
- six==1.16.0

---

## Interpolação por Vizinho mais Próximo

[Redução](/1/reducao_vizinho.py)

[Ampliação](/1/ampliacao_vizinho.py)

## Intepolação Bilinear

[Redução](/1/reducao_bilinear.py)

[Ampliação](/1/ampliação_bilinear.py)

## Rotulação

[Rotulação](/2/rotulacao.py)

## Operações Aritméticas

[Adição](/2/adicao.py)

[Subtração](/2/subtracao.py)

## Operação Geométrica

[Espelhamento Horizontal](/2/espelhamento.py)

## Transformação de Intensidade

[Transformação Negativa](/3/negativa.py)

## Processamento de Histograma

[Equalização de Histograma](/4/equalizacao.py)

## Filtragem

[Filtro da Média](/5/media.py)

[Filtros Laplacianos](/5/laplaciano.py)

[Filtro Gradiente com Máscaras de Sobel](/5/gradiente.py)

## Operações Morfológicas

[Erosão e Dilatação](/6/erosao_dilatacao.py)

[Abertura e Fechamento](/6/abertura_fechamento.py)

## Segmentação

[Segmenação por Limiarização](/6/limiarizacao.py)

---

Caso tenha alguma sugestão de melhoria, por favor, me envie para o email: <antonio.andre@uft.edu.br>
