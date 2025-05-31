produtoJson.map((item, index ) => {
    //console.log(item)
    let produtoItem = document.querySelector('.models .produto-item').cloneNode(true)
    //console.log(pizzaItem)
    document.querySelector('.produto-area').append(produtoItem)

    // preencher os dados de cada pizza
    produtoItem.querySelector('.produto-item--img img').src = item.img
    produtoItem.querySelector('.produto-item--price').innerHTML = `R$ ${item.price.toFixed(2)}`
    produtoItem.querySelector('.produto-item--name').innerHTML = item.name
    produtoItem.querySelector('.produto-item--desc').innerHTML = item.description
})


