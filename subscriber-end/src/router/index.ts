import {createRouter, RouteRecordRaw, Router, createWebHistory} from 'vue-router'

const routes: Array<RouteRecordRaw> = [
    {
        path: '/',
        redirect: '/home'
    },
    {
        path: '/:pathMatch(.*)*',
        redirect: '/home'
    },
    {
        path: '/home',
        // @ts-ignore
        component: () => import('../pages/Home.vue'),
        meta: {title: '首页'}
    },
    {
        path: '/sub',
        // @ts-ignore
        component: () => import('../pages/SubscriptionEnd.vue'),
        meta: {title: '订阅端'}
    },
    {
        path: '/pub',
        // @ts-ignore
        component: () => import('../pages/PublishingEnd.vue'),
        meta: {title: '发布端'}
    }
]

const router: Router = createRouter({
    history: createWebHistory(),
    routes
})

router.beforeEach((to, _, next) => {
    document.title = to.meta.title as string
    next()
})

export default router
