import { createRouter, createWebHistory } from 'vue-router'
import Home          from '../views/Home.vue'
import Predictor     from '../views/Predictor.vue'
import Insights      from '../views/Insights.vue'
import Database      from '../views/Database.vue'
import About         from '../views/About.vue'
import Interventions from '../views/Interventions.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/',              name: 'Home',          component: Home },
    { path: '/predict',       name: 'Predictor',     component: Predictor },
    { path: '/insights',      name: 'Insights',      component: Insights },
    { path: '/database',      name: 'Database',      component: Database },
    { path: '/about',         name: 'About',         component: About },
    { path: '/interventions', name: 'Interventions', component: Interventions },
  ],
  scrollBehavior: () => ({ top: 0 }),
})

export default router
