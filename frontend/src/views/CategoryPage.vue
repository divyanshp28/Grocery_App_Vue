<template>
  <div>
    <NavBar />

    <!-- CURRENT CATEGORY NAME -->
    <div class="container mt-2">
      <h2>{{ selectedCategory ? selectedCategory.category_name : 'All Products' }}</h2>
    </div>

    <div class="container mt-4">
      <div  v-if="filteredProducts.length > 0" class="row">
        <div v-for="product in filteredProducts" :key="product.id" :product="product"
          class="col-lg-3 col-md-6 col-sm-6 mb-4">
          <div class="card">
            <img class="product-image" v-if="product.product_image" :src="getProductImage(product.product_image)"
              alt="{{ product.product_name }}" />
            <div class="card-body">
              <div class="name-rate">
                <h5 class="card-title">{{ product.product_name }}</h5>
                <p class="card-text">₹{{ product.rate_per_unit }}</p>
              </div>
              <p class="card-text">Mfg Date: {{ product.mfg_date }}</p>
              <p class="qty-lbl">Quantity: </p>
              <div class="qty-cart-btn">
                <select v-model="selectedQuantity[product.id]" class="form-select mb-2" aria-label="Quantity">
                  <option v-for="quantity in getQuantity(product.quantity)" :key="quantity">
                    {{ quantity }}
                  </option>
                </select>
                <button @click="addToCart(product)" class="btn btn-primary">{{ product.quantity === 0 ? 'Out of Stock' : 'Add to Cart' }}</button>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-else>
        <h2 class="card-title">No products to display in this category.</h2>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from "../components/NavBar.vue";
import ProductCard from "../components/ProductCard.vue";

export default {
  data() {
    return {
      selectedCategory: null,
      filteredProducts: [],
      selectedQuantity: {},
    };
  },

  components: {
    NavBar,
    ProductCard,
  },

  methods: {
    // FILTERING / GETTING PRODUCTS
    async filterProducts() {
      try {
        console.log('Selected category:', this.selectedCategory);

        const category_id = this.selectedCategory ? this.selectedCategory.id : null;

        const response = await this.$http.get('/products', { params: { category_id } });

        this.filteredProducts = response.data;
      } catch (error) {
        console.error('Error fetching products', error);
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
          this.filterProducts();
        } else {
          console.log("Error response data", response.data);
        }

      } catch (error) {
        window.alert('Error adding item to the cart. Please try again.');
        console.error('Error adding item to the cart:', error);
      }

    },
  },

  // WATCH => CHANGES IN ROUTE QUERY PARAM AND DISPLAY CATGORIES ACCORDINGLY
  watch: {
    // selectedCategory: "filterProducts",
    $route(to, from) {
    const categoryId = to.query.category_id;

    this.selectedCategory = categoryId ? { id: categoryId } : null;

    this.filterProducts();
  },
  },

  created() {
    const category_id = this.$route.query.category_id;
    if (category_id) {
      this.selectedCategory = { id: category_id };
    }
    this.filterProducts();
  },

};
</script>


<style scoped>
/* .card {
  transition: transform 0.2s;
}

.card:hover {
  transform: scale(1.05);
} */

.product-image {
  width: 100%;
  height: 250px;
  object-fit: cover;
  padding: 5px;
}

.card-img-top {
  max-height: 200px;
  object-fit: cover;
  margin: 2px;
}

.card-title {
  font-size: 1.2rem;
  margin: 2px;
}

.card-text {
  color: #6c757d;
  margin: 2px;
}

.btn-primary {
  width: 100%;
  margin-left: 2px;
  font-size: small;
}

.qty-cart-btn {
  display: flex;
}

.qty-lbl {
  margin: 0;
}

.name-rate {
  display: flex;
  justify-content: space-between;
}
</style>
