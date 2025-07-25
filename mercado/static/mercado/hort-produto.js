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
    {id:1, name:'Banana', img:'/static/mercado/images/hort-produto/banana.jpg', price:3.00, sizes:['Unidade', 'Cacho'], description:'Banana fresca, venda por unidade ou por cacho.'},
    {id:2, name:'Maçã', img:'/static/mercado/images/hort-produto/maca.jpg', price:3.50, sizes:['Unidade', 'Kg'], description:'Maçã colhidas do pé mais belo de macieira, Unidade ou Kg.'},
    {id:3, name:'Tomate', img:'/static/mercado/images/hort-produto/tomate.jpg', price:4.00, sizes:['Unidade', 'Kg'], description:'Tomate, natural sem agrotóxicos, Unidade ou Kg.'},
    {id:4, name:'Uva', img:'/static/mercado/images/hort-produto/uva.jpg', price:4.99, sizes:['Unidade', 'Cacho'], description:'Uva, crescida no vinhedo mais cique, Unidade ou Cacho.'}
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