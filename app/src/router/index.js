import { createRouter, createWebHistory } from 'vue-router';
import store from '../store';
import HomeView from '../views/HomeView.vue';

const routes = [
  {
    path: '/',
    meta: { requiresAuth: true, title: 'Главная' },
    component: HomeView,
  },
  { path: '/auth', component: Login },
  { path: '/register', component: Register },
  { path: '/restore' , component: Restore },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !store.getters.isAuth) {
    next('/login');
  } else {
    next();
  }
});

export default router;
