### Universidade Federal de Santa Catarina
#### Departamento de Informática e Estatística (INE)
#### INE5421 - Linguagem Formais e Compiladores - Trabalho 01
##### Filipe Oliveira de Borba
##### Gabriel Leal Chittolina Amaral
##### Lucas João Martins
###### 14 de outubro de 2018

---

#### Informações sobre os fontes

##### Tecnologias

As seguintes tecnologias foram utilizadas:
- Python 3.6 como linguagem de programação;
- Qt QML como framework para desenvolvimento da interface gráfica;
- JSON como extensão dos arquivos utilizados na aplicação;
- git e github para versionamento de código entre os membros da equipe

Além disso, vale citar as principais libs/módulos utilizados:
- `json` para trabalhar com os arquivos nesse formato;
- `itertools` para fazer algumas iterações serem mais eficientes;
- `re` para auxiliar no trabalho com expressões regulares;
- `collections` que fornece um tipo de dado crucial no desenvolvimento da modelagem;
- `unittest` para realização dos testes unitários;
- `os` para fornecer uma interface que permitisse o acesso de arquivos nos testes unitários;
- `sys` para auxiliar na execução da aplicação.

##### Modelagem

Para uma melhor explicação, esse item está separado por autômato, gramática e expressão regular.

Autômato:
- modelado na maneira clássica: uma 5-tupla
- o alfabeto corresponde a um `set`
- o estado inicial é uma `string`
- o conjunto de estados corresponde a um `set`
- o conjunto de estados finais são um `set`
- as produções são mapeadas para um `dict` onde as chaves são uma `collections.namedtuple` de estado
de origem e símbolo do alfabeto que apontam para um `set` que são os estados destinos

Gramática:
- apesar de somente receber o seu símbolo inicial e as produções no construtor, está modelado de modo
clássico: uma 4-tupla
- símbolo inicial é uma `string`
- produções correspondem a um `set` de tuplas
- não-terminais são um `set`
- terminais também são um `set`

Expressão regular:
- modelado de maneira similar ao que o livro do Aho apresenta, ou seja, como uma árvore

Vale citar que buscou-se esboçar como cada parte do código foi modelado, e, que para maiores detalhes
deve-se consultar o código fonte.

##### Estruturas de dados

As estruturas de dados mais utilizadas no desenvolvimento foram:
- `set` e `frozenset`
- `dict`
- `list`
- `namedtuple`

Como visto aqui (https://www.ics.uci.edu/~pattis/ICS-33/lectures/complexitypython.txt), percebe-se,
que na melhor das hipóteses, grande parte das operações possuem complexidade O(1).

##### Execuções dos testes solicitados

Para uma melhor explicação, esse item está separado por autômato, gramática e expressão regular.

Autômato:
- teste 1, minimização de AFD (retirado daqui http://www.cs.ucr.edu/~stelo/cs150fall02/subset.pdf):
  - clicar em 'Import automata' e selecionar o arquivo 'teste1MinimizacaoAfd.json'
  - clicar em 'DFA Minimize' e verificar o resultado
- teste 2, determinização de AFND (retirado daqui https://en.wikipedia.org/wiki/Powerset_construction):
  - clicar em 'Import automata' e selecionar o arquivo 'teste2AfndAfd.json'
  - clicar em 'NFA to DFA' e verificar o resultado
- teste 3, união de AFD (retirado daqui https://www.complang.tuwien.ac.at/lkovacs/ATCSNotes/atcs_h2.pdf):
  - clicar em 'Import automata' e selecionar o arquivo 'teste3UniaoAfdInput01.json'
  - clicar em 'Import automata' e selecionar o arquivo 'teste3UniaoAfdInput02.json'
  - clicar em 'DFA Union' e verificar o resultado
- teste 4, interseção de AFD (retirado daqui https://www.complang.tuwien.ac.at/lkovacs/ATCSNotes/atcs_h2.pdf):
  - clicar em 'Import automata' e selecionar o arquivo 'teste4IntersecaoAfdInput01.json'
  - clicar em 'Import automata' e selecionar o arquivo 'teste4IntersecaoAfdInput02.json'
  - clicar em 'DFA Intersection' e verificar o resultado
- teste 5, transformação de AFD para GR:
  - clicar em 'Import automata' e selecionar o arquivo 'teste5AfdGr.json'
  - clicar em 'DFA to GR' e verificar o resultado

Gramática:

Expressão regular:

---

#### Utilização do sistema

Do ponto de vista visual, a aplicação busca ser simples e intuitiva de ser usada. Consiste de
uma única tela dividida em três partes (autômato, gramática e expressão regular), onde cada parte
possui botões básicos para realizar uma espécie de CRUD (sem todas as ações disponíveis). Além
disso, cada parte possui um botão para a realização de cada requisito solicitado naquela parte.

Observação importante: é possível redimensionar com o mouse o tamanho de cada painel. Basta
colocar ele sobre a divisória (o ponteiro irá mudar), então pressionar e arrastar para o tamanho
desejado.

Já do ponto de vista estrutural, pode-se ver a organização de pastas no repositório do github
(https://github.com/chittolina/ine5421-t1):
- `report` possui os arquivos relacionados ao relatório final;
- `src` possui um arquivo para cada item que deveria ser manipulado pela aplicação. Além disso,
possui um arquivo `utils` que possui código que os itens citados anteriormente compartilham;
- `test` possui os arquivos necessários para a execução dos testes unitários. Como o autômato é
uma das peças chave do trabalho, pois está envolvido em quase todos os requisitos, optou-se por
realizar testes unitários sobre a sua classe;
- `test_with_view` possui os arquivos JSON necessários para a realização dos testes solicitados;
- `ui` contêm toda definição visual do programa;
- `main.py` no diretório principal serve como ponto de partida da aplicação, ou seja, bastaria
um `python main.py` para executar o programa.

---

#### Principais referências

- Slides fornecidos pela professora;
- Compilers: Principles, Techniques, and Tools (2nd Edition) by Alfred V. Aho;
- Introduction to the Theory of Computation by Michael Sipser;
- Introduction to Automata Theory, Languages, and Computation by Hopcroft John;
- Formal Languages and Their Relation to Automata by Hopcroft John.
