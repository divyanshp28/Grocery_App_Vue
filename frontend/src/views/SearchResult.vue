<template>
    <NavBar />
          <!-- SEARCH -->
          <div class="search-container">
        <form @submit.prevent="searchProducts">
          <div class="search">
            <input v-model="searchQuery" type="text" class="search-box" placeholder="Search for products .....">
            <button @click="showProductDetails" class="btn btn-primary">Search</button>
          </div>
        </form>
      </div>
    <div>
        <h2>Search Results</h2>
        <div v-if="searchResults.length === 0">No results found.</div>
        <ul v-else>
            <li v-for="result in searchResults" :key="result.id">
                <!-- <router-link v-for="result in searchResults" :key="result.id" :to="{ name: 'single_product', query: { productId: result.id } }">{{ result.product_name }} - {{ result.id }}</router-link> -->
                <router-link v-for="result in searchResults" :key="result.id" v-if="result.id" :to="{ name: 'single_product', query: { product_id: result.id } }">{{ result.product_name }}</router-link>
            </li>
        </ul>
    </div>
</template>
  
<script>
import NavBar from '../components/NavBar.vue';
export default {
    // props: {
    //     searchResults: {
    //         type: Array,
    //         default: () => [],
    //     },
    // },

    data() {
        return {
            searchResults: [],
            searchQuery: '',
        };
    },

    components: {
        NavBar,
    },

    methods: {
        async searchProducts() {
            try {
                const response = await this.$http.get('/products', {
                    params: { query: this.searchQuery },
                });

                this.searchResults = response.data;

            } catch (error) {
                console.error('Error searching products:', error);
            }
        },
    },
};
</script>

<style scoped>

.search-container {
  flex: 1;
  margin: 0 20px;
}

.search {
  display: flex;
}


.search-box {
  display: flex;
  align-items: center;
  width: 100%;
  padding: 8px;
  border: none;
  border-radius: 5px;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);
  /* color: #d1cfcf; */
  color:#3e5172;
  border: none;
  outline: none;
  margin-right: 4px;
}

</style>
  