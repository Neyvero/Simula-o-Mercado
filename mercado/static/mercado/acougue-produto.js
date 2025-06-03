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
    {id:1, name:'Alcatra', img:'/static/mercado/images/acougue-produto/alcatra.jpg', price:23.00, sizes:['Corte', 'Kg'], description:'Carne alcatra, no precinho.'},
    {id:2, name:'Frango', img:'/static/mercado/images/acougue-produto/frango.png', price:20.00, sizes:['Corte', 'Kg'], description:'Frango da mais alta qualidade, pegue o pedaço ou leve o frango inteiro.'},
    {id:3, name:'Picanha', img:'/static/mercado/images/acougue-produto/picanha.jpg', price:36.00, sizes:['Corte', 'Kg'], description:'Faz o L'}
];

document.querySelector('.produtoInfo--addButton').addEventListener('click', async () => {
  let id = modalKey;
  let produto = produtoJson[id];

  const qt = quantProdutos; 

  const cpf = localStorage.getItem('cpfUsuario');
  if (!cpf) {
    alert('Informe seu CPF antes de adicionar itens.');
    return;
  }

  const payload = {
    descricao: produto.name,
    quantidade: qt,
    preco_unitario: produto.price,
    cpf: cpf 
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
