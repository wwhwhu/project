import Vue from 'vue'
import Router from 'vue-router'
import myLogin from '@/views/myLogin.vue'
import carPage from "@/views/carPage.vue";
import pageChoice from "@/views/pageChoice.vue";
import uploadVisual from "@/views/uploadVisual.vue"

Vue.use(Router)

export default new Router({
    routes: [
        {
            path: '/',
            name: 'myLogin',
            component: myLogin
        },
        {
            path: '/carPage',
            name: 'carPage',
            component: carPage
        },
        {
            path: '/login',
            name: 'Login',
            component: myLogin
        },
        {
            path: '/pageChoice',
            name: 'pageChoice',
            component: pageChoice
        },
        {
            path: '/uploadVisual',
            name: 'uploadVisual',
            component: uploadVisual
        }

    ]
})
