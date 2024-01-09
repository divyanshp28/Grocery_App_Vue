import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'

// BOOTSTRAP
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap'

// FONT AWESOME
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { library } from '@fortawesome/fontawesome-svg-core'
import { fas } from '@fortawesome/free-solid-svg-icons'

library.add(fas)


const app = createApp(App)
// FONT AWESOME
app.component('font-awesome-icon', FontAwesomeIcon)

app.use(router)


// Setting API URL 
const api = axios.create({
  baseURL: "http://localhost:5000",
});

// RESPONSE INTERCEPTOR - CHECKING IF TOKEN IS VALID
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response && error.response.status === 401) {
      window.alert("Please login to continue")
      router.push('/login');
    }

    return Promise.reject(error);
  }
);


//GLOBAL AXIOS INSTANCE
app.config.globalProperties.$http = api;


app.mount('#app')
