import Vue from 'vue'
import VueRouter from 'vue-router'
//import HomeView from '../views/HomeView.vue'
import Kanban_Dashboard from '../components/Dashboard.vue'
import Login_kanban from '../components/Login.vue'
Vue.use(VueRouter)


fetch("http://localhost:5000/api/test", {
  headers: {
    'Content-Type' : 'application/json',
    'Authentication-Token': localStorage.getItem('access_token')
  }
}).then(response => {
  if (!response.ok) {
    localStorage.clear()
  }
})



const routes = [
  {
    path: '/',
    name: 'home',
    component: Kanban_Dashboard
  },
  {
    path: '/about',
    name: 'about',
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: Kanban_Dashboard
  },
  {
    path: '/login',
    name: 'login',
    component: Login_kanban
  },
  {
    path: '/logout',
    name: 'logout',
    component: () => {
      localStorage.clear()
      router.push({name:'login'})
    }
    
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})


export default router
