import type { InjectionKey } from 'vue'
import type { DialogsService } from '@/services/dialogs.ts'
import type { IntlService } from '@/services/intl.ts'

export const Injection = {
  DialogController: Symbol("dialogs-controller") as InjectionKey<DialogsService>,
  Intl: Symbol("intl") as InjectionKey<IntlService>,
}
