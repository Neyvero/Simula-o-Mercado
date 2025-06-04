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
    {id:1, name:'Pão Francês', img:'/static/mercado/images/padaria-produto/pao-frances.png', price:0.99, sizes:['Unidade', 'kg'], description:'Pão francês, o mais quentinho e macio da região'},
    {id:2, name:'Bolo', img:'/static/mercado/images/padaria-produto/bolo.jpg', price:12.99, sizes:['Unidade'], description:'Bolo, vendido inteiro em embalagem.'},
    {id:3, name:'Rosquinha', img:'/static/mercado/images/padaria-produto/rosquinha.jpg', price:2.99, sizes:['Unidade', 'kg'], description:'Rosquinha, doce e açucarada como a vida deve ser.'}
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