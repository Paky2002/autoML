import { createRouter, createWebHistory } from 'vue-router';
import TrainModel from '../views/TrainModel.vue';
import ViewModel from '../views/ViewModel.vue';
import ModelDetail from '../views/ModelDetail.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/train'
    },
    {
      path: '/train',
      name: 'TrainModel',
      component: TrainModel,
      meta: {
        title: 'Train Model'
      }
    },
    {
      path: '/models',
      name: 'ViewModel',
      component: ViewModel,
      meta: {
        title: 'View Models'
      }
    },
    {
      path: '/models/:uuid',
      name: 'ModelDetail',
      component: ModelDetail,
      meta: {
        title: 'Model Details'
      }
    }
  ]
});

router.beforeEach((to) => {
  document.title = `AutoML - ${to.meta.title || 'Dashboard'}`;
});

export default router;