import type { App as AppType, Plugin } from 'vue'
import { Injection } from '@/utils/constants.ts'

export class IntlService {
  private readonly _datetime: Intl.DateTimeFormat
  constructor() {
    this._datetime = new Intl.DateTimeFormat(['en-GB'], {
      month: 'short',
      year: 'numeric',
      day: 'numeric',
    })
  }

  formatDate(date: Date): string {
    return this._datetime.format(date)
  }

  static initPlugin(): Plugin {
    return {
      install: (app: AppType) => {
        app.provide(Injection.Intl, new IntlService())
      }
    }
  }
}
