import { createRouter, createWebHistory } from 'vue-router';
import store from '../store';
import HomeView from '../views/HomeView.vue';
import Login from '../views/LoginView.vue';
import Register from '../views/RegisterView.vue';
import Restore from '../views/RestoreView.vue';

const routes = [
  {
    path: '/',
    meta: { requiresAuth: true, title: 'Главная' },
    component: HomeView,
  },
  { path: '/auth', component: Login },
  { path: '/register', component: Register },
  { path: '/restore', component: Restore },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach((to, _, next) => {
  if (to.meta.requiresAuth && !store.getters.isAuth) {
    next('/auth');
  } else {
    next();
  }
});

export default router;
