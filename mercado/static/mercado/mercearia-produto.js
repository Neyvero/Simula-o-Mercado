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
    {id:1, name:'Arroz', img:'/static/mercado/images/mercearia-produto/arroz.png', price:15.00, sizes:['Saco'], description:'Saco de arroz.'},
    {id:2, name:'Café', img:'/static/mercado/images/mercearia-produto/cafe.png', price:25.00, sizes:['Caoxa'], description:'Embalagem de café 3 corações.'},
    {id:3, name:'Feijão', img:'/static/mercado/images/mercearia-produto/feijao.jpeg', price:13.00, sizes:['Saco'], description:'Saco de feijão.'},
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