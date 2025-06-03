document.addEventListener("DOMContentLoaded", () => {
  const seleciona = (elemento) => document.querySelector(elemento);
  const selecionaTodos = (elemento) => document.querySelectorAll(elemento);

  const formatoReal = (valor) => valor.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
  const formatoMonetario = (valor) => valor ? valor.toFixed(2) : '0.00';

  const abrirModal = () => {
    const modal = seleciona('.produtoWindowArea');
    if (modal) {
      modal.style.opacity = 0;
      modal.style.display = 'flex';
      setTimeout(() => modal.style.opacity = 1, 150);
    }
  };

  window.fecharModal = function () {
    const modal = document.querySelector('.produtoWindowArea');
    if (modal) {
      modal.style.opacity = 0;
      setTimeout(() => {
        modal.style.display = 'none';
      }, 500);
    }
  };

  const botoesFechar = () => {
    selecionaTodos('.produtoInfo--cancelButton, .produtoInfo--cancelMobileButton')
      .forEach((item) => item.addEventListener('click', fecharModal));
  };

  const preencheDadosModal = (item) => {
    seleciona('.produtoBig img').src = item.img;
    seleciona('.produtoInfo h1').innerHTML = item.name;
    seleciona('.produtoInfo--desc').innerHTML = item.description;
    seleciona('.produtoInfo--actualPrice').innerHTML = `R$ ${item.price.toFixed(2)}`;
  };

  const pegarKey = (e) => {
    let key = e.target.closest('.produto-item').getAttribute('data-key');
    console.log('Produto clicada ' + key);
    console.log(produtoJson[key]);
    quantProdutos = 1;
    modalKey = key;
    return key;
  };

  const mudarQuantidade = () => {
    const mais = seleciona('.produtoInfo--qtmais');
    const menos = seleciona('.produtoInfo--qtmenos');
    const qt = seleciona('.produtoInfo--qt');

    if (mais && menos && qt) {
      mais.addEventListener('click', () => {
        quantProdutos++;
        qt.innerHTML = quantProdutos;
      });

      menos.addEventListener('click', () => {
        if (quantProdutos > 1) {
          quantProdutos--;
          qt.innerHTML = quantProdutos;
        }
      });
    }
  };

  const cartBtn = document.querySelector(".btn-cart");
  const cartSidebar = document.querySelector(".cart-sidebar");
  const closeBtn = document.querySelector(".close-cart");

  if (cartBtn && cartSidebar && closeBtn) {
    cartBtn.addEventListener("click", () => cartSidebar.classList.add("show"));
    closeBtn.addEventListener("click", () => cartSidebar.classList.remove("show"));

    document.addEventListener("click", (event) => {
      const clickedInsideSidebar = cartSidebar.contains(event.target);
      const clickedCartBtn = cartBtn.contains(event.target);
      if (!clickedInsideSidebar && !clickedCartBtn) {
        cartSidebar.classList.remove("show");
      }
    });
  }

  if (typeof produtoJson !== 'undefined' && Array.isArray(produtoJson)) {
    produtoJson.map((item, index) => {
      let produtoItem = document.querySelector('.models .produto-item').cloneNode(true);
      seleciona('.produto-area').append(produtoItem);

      produtoItem.setAttribute('data-key', index);
      produtoItem.querySelector('.produto-item--img img').src = item.img;
      produtoItem.querySelector('.produto-item--price').innerHTML = `R$ ${item.price.toFixed(2)}`;
      produtoItem.querySelector('.produto-item--name').innerHTML = item.name;
      produtoItem.querySelector('.produto-item--desc').innerHTML = item.description;

      produtoItem.querySelector('.produto-item--add').addEventListener('click', (e) => {
        e.preventDefault();
        let chave = pegarKey(e);
        abrirModal();
        preencheDadosModal(item);
        seleciona('.produtoInfo--qt').innerHTML = quantProdutos;
      });

      botoesFechar();
    });

    mudarQuantidade();
  }
});
