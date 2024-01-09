<template>
  <div class="container">
    <div class="row">
      <div v-for="product in products" :key="product.id" class="col-md-3 mx-auto">
        <div class="product-card">
          <div>
            <img class="product-image" v-if="product.product_image" :src="getProductImage(product.product_image)"
              alt="{{ product.product_name }}" />
          </div>
          <div class="product-details">
            <div class="basic-details">
              <div>
                <div class="product-name">{{ product.product_name }}</div>
                <div class="manufacture-date"> Mfg. Date : {{ product.mfg_date }}</div>
                <div class="qty-lbl">Quantity:</div>
              </div>
              <div class="product-price">₹{{ product.rate_per_unit }}</div>
            </div>
            <div class="qty-cart">
              <!-- <label for="quantity">Quantity:</label> -->
              <select class="quantity-dropdown" v-model="selectedQuantity[product.id]" id="quantity">
                <option selected hidden>Quantity</option>
                <option v-for="quantity in getQuantity(product.quantity)" :key="quantity">{{ quantity }}</option>
              </select>
              <button @click="addToCart(product)" class="add-to-cart-btn">{{ product.quantity === 0 ? 'Out of Stock' : 'Add to Cart' }}
                <svg v-if="product.quantity > 0" class="cart-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
                  <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g>
                  <g id="SVGRepo_iconCarrier">
                    <path
                      d="M6.29977 5H21L19 12H7.37671M20 16H8L6 3H3M9 20C9 20.5523 8.55228 21 8 21C7.44772 21 7 20.5523 7 20C7 19.4477 7.44772 19 8 19C8.55228 19 9 19.4477 9 20ZM20 20C20 20.5523 19.5523 21 19 21C18.4477 21 18 20.5523 18 20C18 19.4477 18.4477 19 19 19C19.5523 19 20 19.4477 20 20Z"
                      stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path>
                  </g>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { isLoggedIn } from '../router/routeAuth'

export default {
  data() {
    return {
      products: [],
      selectedQuantity: {},
    };
  },
  methods: {
    // GET PRODUCTS
    async getProducts() {
      try {
        const response = await this.$http.get('/products');
        this.products = response.data;
        console.log(response)
      } catch (error) {
        console.error('Error fetching products:', error);
      }
    },

    // GETTING IMAGE
    getProductImage(encodedString) {
      return "data:image/png;base64," + encodedString;
    },

    // GETTING QUANTITY
    getQuantity(maxQuantity) {
      return Array.from({ length: maxQuantity }, (_, index) => index + 1);
    },

    // ADD TO CART FUNCTION
    async addToCart(product) {
      const productId = product.id;
      const quantity = this.selectedQuantity[productId];

      if (!quantity || quantity <= 0) {
        window.alert('Please select a valid quantity.');
        return;
      }

      const token = sessionStorage.getItem('token') || localStorage.getItem('token');
      const role = sessionStorage.getItem('role') || localStorage.getItem('role');

      const headers = {
        'token': token,
        'role': role,
        'Content-Type': 'application/json',
      };

      try {
        const user_id = localStorage.getItem('user_id') || sessionStorage.getItem('user_id');
        const response = await this.$http.post('/cart', { user_id, product_id: productId, quantity }, { headers });

        if (response.status === 200) {
          window.alert("Product added to cart successfully!");
          // console.log("Product added to cart successfully!")
          // console.log("Response:", response); 
          this.getProducts();
        } else {
          console.log("Error response data", response.data);
        }

      } catch (error) {
        window.alert('Error adding item to the cart. Please try again.');
        console.error('Error adding item to the cart:', error);
      }

    },
  },

  mounted() {
    this.getProducts();
  },

};
</script>


<style scoped>
.product-card {
  max-width: 400px;
  margin: 20px auto;
  background: #ffffff;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  overflow: hidden;
}

.product-image {
  width: 100%;
  height: 250px;
  object-fit: cover;
  padding: 5px;
}

.product-details {
  padding: 5px;
}

.product-name {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 5px;
}

.manufacture-date {
  font-size: 0.9rem;
  color: #555555;
  margin-bottom: 3px;
}

.qty-lbl {
  font-size: small;
  font-weight: bold;
}

.quantity-dropdown {
  width: 100%;
  padding: 5px;
  margin-bottom: 10px;
}

.add-to-cart-btn {
  width: 100%;
  padding: 3px;
  background-color: #007bff;
  color: #ffffff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-left: 20px;
  margin-bottom: 10px;
}


.product-price {
  font-size: 16px;
  font-weight: bold;
  margin: 10px;
  text-align: right;
}

.basic-details {
  display: flex;
  justify-content: space-between;
}

.qty-cart {
  display: flex;
  justify-content: space-between;
}

.cart-icon {
  width: 20px;
}

@media (max-width:576px) {
  .product-card {
    max-width: 100%;
  }
}
</style>