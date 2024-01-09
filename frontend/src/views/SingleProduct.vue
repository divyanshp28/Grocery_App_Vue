<template>
    <NavBar />
    <div class="product-card">
        <div v-if="product" class="product-details">
            <img class="product-image" v-if="product.product_image" :src="getProductImage(product.product_image)"
                alt="{{ product.product_name }}" />
            <div class="product-info">
                <h2>{{ product.product_name }}</h2>
                <p class="qtly">Quantity:
                <div class="qty-cart">
                    <!-- <label for="quantity">Quantity:</label> -->
                    <select class="quantity-dropdown" v-model="selectedQuantity[product.id]" id="quantity">
                        <option selected hidden>Quantity</option>
                        <option v-for="quantity in getQuantity(product.quantity)" :key="quantity">{{ quantity }}</option>
                    </select>
                </div>
                </p>
                <p>Manufacturing Date: {{ product.mfg_date }}</p>
                <p>Expiration Date: {{ product.exp_date }}</p>
                <p>Rate per Unit: ₹{{ product.rate_per_unit }}</p>
            </div>
        </div>
        <button @click="addToCart(product)" class="add-to-cart-btn">Add to Cart
            <svg class="cart-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
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
</template>
  
<script>
import NavBar
    from '../components/NavBar.vue';
export default {
    components: {
        NavBar,
    },

    data() {
        return {
            product: {},
            selectedQuantity: {},
        };
    },

    methods: {
        async getProducts() {
            try {
                console.log('query Params:', this.$route.query);
                const product_id = this.$route.query.product_id;
                const response = await this.$http.get(`/products?product_id=${product_id}`);
                this.product = response.data;
                this.product = response.data;
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
  max-width: 600px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.product-details {
    display: flex;
    max-width: 600px;
    margin: 0 auto;
}

.product-image {
    width: 200px;
    height: 200px;
    object-fit: cover;
    margin-right: 20px;
}

.product-info {
    flex: 1;
}

.add-to-cart-btn {
    width: 100%;
    height: 60px;
    padding: 3px;
    background-color: #007bff;
    color: #ffffff;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    margin-left: 20px;
    margin-bottom: 10px;
    margin-top: 10px;
}

.cart-icon {
    width: 20px;
}

.quantity-dropdown {
    padding: 3px;
    width: 100px;
    margin-left: 5px;
}

.qtly{
    display: flex;
    align-items: center;
}

</style>
  