import type { InjectionKey } from 'vue'
import type { DialogsService } from '@/services/dialogs.ts'

export const Injection = {
  DialogController: Symbol("dialogs-controller") as InjectionKey<DialogsService>,
}
