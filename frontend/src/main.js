import { createApp } from 'vue'
import { initAuth } from './auth.js'
// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

import '@mdi/font/css/materialdesignicons.css'


// Components
import App from './App.vue'
import { createPinia } from 'pinia'

initAuth()

const pinia = createPinia()
import router from './router'
const vuetify = createVuetify({
  theme: {
    defaultTheme: 'dark',
  },
  components,
  directives,
})

createApp(App).use(pinia).use(router).use(vuetify).mount('#app')
