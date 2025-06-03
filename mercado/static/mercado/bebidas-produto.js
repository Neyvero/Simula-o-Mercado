function getCSRFToken() {
  let cookieValue = null;
  const cookies = document.cookie.split(';');
  for (let i = 0; i < cookies.length; i++) {
    const cookie = cookies[i].trim();
    if (cookie.startsWith('csrftoken=')) {
      cookieValue = decodeURIComponent(cookie.substring('csrftoken='.length));
      break;
    }
  }
  return cookieValue;
}

let produtoJson = [
    {id:1, name:'Água', img:'/static/mercado/images/bebida-produto/agua.jpeg', price:2.00, sizes:['Unidade', 'Pacote'], description:'Água natural, retirada do monte olimpo.'},
    {id:2, name:'Cerveja', img:'/static/mercado/images/bebida-produto/cerveja.jpg', price:3.50, sizes:['Unidade', 'Engradado'], description:'Cerveja refinada, sinta o gosto da puro malte.'},
    {id:3, name:'Suco', img:'/static/mercado/images/bebida-produto/suco.png', price:4.00, sizes:['Unidade', 'Caixa'], description:'Suco extraido da polpa, natural e gostoso.'}
];

document.querySelector('.produtoInfo--addButton').addEventListener('click', async () => {
  let id = modalKey;
  let produto = produtoJson[id];

  const qt = quantProdutos; 

  const payload = {
    descricao: produto.name,
    quantidade: qt,
    preco_unitario: produto.price
  };

  const response = await fetch('/api/carrinho/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-Requested-With': 'XMLHttpRequest',
    'X-CSRFToken': getCSRFToken()
  },
  body: JSON.stringify(payload)
});

  if (response.ok) {
    window.recarregarCarrinho(); 
    fecharModal();
  } else {
    alert('Erro ao adicionar ao carrinho.');
  }
});