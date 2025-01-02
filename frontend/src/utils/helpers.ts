export function debounce<F extends (...args: Parameters<F>) => unknown>(fn: F, delay: number) {
  let timeoutId: number;
  return function (this: unknown, ...args: Parameters<F>) {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => {
      fn.apply(this, args);
    }, delay);
  };
}
