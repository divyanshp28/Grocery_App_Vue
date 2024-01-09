<script>
import NavBar from '../components/NavBar.vue';
export default {
    data() {
        return {
            category_name: '',
            categories: [],

            // EDIT CATEGORY
            isModalOpen: false,
            categoryId: null,

            // REQUESTS
            requests: [],
            requestId: null,
            users: [],

            //PRODUCTS
            category_id: '',
            products: [],
            filteredProducts: [],
            // Filter
            selectedCategory: "",
            productId: null,

        }
    },
    components: {
        NavBar
    },

    methods: {
        // METHOD TO POST CATEGORY
        async postCategory() {
            const token = sessionStorage.getItem('token') || localStorage.getItem('token');
            const role = sessionStorage.getItem('role') || localStorage.getItem('role')

            const headers = {
                'token': token,
                'role': role,
                'Content-Type': 'application/json'
            };

            // console.log('Headers:', headers);
            console.log(this.$data)
            const response = await this.$http.post('/categories',
                { category_name: this.category_name }, { headers }
            );

            if (response.status === 200) {
                window.alert("Category added succesfully!")
                this.$router.push('/admin')
                this.category_name = '';
                this.getCategories();
            } else {
                console.log(response.data)
            }
        },

        // GET REQUEST FOR CATEGORIES
        async getCategories() {
            const token = sessionStorage.getItem('token') || localStorage.getItem('token');
            const role = sessionStorage.getItem('role') || localStorage.getItem('role')

            const headers = {
                'token': token,
                'role': role,
                'Content-Type': 'application/json'
            };

            const response = await this.$http.get('/categories', { headers });
            this.categories = response.data
            // console.log(response.data)
        },

        // EDITING CATEGORIES - PUT REQUEST

        openModal() {
            this.isModalOpen = true;
        },
        closeModal() {
            this.isModalOpen = false;
        },

        // EDIT PRODUCT
        async editCategory() {
            if (!this.categoryId) {
                console.error('Category ID not provided');
                return;
            }

            const formData = new FormData();
            formData.append('category_name', this.category_name);

            try {
                const token = sessionStorage.getItem('token') || localStorage.getItem('token');
                const role = sessionStorage.getItem('role') || localStorage.getItem('role');
                const response = await this.$http.put(`/categories?category_id=${this.categoryId}`, formData, {
                    headers: {
                        'Content-Type': 'application/json',
                        'token': token,
                        'role': role,
                    },
                });

                if (response.status === 200) {
                    window.alert('Category updated successfully!');
                    this.closeModal();
                    location.reload();
                } else {
                    console.error('Error updating Category:', response);
                }
            } catch (error) {
                console.error('Error updating category:', error);
            }
        },

        // Edit modal with category name
        openEditModal(category) {
            this.categoryId = category.id;
            this.category_name = category.category_name;

            // Open the edit modal
            this.openModal();
        },

        // DELETING CATEGORIES - DELETE REQUEST
        async deleteCategory(categoryId) {
            const token = sessionStorage.getItem('token') || localStorage.getItem('token');
            const role = sessionStorage.getItem('role') || localStorage.getItem('role');
            const headers = {
                'token': token,
                'role': role,
                'Content-Type': 'application/json',
            };

            try {
                window.alert("Are you sure want to delete this category?")
                const response = await this.$http.delete(`/categories?category_id=${categoryId}`, { headers });

                if (response.status === 200) {
                    window.alert("Category deleted successfully!");
                    this.getCategories();
                } else {
                    console.log(response.data);
                }
            } catch (error) {
                console.error("Error deleting category:", error);
            }
        },

        // GETTING REQUESTS SENT BY STORE ADMINS

        async getRequests() {
            const token = sessionStorage.getItem('token') || localStorage.getItem('token');
            const role = sessionStorage.getItem('role') || localStorage.getItem('role')

            const headers = {
                'token': token,
                'role': role,
                'Content-Type': 'application/json'
            };

            try {
                const response = await this.$http.get('/store_admin_request', { headers });
                this.requests = response.data;
                console.log("Requests response:", response)
            } catch (error) {
                console.error('Error getting requests:', error);
            }

        },

        async getUsers() {
            try {
                const token = sessionStorage.getItem('token') || localStorage.getItem('token');
                const role = sessionStorage.getItem('role') || localStorage.getItem('role');

                const headers = {
                    'token': token,
                    'role': role,
                    'Content-Type': 'application/json',
                };

                const response = await this.$http.get('/users', { headers });

                this.users = response.data;
            } catch (error) {
                console.error('Error fetching users:', error);
            }
        },

        // FILTERING / GETTING PRODUCTS
        async filterProducts() {
            try {
                let response;

                // If a category is selected
                if (this.selectedCategory) {
                    response = await this.$http.get(`/products?category_id=${this.selectedCategory}`);
                    console.log("Selected category:", this.selectedCategory)
                    this.filteredProducts = response.data
                    console.log('Filtered products', response.data);
                } else {
                    response = await this.$http.get('/products');
                    this.products = response.data;
                    console.log('All products', response.data);
                }


                this.products = response.data;
            } catch (error) {
                console.error("Error fetching products");
            }
        },

        // GETTING IMAGE
        getProductImage(encodedString) {
            return "data:image/png;base64," + encodedString;
        },

        //-------------------------HANDLING REQUESTS----------------------------
        // APPROVE REQUEST

        async approveRequest(request) {
            const token = sessionStorage.getItem('token') || localStorage.getItem('token');
            const role = sessionStorage.getItem('role') || localStorage.getItem('role')

            const headers = {
                'token': token,
                'role': role,
                'Content-Type': 'application/json'
            };

            const formData = new FormData();
            formData.append('status', 'completed');


            try {
                if (request.status == "Pending" && request.request_type == "Requesting to be store admin") {
                    const response = await this.$http.put(`/store_admin_request?request_id=${request.id}`, formData, { headers });

                    if (response.status === 200) {
                        const user = this.users.find((user) => user.id === request.user_id);
                        if (user) {
                            user.role = 'store_admin';
                        }
                        window.alert('Request Approved!');
                        this.removeEntry(request.id);
                        location.reload();
                    } else {
                        console.error('Error updating Category:', response);
                    }
                }
            } catch (error) {
                console.error("An error occured")
            }
        },

        // REJECTING REQUEST
        async rejectRequest(request) {
            const token = sessionStorage.getItem('token') || localStorage.getItem('token');
            const role = sessionStorage.getItem('role') || localStorage.getItem('role')

            const headers = {
                'token': token,
                'role': role,
                'Content-Type': 'application/json'
            };

            try {
                if (request.status === "Pending" && request.request_type === "Requesting to be store admin") {
                    const response = await this.$http.delete(`/store_admin_request?request_id=${request.id}`, { headers });

                    if (response.status === 200) {
                        this.removeEntry(request.id);

                        window.alert('Request Rejected!');
                        location.reload();
                    } else {
                        console.error('Error rejecting request:', response);
                    }
                }
            } catch (error) {
                console.error("An error occurred")
            }
        },

        // REMOVING ENTRY FROM TABLE AFTER APPROVAL OR REJECTION
        removeEntry(requestId) {
            const index = this.requests.findIndex(request => request.id === requestId);
            if (index !== -1) {
                this.requests.splice(index, 1);
            }
        },

    },

    computed: {
        filteredProducts() {
            if (!this.selectedCategory) {
                return this.products;
            }
            return this.products.filter((product) => product.category_id === this.selectedCategory);
        },
    },

    mounted() {
        this.getCategories();
        this.getRequests();
        this.filterProducts();
        this.getUsers();
    },
};
</script>


<template>
    <div>
        <NavBar />
    </div>
    <div class="category">
        <p class="section-1">Admin Dashboard - Category Management</p>
        <div class="category-management">
            <div class="form-container">
                <p class="form-title">Add Category</p>
                <form @submit.prevent="postCategory">
                    <label for="name" class="category-name">Name:</label>
                    <input type="text" v-model="category_name" id="category_name" name="category_name" required>
                    <button type="submit" class="btn">Add Category</button>
                </form>
            </div>
            <!-- ADDED CATEGORIES TABLE STARTS -->
            <div class="table-section">
                <p class="table-title">Added Categories</p>
                <table>
                    <thead>
                        <tr>
                            <th>S.No</th>
                            <th>Category Name</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(category, index) in categories" :key="index">
                            <td>{{ index + 1 }}.</td>
                            <td>{{ category.category_name }}</td>
                            <td>
                                <button>
                                    <font-awesome-icon @click="openEditModal(category)" :icon="['fas', 'pen-to-square']"
                                        class="edit-button" data-bs-toggle="modal" data-bs-target="#edit_category_modal" />
                                </button>
                                <button>
                                    <font-awesome-icon :icon="['fas', 'trash']" class="delete-button"
                                        @click="deleteCategory(category.id)" />
                                </button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <!-- ADDED CATEGORIES TABLE ENDS -->
        </div>
        <!-- REQUEST TABLE STARTS -->
        <div class="rqst-table-parent-div">
            <div class="table-section">
                <p class="table-title">Requests</p>
                <p class="table-info">(Requests from users to get role of Store Admin)</p>
                <table>
                    <thead>
                        <tr>
                            <th>S.No</th>
                            <th>Name</th>
                            <th>Username</th>
                            <th>Category Name</th>
                            <th>Request Message</th>
                            <th>Status</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(request, index) in requests" :key="index">
                            <td>{{ request.id }}</td>
                            <td>{{ request.full_name }}</td>
                            <td>{{ request.username }}</td>
                            <td>{{ request.category_name }}</td>
                            <td>{{ request.request_type }}</td>
                            <td>{{ request.status }}</td>
                            <td>
                                <button @click="approveRequest(request)">
                                    <font-awesome-icon :icon="['fas', 'square-check']" class="approve-button" />
                                </button>
                                <button @click="rejectRequest(request)">
                                    <font-awesome-icon :icon="['fas', 'xmark']" class="delete-button" />
                                </button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
        <!-- REQUEST TABLE ENDS -->
    </div>

    <p class="section-1">Inventory</p>
    <!-- PRODUCT TABLE STARTS -->
    <div class="table-section">
        <div class="filter-products">
            <div>
                <p class="table-title">Products</p>
                <p class="table-info">(Products in Category)</p>
            </div>
            <!-- DROPDOWN TO FILTER PRODUCTS BASED ON CATEGORIES -->
            <div class="category-dropdown">
                <label for="category-dropdown" class="category-dropdown-label">Select Category:</label>
                <select v-model="selectedCategory" @change="filterProducts">
                    <option value="" selected>All Categories</option>
                    <option v-for="category in categories" :key="category.id" :value="category.id">
                        {{ category.category_name }}
                    </option>
                </select>
            </div>
        </div>
        <table>
            <thead>
                <tr>
                    <th>S.No</th>
                    <th>Product Image</th>
                    <th>Product Name</th>
                    <th>Quantity Remaining</th>
                    <th>Rate per unit</th>
                    <th>Mfg Date</th>
                    <th>Exp Date</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <!-- <tr v-for="(product, index) in filteredProducts" :key="product.id"> -->
                <tr v-for="(product, index) in filteredProducts" :key="index" v-if="filteredProducts.length > 0">
                    <td>{{ index + 1 }}</td>
                    <!-- <td>{{ product.category_name }}</td> -->
                    <td>
                        <div>
                            <img class="product-image" v-if="product.product_image"
                                :src="getProductImage(product.product_image)" alt="{{ product.product_name }}" />
                        </div>
                    </td>
                    <td>{{ product.product_name }}</td>
                    <td>{{ product.quantity }}</td>
                    <td>{{ product.rate_per_unit }}</td>
                    <td>{{ product.mfg_date }}</td>
                    <td>{{ product.exp_date }}</td>
                    <td>
                        <button @click="openEditModal(product)" data-bs-toggle="modal" data-bs-target="#edit-product-modal"
                            data-bs-whatever="@getbootstrap">
                            <font-awesome-icon :icon="['fas', 'pen-to-square']" class="edit-button" />
                        </button>
                        <button @click="deleteProduct(index)">
                            <font-awesome-icon :icon="['fas', 'trash']" class="delete-button"
                                @click="deleteProduct(product.id)" />
                        </button>
                    </td>
                </tr>
                <tr v-else>
                    <td colspan="8">No products available for the selected category.</td>
                </tr>

            </tbody>

        </table>
    </div>
    <!-- PRODUCT TABLE ENDS -->

    <!-- Edit Category Modal -->
    <div class="modal fade" id="edit_category_modal" tabindex="-1" aria-labelledby="edit_category_modal" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Edit Category</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <form @submit.prevent="editCategory">
                    <div class="modal-body">
                        <label for="category_name" class="category-name">Name:</label>
                        <input type="text" v-model="category_name" id="category_name" name="category_name" required>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button type="submit" class="btn btn-primary">Save changes</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<style scoped>
.section-1 {
    width: 100%;
    background: #56cca9;
    text-align: center;
    padding: 12px;
    font-size: 25px;
    font-weight: bold;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 20px;
    margin-top: 20px;
}


.filter-products {
    display: flex;
    position: center;
    justify-content: center;
}

.product-image {
    width: 30px;
}


.category-management {
    display: flex;
    align-items: center;
    justify-content: center;
}

.rqst-table-parent-div {
    padding: 10px;
    margin-top: 20px;
}


.form-container {
    width: 300px;
    height: 200px;
    margin: 0 20px;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 5px;
    background-color: #f9f9f9;
}

.form-title {
    font-size: 20px;
    font-weight: bold;
    margin-bottom: 10px;
}

/* Name label for Category */
.category-name {
    display: block;
    margin-top: 10px;
    font-weight: bold;
}

/* Form to add category */
#category_name {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    margin-top: 5px;
}


.btn {
    background-color: #007bff;
    color: #fff;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    margin-top: 10px;
}

.btn:hover {
    background-color: #0056b3;
}

/* ############################################################ */
/* #################### TABLE DESIGN ########################## */

.table-section {
    max-height: 400px;
    margin-right: 10px;
    border-radius: 5px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.15);
    overflow: auto;
    background-color: #f9f9f9;
}

.table-title {
    font-size: 20px;
    font-weight: bold;
    text-align: center;
    margin-top: 5px;
    margin-bottom: 5px;
}

.table-info {
    text-align: center;
}


table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
}

thead th {
    background-color: #a0f2da;
    color: #3c3b3b;
    font-weight: 600;
    padding: 10px 20px;
    text-align: center;
    font-size: small;
}

td {
    padding: 10px;
    text-align: center;
    font-size: small;
}

tr:nth-child(even) {
    background-color: #d4d4d4;
}

tr:hover {
    background-color: #e6f7ff;
    cursor: pointer;
}

/* SCROLLBAR STYLING */
.table-section::-webkit-scrollbar {
    width: 5px;
    height: 5px;
}

.table-section::-webkit-scrollbar-thumb {
    background: #888;
    border-radius: 5px;
}

.table-section::-webkit-scrollbar-track {
    background: #f1f1f1;
}

/* TRY TO CREATE BUTTONS AS COMPONENTS */
/* STYLING ACTION BUTTONS */

button {
    border: none;
    outline: none;
    background-color: inherit;
    cursor: pointer;
}

.edit-button {
    color: #007bff;
}


.delete-button {
    color: #ff0000;
    margin-left: 10px;
}

.approve-button {
    color: #3a9b11;
}

.edit-button:hover,
.delete-button:hover,
.approve-button:hover {
    transform: scale(1.5);
}

@media (max-width: 768px) {
    .category-management {
        flex-direction: column;
    }

    .table-section {
        overflow-x: auto;
        margin-bottom: 20px;
    }
}
</style>