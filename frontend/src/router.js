import { createMemoryHistory, createRouter, createWebHashHistory } from 'vue-router'

import IndexPage from './components/IndexPage.vue'
import LoginPage from './components/LoginPage.vue'
import SignupPage from './components/SignupPage.vue'
import UserDashboardPage from './components/UserDashboardPage.vue'
import AdminDashboardPage from './components/AdminDashboardPage.vue'
import AdminSubjectPage from './components/AdminSubjectPage.vue'
import AdminNewChapterPage from './components/AdminNewChapterPage.vue'
import axiosClient from './axiosClient'
import { useUserStore } from './stores/user'
import UserSubjectPage from './components/UserSubjectPage.vue'
import UserQuizPage from './components/UserQuizPage.vue'
import AdminQuizScoresPage from './components/AdminQuizScoresPage.vue'
import UserScorePage from './components/UserScorePage.vue'
import AdminQuizQuestionsPage from './components/AdminQuizQuestionsPage.vue'


const isUnauthenticated = async (to, from) => {
  const store = useUserStore()
  if (store.role != "" && store.role != undefined) {
    return { path: `/${store.role}/dashboard`, replace: true }
  }
  try {
    const response = await axiosClient.get("/auth/me")
    const user = response.data.user
    store.$patch({
        id: user.id,
        email: user.email,
        name: user.full_name,
        role: user.role
    })
    return { path: `/${user.role}/dashboard`, replace: true }
  }
  catch(error) {
    return true
  }
}

const isAdminAuthenticated = async (to, from) => {
  const store = useUserStore()
  if (store.role == "admin") {
    return true
  } else if (store.role == "user") {
    return false
  } else {
    try {
      const response = await axiosClient.get("/auth/me")
      const user = response.data.user
      store.$patch({
          id: user.id,
          email: user.email,
          name: user.full_name,
          role: user.role
      })
      return user.role == "admin"
    }
    catch(error) {
      return { path: "/login", replace: true }
    }
  }
}

const isUserAuthenticated = async (to, from) => {
  const store = useUserStore()
  if (store.role == "user") {
    return true
  } else if (store.role == "admin") {
    return false
  } else {
    try {
      const response = await axiosClient.get("/auth/me")
      const user = response.data.user
      store.$patch({
          id: user.id,
          email: user.email,
          name: user.full_name,
          role: user.role
      })
      return user.role == "user"
    }
    catch(error) {
      return { path: "/login", replace: true }
    }
  }
}

const isQuizAvailable = async(to, from) => {
  try {
    const resp = await axiosClient.get(`/user/quiz/${to.params.quizId}/check`)
  } catch(error) {
    return false
  }
  return true
}

const routes = [
  { 
    path: '/', 
    component: IndexPage,
    beforeEnter: isUnauthenticated
  },
  { 
    path: '/login', 
    component: LoginPage,
    beforeEnter: isUnauthenticated
  },
  { 
    path: '/register',
    component: SignupPage,
    beforeEnter: isUnauthenticated
  },
  { 
    path: '/user/dashboard', 
    component: UserDashboardPage, 
    beforeEnter: isUserAuthenticated
  },
  { 
    path: '/user/scores', 
    component: UserScorePage, 
    beforeEnter: isUserAuthenticated
  },
  { 
    path: '/user/subject/:subjectId', 
    component: UserSubjectPage, 
    beforeEnter: isUserAuthenticated
  },
  {
    path: '/user/quiz/:quizId',
    component: UserQuizPage,
    beforeEnter: [isUserAuthenticated, isQuizAvailable]
  },
  { 
    path: '/admin/dashboard',
    component: AdminDashboardPage,
    beforeEnter: isAdminAuthenticated
  },
  { 
    path: '/admin/subject/:subjectId', 
    component: AdminSubjectPage, 
    beforeEnter: isAdminAuthenticated
  },
  { 
    path: '/admin/subject/:subjectId/chapter/new',
    component: AdminNewChapterPage, 
    beforeEnter: isAdminAuthenticated 
  },
  {
    path: '/admin/quiz/:quizId/scores',
    component: AdminQuizScoresPage,
    beforeEnter: isAdminAuthenticated
  },
  {
    path: '/admin/quiz/:quizId/questions',
    component: AdminQuizQuestionsPage,
    beforeEnter: isAdminAuthenticated
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

export default router