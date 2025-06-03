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
    {id:1, name:'Sabonete', img:'/static/mercado/images/higiene_pessoal-produto/sabonete.png', price:3.00, sizes:['Unidade', 'Caixa'], description:'Sabonete Dove, vai se limpar.'},
    {id:2, name:'Shampoo', img:'/static/mercado/images/higiene_pessoal-produto/shampo.jpg', price:8.00, sizes:['Unidade', 'Caixa'], description:'Shampo ....'}
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