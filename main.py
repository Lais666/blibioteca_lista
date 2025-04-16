from flask import Flask, render_template, request, redirect, flash

# Criação da instância do Flask
app = Flask(__name__)

# A chave secreta é usada para criar sessões seguras e gerenciar flash messages
app.secret_key = 'biblioteca_virtual_super_secreta_2025'

# Lista de livros (simulando um banco de dados em memória)
livros = []


# Rota para a página inicial, que renderiza a lista de livros
@app.route('/')
def index():
    return render_template('index.html')


# Rota para listar todos os livros
@app.route("/livros", methods=["GET"])
def listar_livros():
    return render_template("livros.html", livros=livros)


# Rota para abrir o formulário de adicionar um novo livro
@app.route("/abrir_adicionar", methods=["GET"])
def abrir_adicionar():
    return render_template("adicionar.html")


# Rota para processar o formulário de adicionar um novo livro
@app.route('/adicionar', methods=['POST'])
def adicionar():
    # Gera o próximo código automaticamente com base no tamanho da lista de livros
    codigo = str(len(livros) + 1)

    # Coleta os dados do formulário
    titulo = request.form['titulo']
    autor = request.form['autor']
    ano = request.form['ano']

    # Cria um dicionário com os dados do livro
    livro = {'codigo': codigo, 'titulo': titulo, 'autor': autor, 'ano': ano}

    # Adiciona o livro à lista
    livros.append(livro)

    # Mensagem de sucesso com flash
    flash('Livro adicionado com sucesso!', 'success')

    # Redireciona para a página de listagem de livros
    return redirect('/livros')


# Rota para abrir o formulário de edição de um livro específico
@app.route('/abrir_editar/<codigo>')  # Define a URL que aceita um código como parâmetro
def abrir_editar(codigo):
    # Percorre a lista de livros para encontrar o livro com o código correspondente
    for livro in livros:
        if livro['codigo'] == codigo:
            # Se o livro for encontrado, renderiza a página de edição com os dados do livro
            return render_template('editar.html', livro=livro)

    # Se não encontrar o livro, exibe uma mensagem de erro e redireciona para a página inicial
    flash('Livro não encontrado!', 'danger')
    return redirect('/')


# Rota para processar o formulário de edição de um livro
@app.route('/editar/<codigo>', methods=['POST'])  # Aceita apenas requisições POST com o código do livro na URL
def editar(codigo):
    # Percorre a lista de livros para encontrar o livro com o código correspondente
    for livro in livros:
        if livro['codigo'] == codigo:
            # Atualiza os dados do livro com os valores enviados pelo formulário
            livro['titulo'] = request.form['titulo']
            livro['autor'] = request.form['autor']
            livro['ano'] = request.form['ano']

            # Exibe uma mensagem de sucesso ao usuário
            flash('Livro atualizado com sucesso!', 'success')
            break
    else:
        # Caso o livro não seja encontrado, exibe uma mensagem de erro
        flash('Erro ao editar o livro. Livro não encontrado!', 'danger')

    # Redireciona de volta para a página de listagem de livros
    return redirect('/livros')


# Rota para excluir um livro
@app.route('/excluir/<codigo>', methods=['POST'])
def excluir(codigo):
    # Converte o código para inteiro e calcula a posição na lista
    posicao = int(codigo) - 1  # Ajusta para excluir na posição correta (código começa de 1)

    if posicao < len(livros) and posicao >= 0:  # Verifica se a posição é válida
        livros.pop(posicao)  # Remove o livro da lista
        flash('Livro excluído com sucesso!', 'success')
    else:
        flash('Erro ao excluir o livro. Livro não encontrado!', 'danger')

    # Redireciona para a página de listagem de livros
    return redirect('/livros')


# Inicia o servidor Flask
if __name__ == '__main__':
    app.run(debug=True)
