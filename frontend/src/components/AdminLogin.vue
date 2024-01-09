<!-- AdminLogin.vue -->
<script>
export default {
  data() {
    return {
      username: '',
      password: '',
      loading: false,
      errorMessage: '',
    };
  },
  methods: {
    async login() {
        this.loading = true;
      try {
        const response = await this.$http.post('/admin_login', {
          username: this.username,
          password: this.password,
        });

        const token = response.data?.token;

        if (token) {
          localStorage.setItem('token', token);
          this.$router.push({ name: 'admin' });
        } else {
          console.error('Token not found in the response:', response);
        }
      } catch (error) {
        console.error('Login failed:', error.response.data.message);
        this.errorMessage = 'Login failed. Please check your credentials.';
      } finally {
        this.loading = false;
      }
    },
    showErrorMessage() {
      setTimeout(() => {
        this.errorMessage = '';
      }, 1000);
    },
  },
};
</script>


<template>
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    <div class="login-container">
      <h2>Admin Login</h2>
      <form @submit.prevent="login" class="login-form">
        <label for="username">Username:</label>
        <input type="text" v-model="username" required />
  
        <label for="password">Password:</label>
        <input type="password" v-model="password" required />
  
        <!-- <button type="submit">Login</button> -->
        <button type="submit" :disabled="loading">
        {{ loading ? 'Logging in...' : 'Login' }}
      </button>
      </form>
    </div>
  </template>



 
  <style scoped>

  .login-container {
    max-width: 400px;
    margin: 0 auto;
    padding: 20px;
    background-color: #f5f5f5;
    border-radius: 5px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  }
  
  .login-form {
    display: grid;
    gap: 10px;
  }
  
  label {
    font-weight: bold;
  }
  
  input {
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 3px;
    width: 100%;
  }
  
  button {
    padding: 10px;
    background-color: #4caf50;
    color: #fff;
    border: none;
    border-radius: 3px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #45a049;
  }

  .error-message {
    color: white;
    background-color: red;
    padding: 10px;
    border-radius: 5px;
    text-align: center;
    position: fixed;
    top: 10px;
    left: 10px;
    z-index: 999;
  }

  @media (min-width: 600px) {
    .error-message {
      width: auto;
      max-width: 300px; 
    }
  }
  </style>
  