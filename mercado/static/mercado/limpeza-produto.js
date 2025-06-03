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
    {id:1, name:'Detergente', img:'/static/mercado/images/limpeza-produto/detergente.png', price:1.99, sizes:['Unidade', 'Caixa'], description:'Detergente , vendido por unidade ou por caixa.'},
    {id:2, name:'Sabão em Pó', img:'/static/mercado/images/limpeza-produto/sabao_em_po.jpg', price:6.00, sizes:['Unidade', 'Caixa'], description:'Sabão em pó, vendido em unidade ou caixa.'},
    {id:3, name:'Vassoura', img:'/static/mercado/images/limpeza-produto/vassoura.png', price:7.99, sizes:['Unidade'], description:'Vassouras bonitas, vendidas por unidade'}
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