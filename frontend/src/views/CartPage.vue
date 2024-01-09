<script>
import NavBar from "../components/NavBar.vue";

export default {
    data() {
        return {
            cartItems: [],
            cart_id: null,
            processingOrder: false,
        };
    },

    components: {
        NavBar,
    },

    mounted() {
        this.getCartItems();
    },

    methods: {
        async getCartItems() {

            const token = sessionStorage.getItem('token') || localStorage.getItem('token');
            const role = sessionStorage.getItem('role') || localStorage.getItem('role');

            const headers = {
                'token': token,
                'role': role,
                'Content-Type': 'application/json',
            };


            const user_id = localStorage.getItem('user_id') || sessionStorage.getItem('user_id');
            try {
                const response = await this.$http.get(`/cart_items?user_id=${user_id}`, { headers });
                this.cartItems = response.data;
                // this.cart_id = response.data[1].cart_id;
                this.cart_id = this.cartItems[0].cart_id;;
                // console.log("Cart ID", this.cart_id)
                // console.log('Cart Items Response:', response.data);
            } catch (error) {
                console.error('Error getting cart items:', error);
            }
        },

        getProductImage(encodedString) {
            return "data:image/png;base64," + encodedString;
        },

        totalPrice(item) {
            return item.quantity * item.rate_per_unit;
        },


        increaseQuantity(item) {
            item.quantity += 1;
            // POST REQUEST
        },

        decreaseQuantity(item) {
            if (item.quantity > 1) {
                item.quantity -= 1;
                // POST REQUEST
            }
        },

        async proceedToBuy() {

            const token = sessionStorage.getItem('token') || localStorage.getItem('token');
            const role = sessionStorage.getItem('role') || localStorage.getItem('role');

            const headers = {
                'token': token,
                'role': role,
                'Content-Type': 'application/json',
            };

            // GETTING CART ID

            const user_id = localStorage.getItem('user_id') || sessionStorage.getItem('user_id');

            const data = {
                user_id: user_id,
                cart_id: this.cart_id,
            }

            try {
                this.processingOrder = true;
                const response = await this.$http.post('/orders', data, { headers })

                if (response.status === 200) {
                    window.alert('Order successful!');
                    // location.reload();
                    this.$router.push('/')
                } else {
                    console.error('Error placing order:', response);
                }
            } catch (error) {
                console.error('Error placing order:', error);
                window.alert("Can't process this order, please try again after sometime")
            } finally {
                this.processingOrder = false;
            }
        },

        // DELETING ITEMS FROM CART - DELETE REQUEST
        async deleteCartItem(item_id) {
            const token = sessionStorage.getItem('token') || localStorage.getItem('token');
            const role = sessionStorage.getItem('role') || localStorage.getItem('role');
            const headers = {
                'token': token,
                'role': role,
                'Content-Type': 'application/json',
            };

            try {
                window.alert("Are you sure want to delete this product from card?")
                const response = await this.$http.delete(`/cart_items?item_id=${item_id}`, { headers });

                if (response.status === 200) {
                    window.alert("cart item deleted successfully!");
                    this.getCartItems();
                } else {
                    console.log(response.data);
                }
            } catch (error) {
                console.error("Error deleting cart item:", error);
            }
        },
    }
};
</script>

<template>
    <div>
        <NavBar />
        <!-- DO NOT SHOW SUBHEADER IN CART PAGE -->
    </div>
    <!-- EMPTY CART MESSAGE -->
    <div v-if="cartItems.length === 0" class="empty-cart">
        <h2>Your Grocery Cart is empty.</h2>
        <a href="/">Continue Shopping</a>
    </div>
    <br />
    <!-- CART VIEW WHEN CART IS NOT EMPTY -->

    <div v-if="cartItems.length > 0" class="cart-table">
        <h2>Shopping Cart</h2>
        <hr />
        <!-- CART SINGLE PRODUCT CARD -->
        <div v-for="item in cartItems" :key="item.id" class="cart-product-card">
            <div class="row g-0 border rounded overflow-hidden flex-md-row mb-4 shadow-sm h-md-150 position-relative">
                <div class="cart-card">
                    <!-- PRODUCT IMAGE -->
                    <div class="col-auto d-none d-lg-block">
                        <img class="product-image" v-if="item.product_details && item.product_details.product_image"
                            :src="getProductImage(item.product_details.product_image)"
                            alt="{{ item.product_details.product_name }}" width="150" height="170" />
                    </div>
                    <div class="col p-2 d-flex flex-column position-static">
                        <strong class="d-inline-block mb-2 text-primary-emphasis">{{ item.product_details.category
                        }}</strong>
                        <h3 class="mb-0">{{ item.product_details.product_name }}</h3>
                        <div class="mb-1 text-body-secondary">Exp Date: {{ item.product_details.exp_date }}</div>
                        <!-- QUANTITY INCREASE/DECREASE -->
                        <div class="quantity-control">
                            <label for="quantity" class="lbl-qty">Quantity : </label>
                            <div class="quantity-buttons">
                                <button class="qty-decrease" @click="decreaseQuantity(item)"
                                    :disabled="item.quantity === 1">-</button>
                                <span class="quantity-value">{{ item.quantity }}</span>
                                <button class="qty-increase" @click="increaseQuantity(item)">+</button>
                            </div>
                        </div>
                        <!-- PRICE -->
                        <!-- <p class="product-price">{{ `₹ ${item.rate_per_unit.toFixed(2)}` }}</p> -->
                        <p class="product-price">{{ `₹${totalPrice(item).toFixed(2)}` }}</p>
                        <!-- ACTION -->
                        <button class="delete-button" @click="deleteCartItem(item.id)">
                            <!-- class="button-content" -->
                            <span>
                                Delete
                                <font-awesome-icon :icon="['fas', 'trash']" class="icon-large" />
                            </span>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- CART TOTAL -->
    <div v-if="cartItems.length > 0" class="cart-value">
        <div class="">
            <h4 class="d-flex justify-content-between align-items-center mb-3">
                <span class="text-primary">Your cart</span>
                <span class="badge bg-primary rounded-pill">{{ cartItems.length }}</span>
            </h4>
            <ul class="list-group mb-3">
                <li v-for="item in cartItems" :key="item.id" class="list-group-item d-flex justify-content-between lh-sm">
                    <div>
                        <h6 class="my-0">{{ item.product_details.product_name }}</h6>
                        <small class="text-body-secondary">Details: {{ `₹ ${item.rate_per_unit.toFixed(2)}` }} X {{
                            item.quantity }}</small>
                    </div>
                    <span class="text-body-secondary">{{ `₹ ${totalPrice(item).toFixed(2)}` }}</span>
                </li>
            </ul>
            <div class="card p-2">
                <!-- <button class="checkout-button" @click="proceedToBuy">Proceed to Buy</button> -->
                <button class="checkout-button" @click="proceedToBuy" :disabled="processingOrder">
                    {{ processingOrder ? 'Processing...' : 'Proceed to Buy' }}
                </button>
            </div>
        </div>
    </div>
</template>

<style scoped>
/* ########################################################################## */
/* ######################### EMPTY CART MESSAGE ############################# */
.empty-cart {
    display: block;
    background: #d1cfcf;
    width: 65%;
    margin-top: 150px;
    margin-left: 10px;
    padding: 10px 20px;
}

/* ########################################################################## */
/* ################# SHOPPING CART WITH PRODUCT ############################# */

/* .cart-table {
    display: inline-block;
    background: #d1cfcf;
    width: 65%;
    padding: 10px 20px;
    margin-left: 10px;
} */

@media (max-width: 768px) {

    .cart-table {
        width: 100%;
        margin-left: 0;
    }

    .cart-value {
        width: 100%;
        margin-left: 0;
    }
}

.cart-card {
    display: flex;
    align-items: center;
    padding: 2px;
}


.cart-table {
    /* display: inline-block; */
    float: left;
    background: #d1cfcf;
    width: 65%;
    margin-left: 10px !important;
    padding: 10px 20px;
}

.cart-value {
    float: left;
    /* display: inline-block; */
    width: 30%;
    margin-left: 10px;
}

/* ############################################################ */
/* ################# PRODUCT CARD ############################# */
.cart-product-card {
    width: 70%;
    max-height: fit-content;
    background: white;
}



.product-price {
    font-size: 18px;
    font-weight: bold;
    color: #007bff;
    margin: 10px 0;
}

/* ################################################################## */
/* ################# QUANTITY SELECTION ############################# */


.quantity-control {
    display: flex;
    align-items: center;
}

.qty-decrease,
.qty-increase {
    border: none;
    padding: 2px;
    background: linear-gradient(to right, #ff7e5f, #feb47b);
    padding: 3px 15px;
    cursor: pointer;
    border-radius: 5px;
    font-size: larger;
    font-weight: bold;
}

.qty-decrease {
    margin-right: 5px;
}

.qty-increase {
    margin-left: 5px;
}

.qty-increase:hover,
.qty-decrease:hover {
    background: linear-gradient(to right, #ff6a3f, #fda95c);
}

.lbl-qty,
.quantity-value {
    font-weight: bold;
    padding: 5px;
}

/* ############################################################## */
/* ################# DELETE BUTTON ############################# */

.delete-button {
    background: #ff0000;
    color: #fff;
    border: none;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: 5px;
    padding: 10px 50px;
    cursor: pointer;
    font-weight: bold;
    width: auto;
    transition: background-color 0.2s;
}

.delete-button:hover {
    background: #cc0000;
}

.checkout-button {
    background: linear-gradient(45deg, #FFA500, #FFD700);
    color: rgb(9, 13, 11);
    font-weight: Bold;
    font-size: 18px;
    border: none;
    border-radius: 5px;
    padding: 7px;
}
</style>
