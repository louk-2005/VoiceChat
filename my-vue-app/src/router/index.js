import { createRouter, createWebHistory } from "vue-router"

const Home = () => import("../pages/home/home.vue")


const routes = [
    { path: "/", name: "Home", component: Home },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
    scrollBehavior(to, from, savedPosition) {
        // اگر برگشت به عقب یا جلو (history) باشه
        if (savedPosition) {
            return savedPosition
        }
        // در حالت عادی برو بالای صفحه
        return { top: 0 }
    }
})

export default router
