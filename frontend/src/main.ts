import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import { DialogsService } from '@/services/dialogs.ts'
import { IntlService } from '@/services/intl'

const app = createApp(App)

app.use(createPinia())
app.use(DialogsService.initPlugin())
app.use(IntlService.initPlugin())
app.use(router)

app.mount('#app')
