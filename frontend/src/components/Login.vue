<template>
    <div class="login-form">
      <h2>Login</h2>
      <form @submit.prevent="login">
        <div class="form-group">
          <label for="username">Username</label>
          <input type="text" v-model="username" id="username" required>
        </div>
  
        <div class="form-group">
          <label for="password">Password</label>
          <input type="password" v-model="password" id="password" required>
        </div>
  
        <button type="submit" :disabled="loading">
          {{ loading ? 'Logging in...' : 'Login' }}
        </button>
      </form>
      Don't have an account ? <router-link to="/signup">Sign up</router-link>
    </div>
  </template>

<script>
export default {
    data() {
        return {
            username: '',
            password: '',
            loading: false,
            errorMessage: ''
        };
    },
    methods: {
        async login() {
            try {
                const response = await this.$http.post('/login', {
                    username: this.username,
                    password: this.password
                });
                this.loading = true;
                await new Promise(resolve => setTimeout(resolve, 1500));

                if (response.status === 200) {
                    const user_id = response.data.user_id;
                    sessionStorage.setItem('user_id', user_id);
                    localStorage.setItem('user_id', user_id);

                    const username = response.data.username;
                    sessionStorage.setItem('username', username);
                    localStorage.setItem('username', username);

                    const role = response.data.role;
                    sessionStorage.setItem('role', role);
                    localStorage.setItem('role', role);

                    const token = response.data.token;
                    sessionStorage.setItem('token', token);
                    localStorage.setItem('token', token);

                    if (response.data.role === "admin") {
                        this.$router.push({ path: '/admin', query: { username: this.username } });
                    } else if (response.data.role === "store_admin") {
                        this.$router.push({ path: '/storeadmin', query: { username: this.username } });
                    } else {
                        console.log('Login successful!');
                        this.$router.push({ path: '/', query: { username: this.username } });
                    }
                    console.log('Login Response:', response);
                }
            } catch (error) {
                console.error('Login failed:', error.message);
                this.errorMessage = 'Login failed. Please check your credentials.';
            } finally {
                this.loading = false;
            }
        }
    }
};
</script>

  
  <!-- <script>
  export default {
    data() {
      return {
        username: '',
        password: '',
        loading: false,
        errorMessage: ''
      };
    },
    methods: {
      async login() {
        try {
          const response = await this.$http.post('/login', {
            username: this.username,
            password: this.password
          });
          this.loading = true;

          if (response.status === 200) {
            // User ID
            const userId = parseInt(response.data.user_id, 10);
            sessionStorage.setItem('user_id', userId);
            localStorage.setItem('user_id', userId);

            // Username
            const username = response.data.username;
            sessionStorage.setItem('username', username);
            localStorage.setItem('username', username);

            // Role
            const role = response.data.role;
            sessionStorage.setItem('role', role);
            localStorage.setItem('role', role);

            // Token
            const token = response.data.token;
            sessionStorage.setItem('token', token);
            localStorage.setItem('token', token);


            if (response.data.role === "admin") {
                this.$router.push({path:'/admin', params: { userId }})
                //Loading
                await new Promise(resolve => setTimeout(resolve, 1500));
            }
            else if (response.data.role === "storeadmin") {
              this.$router.push({path:'/storeadmin', params: { userId }})
              //Loading
              await new Promise(resolve => setTimeout(resolve, 1500));
            }
            else{
                // Login successful -> Redirect to home
                console.log('Login successful!');
                this.$router.push({path:'/', params: { userId }});
                //Loading
                await new Promise(resolve => setTimeout(resolve, 1500));
            }
            console.log('Login Response:', response);
          }
  
  
        } catch (error) {
          console.error('Login failed:', error.message);
          this.errorMessage = 'Login failed. Please check your credentials.';
        } finally {
          this.loading = false;
        }
      }
    }
  };
  </script> -->
  
  <style scoped>
  .login-form {
    max-width: 400px;
    margin: auto;
    padding: 20px;
    border: 2px solid #ccc;
    border-radius: 8px;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  label {
    display: block;
    margin-bottom: 5px;
  }
  
  input {
    width: 100%;
    padding: 8px;
    box-sizing: border-box;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 14px;
  }
  
  button {
    background-color: #4caf50;
    color: #fff;
    padding: 10px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
  }
  
  button:hover {
    background-color: #45a049;
  }
  
  @media (max-width: 600px) {
    .login-form {
      max-width: 100%;
    }
  }
  </style>
  