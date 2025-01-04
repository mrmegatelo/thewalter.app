import './assets/main.css'

import { createApp } from 'vue'
import type { Plugin, App as AppType } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

const app = createApp(App)

function createDialogs(): Plugin {
  class DialogsController {
    private dialogs = new Map<string, HTMLDialogElement>()

    public addDialog(name: string, el: HTMLDialogElement): void {
      this.dialogs.set(name, el)
    }

    public removeDialog(name: string): void {
      this.dialogs.delete(name)
    }

    public showDialog(name: string): void {
      this.dialogs.get(name)?.showModal()
    }

    public hideDialog(name: string): void {
      this.dialogs.get(name)?.close()
    }
  }

  return {
    install(app: AppType) {
      app.provide('dialogsController', new DialogsController())
    },
  }
}

app.use(createPinia())
app.use(createDialogs())
app.use(router)

app.mount('#app')
