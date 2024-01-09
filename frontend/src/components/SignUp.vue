<template>
  <main>
    <div class="signup-form">
      <h2>Create an Account</h2>
      <form @submit.prevent="signup">
        <div class="form-group">
          <label for="username">Username</label>
          <input type="text" v-model="username" id="username" required>
        </div>
        <div class="form-group">
          <label for="full_name">Full Name</label>
          <input type="text" v-model="full_name" id="full_name" required>
        </div>
        <div class="form-group">
          <label for="mobile">Mobile</label>
          <input type="tel" v-model="mobile" id="mobile" required>
        </div>
        <div class="form-group">
          <label for="email">Email</label>
          <input type="email" v-model="email" id="email" required>
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <input type="password" v-model="password" id="password" required>
        </div>
        <button type="submit">Sign Up</button>
      </form>
      Already have an account ? <router-link to="/login">Login</router-link>
      <div v-if="signupStatus" class="alert" :class="signupStatus === 'success' ? 'alert-success' : 'alert-danger'">
        {{ signupStatus === 'success' ? 'Signup successful' : 'Signup failed' }}
      </div>
    </div>
  </main>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      full_name: '',
      mobile: '',
      email: '',
      password: '',
      signupStatus: ''
    }
  },
  
  methods: {
    async signup() {
      console.log(this.$data);
      const response = await this.$http.post('/signup', {
        full_name: this.full_name,
        email: this.email,
        username: this.username,
        mobile: this.mobile,
        password: this.password
      });

      // SIGNUP STATUS BASED ON BACKEND RESPONSE
      if (response.status === 200) {
        this.signupStatus= 'success';
        window.alert("Signup successful")
        this.$router.push('/login')
      } else {
        console.log(response.data)
        this.signupStatus = 'error';
      }
    }
  },
}
</script>

<style scoped>
/* main{
  background-image: url('../assets/img/demo-product.png');
  position: center;
} */
.signup-form {
  max-width: 400px;
  margin: auto;
  padding: 20px;
  border: 1px solid #ccc;
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
</style>
