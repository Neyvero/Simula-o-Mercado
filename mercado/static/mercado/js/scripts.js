let modalKey = 0

// variavel para controlar a quantidade inicial de produtos na modal
let quantProdutos = 1

let cart = [] // carrinho

const seleciona = (elemento) => document.querySelector(elemento)
const selecionaTodos = (elemento) => document.querySelectorAll(elemento)

const formatoReal = (valor) => {
    return valor.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
}

const formatoMonetario = (valor) => {
    if(valor) {
        return valor.toFixed(2)
    }
}

const abrirModal = () => {
    seleciona('.produtoWindowArea').style.opacity = 0
    seleciona('.produtoWindowArea').style.display = 'flex'
    setTimeout(() => {
        seleciona('.produtoWindowArea').style.opacity = 1
    }, 150)
}

const fecharModal = () => {
    seleciona('.produtoWindowArea').style.opacity = 0 // transparente
    setTimeout(() => seleciona('.produtoWindowArea').style.display = 'none', 500)
}

const botoesFechar = () => {
    // BOTOES FECHAR MODAL
    selecionaTodos('.produtoInfo--cancelButton, .produtoInfo--cancelMobileButton').forEach( (item) => item.addEventListener('click', fecharModal) )
}


const preencheDadosModal = (item) => {
        seleciona('.produtoBig img').src = item.img
        seleciona('.produtoInfo h1').innerHTML = item.name
        seleciona('.produtoInfo--desc').innerHTML = item.description
        seleciona('.produtoInfo--actualPrice').innerHTML = `R$ ${item.price.toFixed(2)}`
}

const pegarKey = (e) => {
    // .closest retorna o elemento mais proximo que tem a class que passamos
    // do .pizza-item ele vai pegar o valor do atributo data-key
    let key = e.target.closest('.produto-item').getAttribute('data-key')
    console.log('Produto clicada ' + key)
    console.log(produtoJson[key])

    // garantir que a quantidade inicial de pizzas é 1
    quantProdutos = 1

    // Para manter a informação de qual pizza foi clicada
    modalKey = key

    return key
}

const mudarQuantidade = () => {
    // Ações nos botões + e - da janela modal
    seleciona('.produtoInfo--qtmais').addEventListener('click', () => {
        quantProdutos++
        seleciona('.produtoInfo--qt').innerHTML = quantProdutos
    })

    seleciona('.produtoInfo--qtmenos').addEventListener('click', () => {
        if(quantProdutos > 1) {
            quantProdutos--
            seleciona('.produtoInfo--qt').innerHTML = quantProdutos	
        }
    })
}

produtoJson.map((item, index ) => {
    //console.log(item)
    let produtoItem = document.querySelector('.models .produto-item').cloneNode(true)
    //console.log(pizzaItem)
    seleciona('.produto-area').append(produtoItem)

    // preencher os dados de cada produto
    produtoItem.setAttribute('data-key', index)
    produtoItem.querySelector('.produto-item--img img').src = item.img
    produtoItem.querySelector('.produto-item--price').innerHTML = `R$ ${item.price.toFixed(2)}`
    produtoItem.querySelector('.produto-item--name').innerHTML = item.name
    produtoItem.querySelector('.produto-item--desc').innerHTML = item.description

    produtoItem.querySelector('.produto-item--add').addEventListener('click', (e) => {
        e.preventDefault()
        console.log('Clicou no produto')

        let chave = pegarKey(e)

        // abriu janela do modal
        abrirModal()

        //preenchimento dos dados 
        preencheDadosModal(item)

        seleciona('.produtoInfo--qt').innerHTML = quantProdutos
    })

    botoesFechar()
    
})

mudarQuantidade()


