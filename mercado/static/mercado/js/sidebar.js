document.addEventListener("DOMContentLoaded", () => {
  const cartItemsContainer = document.querySelector('.cart-items');
  const cartTotalElement = document.querySelector('.cart-total');
  const cartCountElement = document.querySelector('.cart-count');

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

  async function carregarCarrinho() {
    try {
      const response = await fetch('/api/carrinho/', {
        headers: {
          'X-Requested-With': 'XMLHttpRequest'
        }
      });

      if (!response.ok) {
        console.error('Erro ao carregar carrinho');
        return;
      }

      const data = await response.json();

      cartItemsContainer.innerHTML = '';
      let total = 0;
      let count = 0;

      data.itens.forEach(item => {
        const itemHTML = document.createElement('div');
        itemHTML.classList.add('cart-item');
        itemHTML.innerHTML = `
          <div>${item.descricao}</div>
          <div class="cart--item-qtarea" data-id="${item.id}">
            <button class="cart--item-qtmenos">-</button>
            <span>${item.quantidade}</span>
            <button class="cart--item-qtmais">+</button>
          </div>
          <div>${item.quantidade} x R$ ${parseFloat(item.preco_unitario).toFixed(2)}</div>
        `;
        cartItemsContainer.appendChild(itemHTML);

        total += item.quantidade * parseFloat(item.preco_unitario);
        count += item.quantidade;

        itemHTML.querySelector('.cart--item-qtmais').addEventListener('click', async () => {
          await atualizarQuantidade(item.id, item.quantidade + 1);
        });

        itemHTML.querySelector('.cart--item-qtmenos').addEventListener('click', async () => {
          await atualizarQuantidade(item.id, item.quantidade - 1);
        });
      });

      cartTotalElement.textContent = `R$ ${total.toFixed(2)}`;
      cartCountElement.textContent = count;
    } catch (err) {
      console.error('Erro ao buscar carrinho:', err);
    }
  }

  async function atualizarQuantidade(id, novaQt) {
    try {
      const response = await fetch(`/api/carrinho/${id}/atualizar_quantidade/`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({ quantidade: novaQt })
      });

      if (response.ok) {
        window.recarregarCarrinho();
      } else {
        console.error('Erro ao atualizar quantidade');
      }
    } catch (err) {
      console.error('Erro:', err);
    }
  }

  document.querySelector('.btn-clear-cart')?.addEventListener('click', async () => {
    try {
      const response = await fetch('/api/carrinho/limpar/', {
        method: 'DELETE',
        headers: {
          'X-CSRFToken': getCSRFToken()
        }
      });

      if (response.ok) {
        window.recarregarCarrinho();
      } else {
        alert('Erro ao limpar carrinho.');
      }
    } catch (err) {
      console.error('Erro:', err);
    }
  });

  document.querySelector('.btn-finalizar-compra')?.addEventListener('click', async () => {
    try {
      const response = await fetch('/api/carrinho/finalizar/', {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCSRFToken()
        }
      });

      if (response.ok) {
        window.recarregarCarrinho();
        alert('Compra finalizada com sucesso!');
      } else {
        alert('Erro ao finalizar compra.');
      }
    } catch (err) {
      console.error('Erro:', err);
    }
  });

  carregarCarrinho();
  window.recarregarCarrinho = carregarCarrinho;
});
