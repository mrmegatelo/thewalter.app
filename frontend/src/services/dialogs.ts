import type { App as AppType, Plugin } from 'vue'
import { Injection } from '@/utils/constants.ts'

export class DialogsService {
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

  static initPlugin(): Plugin {
    return {
      install(app: AppType) {
        app.provide(Injection.DialogController, new DialogsService())
      }
    }
  }
}
