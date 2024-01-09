<template>
  <header>
    <nav>
      <router-link to="/" class="logo">Grocery Store</router-link>
      <ul class="nav-links">
        <!-- SEARCH ICON -->
        <li><router-link to="/search_results"><font-awesome-icon :icon="['fas', 'search']"
              class="icon-large"></font-awesome-icon></router-link></li>
        <!-- LOCATION -->
        <li><a href="#"><font-awesome-icon :icon="['fas', 'map-marker-alt']" class="icon-large" />Patna, Bihar</a></li>
        <!-- CART ICON -->
        <li>
          <router-link to="/user_cart">
            <font-awesome-icon :icon="['fas', 'shopping-cart']" class="icon-large" />
          </router-link>
        </li>
        <!-- USER PROFILE DROPDOWN -->
        <li>
          <div class="user_dropdown">
            <font-awesome-icon :icon="['fas', 'user']" class="icon-large" />
            <div class="user_dropdown_content">
              <router-link v-if="authenticated" class="user_actions" to="/user_profile">User Profile</router-link>
              <router-link v-if="!authenticated" class="user_actions" to="/login">Login</router-link>
              <router-link v-if="authenticated" class="user_actions" to="/" @click="confirmLogout">Logout</router-link>
            </div>
          </div>
        </li>
      </ul>
      <div class="menuBar">
        <font-awesome-icon :icon="['fas', 'bars']" />
      </div>
    </nav>
    <!-- SUBHEADER -->
    <div class="subheader">
      <select class="form-select form-select-lg mb-3 dropdown" aria-label=".form-select-lg example"
        v-model="selectedCategory" @change="goToCategoryPage">
        <option selected hidden>Shop by Category</option>
        <option v-for="category in categories" :key="category.id" :value="category.id">{{ category.category_name }}
        </option>
      </select>
    </div>
    <!-- SUBHEADER ENDS -->
  </header>
</template>

<script>
export default {
  mounted() {
    const menuBar = document.querySelector('.menuBar');
    const ul = document.querySelector('ul');

    menuBar.addEventListener('click', () => {
      ul.classList.toggle('menu-active');
    });
  },
  data() {
    return {
      dropdownOpen: false,
      //GETTING CATEGORIES FOR DROPDOWN
      categories: [],
      authenticated: false,
      selectedCategory: "Shop by Category",
      searchQuery: '',
      products: [],
    };
  },
  methods: {
    toggleDropdown() {
      this.dropdownOpen = !this.dropdownOpen;
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
      // console.log(response.data)
    },

    // Checking if user is logged in
    isAuthenticated() {
      const token = sessionStorage.getItem('token') || localStorage.getItem('token');
      return !!token;
    },

    // LOGOUT CONFIRMATION
    confirmLogout() {
      if (this.isAuthenticated() && window.confirm('Are you sure you want to log out?')) {
        this.logout();
      }
    },

    // LOGOUT
    logout() {
      // Clearing session and local storage
      sessionStorage.removeItem('username');
      sessionStorage.removeItem('token');
      sessionStorage.removeItem('role')
      localStorage.removeItem('username');
      localStorage.removeItem('token');
      localStorage.removeItem('role');
      this.authenticated = false;
      this.$router.push('/');
    },

    // SETTING CATEGORY ID
    setCategoryId(id) {
      this.category_id = id;
      console,log(this.category_id)
    },
    // NAVIGATING TO CATEGORY PAGE
    goToCategoryPage() {
      if (this.selectedCategory) {
        this.$router.push({ name: 'Category', query: { category_id: this.selectedCategory } });
      }
    },

  },
  mounted() {
    this.getCategories();
    this.authenticated = this.isAuthenticated();
  },

};

</script>

<style scoped>
template {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

header {
  width: 100%;
  top: 0;
  left: 0;
  position: absolute;
}

.icon-large {
  font-size: 30px;
  color: #f9e9de;
}

/* WHOLE NAVBAR */
header nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 20px;
  /* background-color: rgb(22, 167, 111); */
  background-color: #3e5172;
}

/* COLOUR OF NAVBAR ITEMS */
.nav-links a {
  /* color: black; */
  color: #f9e9de;
}

/* SEARCH BOX */

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
  color: #3e5172;
  border: none;
  outline: none;
  margin-right: 4px;
}


.logo {
  /* color: black; */
  color: #f9e9de;
  font-size: 30px;
  font-weight: bold;
  font-family: "Brush Script MT", cursive;
}

ul {
  display: flex;
  justify-content: space-between;
  flex-basis: 20%;
}

ul li {
  list-style: none;
}

ul li a {
  font-weight: 600;
  text-decoration: none;
}

ul li a:hover {
  text-decoration: underline 2px;
  text-underline-offset: 4px;
}

.menuBar {
  font-size: 30px;
  display: none;
}

@media screen and (max-width:1024px) {
  .menuBar {
    display: flex;
    cursor: pointer;
  }

  ul {
    display: none;
  }

  ul.menu-active {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    position: absolute;
    top: 60px;
    left: 0;
    width: 100%;
    gap: 24px;
    background-color: cadetblue;
  }
}


/* STYLING SUBHEADER */

.subheader {
  display: flex;
  width: 100%;
  margin: 3px 0;
  margin-left: 5px;
  cursor: pointer;
  width: 230px;
}

.dropdown {
  background-color: #69b0d1;
  font-weight: bold;
}

.dropdown:hover {
  background-color: #69b0d1;
  cursor: pointer;
}

/* USER ICON DROPDOWN */
.user_dropdown {
  position: relative;
  display: inline-block;
}

.user_dropdown_content {
  display: none;
  position: absolute;
  background-color: #f1f1f1;
  min-width: 160px;
  box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
  z-index: 1;
}

.user_dropdown_content .user_actions {
  color: black;
  padding: 12px 16px;
  text-decoration: none;
  display: block;
}

.user_dropdown_content .user_actions:hover {
  background-color: #ddd;
}

.user_dropdown:hover .user_dropdown_content {
  display: block;
}

.user_dropdown:hover .user_dropdown_content {
  display: block;
  left: auto;
  right: 0;
}

.user_dropdown:hover {
  background-color: #69b0d1;
}
</style>