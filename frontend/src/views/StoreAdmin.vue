<script>
import NavBar from '../components/NavBar.vue';

export default {
    data() {
        return {
            isModalOpen: false,
            // CATEGORIES
            categories: [],

            // ADDING PRODUCTS
            category_name: '',
            product_name: '',
            product_image: null,
            quantity: '',
            mfg_date: '',
            exp_date: '',
            rate_per_unit: '',
            category_id: '',
            products: [],
            filteredProducts: [],
            // Filter
            selectedCategory: "",
            productId: null,
            //REQUESTING TO ADD NEW CATEGORY
            newCategory: '',
        };
    },
    components: {
        NavBar
    },
    methods: {
        openModal() {
            this.isModalOpen = true;
        },
        closeModal() {
            this.isModalOpen = false;
        },

        // SETTING CATEGORY ID
        setCategoryId(id) {
            console.log("category_id:", id);
            this.category_id = id;
        },

        // ADDING PRODUCT
        async addProduct() {

            // FORM VALIDATION
            if (!this.product_name || !this.quantity || !this.mfg_date || !this.exp_date || !this.rate_per_unit) {
                window.alert('Please fill in all required fields.');
                return;
            }

            const formData = new FormData();
            formData.append('category_id', this.category_id);
            formData.append('product_name', this.product_name);
            formData.append('product_image', this.product_image);
            formData.append('quantity', this.quantity);
            formData.append('mfg_date', this.mfg_date);
            formData.append('exp_date', this.exp_date);
            formData.append('rate_per_unit', this.rate_per_unit);

            const response = await this.$http.post('/products', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });



            if (response.status === 200) {
                window.alert('Product added successfully!');
                this.closeModal();
                location.reload()
            } else {
                // console.error('Error adding product:', response);
                console.error('Error adding product:', error);
            }
        },

        // HANDLING IMAGE UPLOAD
        handleFileChange(event) {
            this.product_image = event.target.files[0];
        },

        // GET REQUEST FOR CATEGORIES
        async getCategories() {
            const token = sessionStorage.getItem('token') || localStorage.getItem('token');
            const response = await this.$http.get('/categories', {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
            this.categories = response.data
            console.log(response.data)
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


        // EDIT PRODUCT
        async editProduct() {
            if (!this.productId) {
                console.error('No product ID provided');
                return;
            }

            const formData = new FormData();
            formData.append('product_name', this.product_name);
            formData.append('product_image', this.product_image);
            formData.append('quantity', this.quantity);
            formData.append('mfg_date', this.mfg_date);
            formData.append('exp_date', this.exp_date);
            formData.append('rate_per_unit', this.rate_per_unit);

            try {
                const response = await this.$http.put(`/products?product_id=${this.productId}`, formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                    },
                });

                if (response.status === 200) {
                    window.alert('Product updated successfully!');
                    this.closeModal();
                    location.reload();
                } else {
                    console.error('Error updating product:', response);
                }
            } catch (error) {
                console.error('Error updating product:', error);
            }
        },

        // Edit modal with product details
        openEditModal(product) {
            this.productId = product.id;
            this.product_name = product.product_name;
            this.product_image = null;
            this.quantity = product.quantity;
            // this.mfg_date = product.mfg_date;
            // this.exp_date = product.exp_date;
            this.mfg_date = this.formatDate(product.mfg_date);
            this.exp_date = this.formatDate(product.exp_date);
            this.rate_per_unit = product.rate_per_unit;

            // Open the edit modal
            this.openModal();
        },

        // FORMATTING DATE
        formatDate(dateString) {
            const [day, month, year] = dateString.split('-');
            return `${year}-${month}-${day}`;
        },

        // DELETING CATEGORIES - DELETE REQUEST
        async deleteProduct(productId) {
            const token = sessionStorage.getItem('token') || localStorage.getItem('token');
            const role = sessionStorage.getItem('role') || localStorage.getItem('role');
            const headers = {
                'token': token,
                'role': role,
                'Content-Type': 'application/json',
            };

            try {
                // window.alert("Are you sure want to delete this product?")
                const confirmed = window.confirm("Are you sure you want to delete this product?");
                if (!confirmed) {
                    return;
                }

                const response = await this.$http.delete(`/products?product_id=${productId}`, { headers });

                if (response.status === 200) {
                    window.alert("Product deleted successfully!");
                    this.filterProducts();
                } else {
                    console.log(response.data);
                }
            } catch (error) {
                console.error("Error deleting product:", error);
            }
        },

        // SUBMITTING REQUEST TO DELETE A CATEGORY
        async deleteCategoryRequest(category) {
            this.setCategoryId(category.id);
            const category_name = category.category_name;
            console.log("Deleting Request:", category);
            const token = sessionStorage.getItem('token') || localStorage.getItem('token');
            const role = sessionStorage.getItem('role') || localStorage.getItem('role');

            const headers = {
                'token': token,
                'role': role,
                'Content-Type': 'application/json',
            };

            const user_id = localStorage.getItem('user_id') || sessionStorage.getItem('user_id');

            const data = {
                user_id: user_id,
                category_id: category.category_id,
                category_name: category_name,
                request_type: "Please delete this category.",
                status: "Pending"
            }
            console.log(data);

            try {
                const response = await this.$http.post('/store_admin_request', data, { headers })

                console.log('Response after submitting request:', response);

                if (response.status === 200) {
                    window.alert('Request Submitted.');
                    location.reload();
                    // this.$router.push('/')
                } else {
                    console.error('Error submitting request:', response);
                }
            } catch (error) {
                console.error('Error submitting request:', error);
                window.alert("Can't process this request, please try again after sometime")
            }
        },

        // ADD CATEGORY REQUEST
        async addCategoryRequest() {
            if (!this.newCategory) {
                window.alert('Please enter a category name.');
                return;
            }

            const token = sessionStorage.getItem('token') || localStorage.getItem('token');
            const role = sessionStorage.getItem('role') || localStorage.getItem('role');

            const headers = {
                'token': token,
                'role': role,
                'Content-Type': 'application/json',
            };

            const user_id = localStorage.getItem('user_id') || sessionStorage.getItem('user_id');

            const data = {
                user_id: user_id,
                category_name: this.newCategory,
                request_type: "Please add this category",
                status: "Pending",
            };

            try {
                const response = await this.$http.post('/store_admin_request', data, { headers });

                if (response.status === 200) {
                    window.alert('Category add request submitted successfully.');
                    this.newCategory = '';
                } else {
                    console.error('Error submitting category add request:', response);
                    throw error;
                }
            } catch (error) {
                console.error('Error submitting category add request:', error);
                window.alert("Can't process this request, please try again after some time.")
            }
        },

        // EDIT CATEGORY REQUEST

        // Edit modal with category name
        // openEditModal(category) {
        //     this.categoryId = category.id;
        //     this.category_name = category.category_name;

        //     // Open the edit modal
        //     this.openModal();
        // },

        // async editCategoryRequest() {
        //     if (!this.categoryId) {
        //         console.error('Category ID not provided');
        //         return;
        //     }

        //     const token = sessionStorage.getItem('token') || localStorage.getItem('token');
        //     const role = sessionStorage.getItem('role') || localStorage.getItem('role');

        //     const data = {
        //         category_id: this.categoryId,
        //         category_name: this.category_name,
        //         request_type: "Please change this category name",
        //         status: "Pending"
        //     };

        //     try {
        //         const response = await this.$http.post('/store_admin_request', data, {
        //             headers: {
        //                 'Content-Type': 'application/json',
        //                 'token': token,
        //                 'role': role,
        //             },
        //         });

        //         if (response.status === 200) {
        //             window.alert('Category updated successfully!');
        //             this.closeModal();
        //             location.reload();
        //         } else {
        //             console.error('Error updating Category:', response);
        //         }
        //     } catch (error) {
        //         console.error('Error updating category:', error);
        //     }
        // },
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
        this.filterProducts();
    },

};
</script>

<template>
    <div>
        <NavBar />
    </div>
    <!-- <h1>Admin View Works!</h1> -->
    <div class="category">
        <p class="section-1">Store Admin Dashboard - Stock Management</p>
        <div class="category-management">
            <div class="form-container">
                <p class="form-title">Add Category</p>
                <form @submit.prevent="addCategoryRequest">
                    <label for="name" class="category-name">Name:</label>
                    <input v-model="newCategory" type="text" id="category_name" name="category_name" required>
                    <button type="submit" class="btn">Add Category</button>
                </form>
            </div>
            <!-- ADDED CATEGORIES TABLE STARTS -->
            <div class="table-section">
                <p class="table-title">Added Categories</p>
                <p class="table-info">(Click on <strong>Add Product</strong> button to add products for a particular
                    category.)</p>
                <table>
                    <thead>
                        <tr>
                            <th>S.No</th>
                            <th>Category Name</th>
                            <th>Action</th>
                            <th> </th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(category, index) in categories" :key="index">
                            <td>{{ index + 1 }}.</td>
                            <td>{{ category.category_name }}</td>
                            <td>
                                <button @click="openEditModal(category)"  data-bs-toggle="modal" data-bs-target="#edit_category_modal">
                                    <font-awesome-icon :icon="['fas', 'pen-to-square']" class="edit-button" />
                                </button>
                                <button @click="deleteCategoryRequest(category)">
                                    <font-awesome-icon :icon="['fas', 'trash']" class="delete-button" />
                                </button>
                            </td>
                            <td>
                                <!-- <button class="btn"  @click="openModal">Add Product</button> -->
                                <button type="button" class="btn btn-sm-primary" data-bs-toggle="modal"
                                    data-bs-target="#add-product-modal" @click="setCategoryId(category.id)"
                                    data-bs-whatever="@getbootstrap">Add
                                    Product</button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <!-- ADDED CATEGORIES TABLE ENDS -->
        </div>
        <br>
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
                        <!-- <th>Category Name</th> -->
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
                            <button @click="openEditModal(product)" data-bs-toggle="modal"
                                data-bs-target="#edit-product-modal" data-bs-whatever="@getbootstrap">
                                <font-awesome-icon :icon="['fas', 'pen-to-square']" class="edit-button" />
                            </button>
                            <button @click="deleteProduct(product.id)">
                                <font-awesome-icon :icon="['fas', 'trash']" class="delete-button" />
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
    </div>

    <!-- MODAL TO ADD PRODUCT STARTS -->
    <div class="modal fade" id="add-product-modal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="exampleModalLabel">Add New Product</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form @submit.prevent="addProduct" enctype="multipart/form-data"> <!--enctype="multipart/form-data"-->
                        <div class="mb-2">
                            <label for="productName" class="col-form-label">Product Name</label>
                            <input type="text" v-model="product_name" class="form-control" id="productName" required>
                        </div>
                        <div class="mb-2">
                            <label for="productImage" class="col-form-label">Product Image</label>
                            <input type="file" @change="handleFileChange" class="form-control" accept="image/*"
                                id="productImage" required>
                        </div>
                        <!-- <div class="mb-2">
                            <label for="rate" class="col-form-label">Product Image</label>
                            <input type="text" v-model="product_image" class="form-control" id="rate" required>
                        </div> -->
                        <div class="mb-2">
                            <label for="rate" class="col-form-label">Rate per unit</label>
                            <input type="text" v-model="rate_per_unit" class="form-control" id="rate" required>
                        </div>
                        <div class="mb-2">
                            <label for="quantity" class="col-form-label">Quantity</label>
                            <input type="number" v-model="quantity" class="form-control" id="quantity" required>
                        </div>
                        <div class="mb-2">
                            <label for="productName" class="col-form-label">Manufacture Date</label>
                            <input type="date" v-model="mfg_date" class="form-control" id="mfgDate" required>
                        </div>
                        <div class="mb-2">
                            <label for="expiryDate" class="col-form-label">Expiry Date</label>
                            <input type="date" v-model="exp_date" class="form-control" id="expiryDate" required>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                            <button type="submit" class="btn btn-primary">Add Product</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
    <!-- MODAL TO ADD PRODUCT ENDS -->

    <!-- MODAL TO EDIT PRODUCT STARTS -->
    <div class="modal fade" id="edit-product-modal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="exampleModalLabel">Edit Product</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form @submit.prevent="editProduct" enctype="multipart/form-data">
                        <div class="mb-2">
                            <label for="productName" class="col-form-label">Product Name</label>
                            <input type="text" v-model="product_name" class="form-control" id="productName" required>
                        </div>
                        <div class="mb-2">
                            <label for="productImage" class="col-form-label">Product Image</label>
                            <input type="file" @change="handleFileChange" class="form-control" accept="image/*"
                                id="productImage" required>
                        </div>
                        <!-- <div class="mb-2">
                            <label for="rate" class="col-form-label">Product Image</label>
                            <input type="text" v-model="product_image" class="form-control" id="rate" required>
                        </div> -->
                        <div class="mb-2">
                            <label for="rate" class="col-form-label">Rate per unit</label>
                            <input type="text" v-model="rate_per_unit" class="form-control" id="rate" required>
                        </div>
                        <div class="mb-2">
                            <label for="quantity" class="col-form-label">Quantity</label>
                            <input type="number" v-model="quantity" class="form-control" id="quantity" required>
                        </div>
                        <div class="mb-2">
                            <label for="productName" class="col-form-label">Manufacture Date</label>
                            <input type="date" v-model="mfg_date" class="form-control" id="mfgDate" required>
                        </div>
                        <div class="mb-2">
                            <label for="expiryDate" class="col-form-label">Expiry Date</label>
                            <input type="date" v-model="exp_date" class="form-control" id="expiryDate" required>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                            <button type="submit" class="btn btn-primary">Update Product</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
    <!-- MODAL TO EDIT PRODUCT ENDS -->

    <!-- Edit Category Modal -->
    <div class="modal fade" id="edit_category_modal" tabindex="-1" aria-labelledby="edit_category_modal" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Edit Category</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <form @submit.prevent="editCategoryRequest">
                    <div class="modal-body">
                        <label for="category_name" class="category-name">Name:</label>
                        <input type="text" v-model="category_name" id="category_name" name="category_name" required>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button type="submit" class="btn btn-primary">Send Request</button>
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
}

.category-management {
    display: flex;
}

@media screen and (max-width:768px) {
    .category-management {
        display: flex;
    }
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
    padding: 8px 16px;
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
    margin-bottom: 40px;
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
    word-break: break-word;
    margin: 3px;
}


table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
}

thead th {
    background-color: #a0f2da;
    color: #3c3b3b;
    font-weight: bold;
    padding: 15px 30px;
    text-align: center;
}

td {
    padding: 5px;
    text-align: center;
    /* width: 100%; */
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
.approve-button {
    transform: scale(1.5);
}

.filter-products {
    display: flex;
    position: center;
    justify-content: center;
}

.product-image {
    width: 30px;
}

.category-dropdown-label {
    padding-right: 4px;
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