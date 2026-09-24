// Horloge de dev : décale « maintenant » de N jours (voyage dans le temps pour tester streak, J+1…).
// Remplace globalThis.Date par une sous-classe : index.ts et le faux Supabase la voient tous les deux.
const RealDate = Date;
let offsetMs = 0;

class DevDate extends RealDate {
  // deno-lint-ignore no-explicit-any
  constructor(...args: any[]) {
    if (args.length === 0) super(RealDate.now() + offsetMs);
    // deno-lint-ignore no-explicit-any
    else super(...(args as [any]));
  }
  static override now() { return RealDate.now() + offsetMs; }
}

export function installClock() {
  // deno-lint-ignore no-explicit-any
  (globalThis as any).Date = DevDate;
}
export function setOffsetDays(n: number) { offsetMs = Math.round(n * 86400000); }
export function getOffsetDays() { return offsetMs / 86400000; }
