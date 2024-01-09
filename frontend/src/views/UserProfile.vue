<script>
import NavBar from '../components/NavBar.vue';

export default {
  components: {
    NavBar,
  },

  data() {
    return {
      user: "",
      sendingRequest: false,
      orderHistory: [],
      user_id: null,
    };
  },
  methods: {
    async getUser() {
      try {
        const username = sessionStorage.getItem('username') || localStorage.getItem('username');
        const token = sessionStorage.getItem('token') || localStorage.getItem('token');
        const role = sessionStorage.getItem('role') || localStorage.getItem('role');
        const headers = {
          'token': token,
          'role': role,
          'Content-Type': 'application/json'
        };
        const response = await this.$http.get(`/users?username=${username}`, { headers });
        this.user = response.data;
        console.log(this.user)
      } catch (error) {
        console.error("Error getting user details", error)
      }
    },

    //POSTING REQUEST TO BE STORE ADMIN
    async storeAdminRequest() {
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
        request_type: "Requesting to be store admin",
        status: "Pending"
      }

      try {
        this.sendingRequest = true;
        const response = await this.$http.post('/store_admin_request', data, { headers })

        if (response.status === 200) {
          window.alert('Request Submitted.');
          // location.reload();
          this.$router.push('/')
        } else {
          console.error('Error submitting request:', response);
        }
      } catch (error) {
        console.error('Error submitting request:', error);
        window.alert("Can't process this request, please try again after sometime")
      } finally {
        this.sendingRequest = false;
      }
    },

    // GETTING ORDER HISTORY
    async getOrderHistory() {
      try {
        const token = sessionStorage.getItem('token') || localStorage.getItem('token');
        const role = sessionStorage.getItem('role') || localStorage.getItem('role');

        const headers = {
          'token': token,
          'role': role,
          'Content-Type': 'application/json'
        };

        const user_id = sessionStorage.getItem('user_id') || localStorage.getItem('user_id');

        const response = await this.$http.get(`/orders?user_id=${user_id}`, { headers });
        this.orderHistory = response.data;
        console.log(this.orderHistory)
      } catch (error) {
        console.error("Error getting user details", error)
      }
    },

  },
  mounted() {
    this.getUser();
    this.getOrderHistory();
  }
}
</script>

<template>
  <div>
    <NavBar />
    <div class="user-profile-container">
      <div class="user-details">
        <p class="welcome-message">Welcome, {{ user.full_name }}!</p>
        <div class="user-info">
          <strong>Username:</strong> {{ user.username }}
        </div>
        <div class="user-info">
          <strong>Email:</strong> {{ user.email }}
        </div>
        <div class="user-info">
          <strong>Mobile:</strong> {{ user.mobile }}
        </div>
        <div class="user-info">
          <strong>Role:</strong> {{ user.role }}
        </div>
      </div>
      <div class="store-admin-request">
        <button class="btn btn-outline-primary" @click="storeAdminRequest"
          :disabled="sendingRequest">
          {{ sendingRequest ? 'Sending request...' : 'Request to be Store Admin' }}
        </button>
      </div>
    </div>
  </div>

  <!-- ORDER HISTORY -->
  <div class="table-section">
    <p class="table-title">Order History</p>
    <table>
      <thead>
        <tr>
          <th>Order ID</th>
          <th>Product Name</th>
          <th>Quantity</th>
          <th>Order Date & Time</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(order, index) in orderHistory" :key="index">
          <td>{{ order.id }}.</td>
          <td>{{ order.product_name }}</td>
          <td>{{ order.quantity }}</td>
          <td>{{ order.order_date }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.btn {
  background-color: #007bff;
  color: #fff;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 10px;
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

@media (max-width: 768px) {
  .category-management {
    flex-direction: column;
  }

  .table-section {
    overflow-x: auto;
    margin-bottom: 20px;
  }
}

.user-profile-container {
  max-width: 600px;
  margin: 20px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 10px;
  background-color: #f8f8f8;
  display: flex;
  justify-content: space-between;
}

.user-details {
  flex: 1;
}

.welcome-message {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 10px;
}

.user-info {
  margin-bottom: 15px;
}

.store-admin-request button {
  padding: 10px 20px;
  font-size: 16px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease-in-out;
}

.store-admin-request button:disabled {
  cursor: not-allowed;
}

.store-admin-request button:hover {
  background-color: #4caf50;
  /* Green */
  color: white;
}
</style>
