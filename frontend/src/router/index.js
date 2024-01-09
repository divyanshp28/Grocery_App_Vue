import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SignUp from '../components/SignUp.vue'
import CategoryPage from '../views/CategoryPage.vue'
import Admin from '../views/Admin.vue'
import CartPage from '../views/CartPage.vue'
import StoreAdmin from '../views/StoreAdmin.vue'
import AdminLogin from '../components/AdminLogin.vue'

// Route protection
import { isAdmin, isLoggedIn, isStoreAdmin } from './routeAuth'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignUp
    },
    {
      path: '/login',
      name: '/login',
      component: () => import('../components/Login.vue')
    },
    // {
    //   path: '/about',
    //   name: 'about',
    //   // route level code-splitting
    //   // this generates a separate chunk (About.[hash].js) for this route
    //   // which is lazy-loaded when the route is visited.
    //   component: () => import('../views/AboutView.vue')
    // },
    {
      path: '/admin',
      name: 'admin',
      component: Admin,
      beforeEnter: isAdmin
    },
    //ADMIN LOGIN COMPONENT
    // {
    //   path: "/admin_login",
    //   name: 'admin_login',
    //   component: AdminLogin,
    // },
    {
      path: '/storeadmin',
      name: 'store_admin',
      component: StoreAdmin,
      beforeEnter: isStoreAdmin,
    },
    {
      path: "/category",
      name: "Category",
      component: CategoryPage,
    },
    {
      path: '/user_cart',
      name: 'cart',
      component: CartPage,
      beforeEnter: isLoggedIn,
    },
    {
      path: '/user_profile',
      name: 'user_profile',
      component: () => import('../views/UserProfile.vue'),
      beforeEnter: isLoggedIn,
    },
    {
      // path: '/single_product/:productId',
      path: '/single_product',
      name:"single_product",
      component: () => import('../views/SingleProduct.vue')
    },
    {
      path: '/search_results',
      name: 'search_results',
      component: () => import('../views/SearchResult.vue')
    },
  ]
})

export default router
