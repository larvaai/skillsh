import { DoseEvent } from '../scheduling/dose-event.entity';

// Đoạn KHÓ ĐỌC (dành cho /teen): tính chuỗi ngày liên tiếp uống đủ liều.
export function currentStreak(evts: DoseEvent[]): number {
  const byDay = evts.reduce<Record<string, number[]>>((a, e) => {
    const k = e.scheduledTime.toISOString().slice(0, 10);
    (a[k] ??= []).push(e.status === 'taken' ? 1 : e.status === 'skipped' ? -1 : 0);
    return a;
  }, {});
  const days = Object.keys(byDay).sort().reverse();
  let s = 0;
  for (const d of days) {
    const arr = byDay[d];
    const ok = arr.every((x) => x !== 0) && arr.reduce((p, c) => p + c, 0) === arr.length;
    if (ok) s++;
    else break;
  }
  return s;
}
