import { db } from '../common/db';
import { pushProvider } from '../common/providers';

/**
 * Gửi reminder cho các DoseEvent 'pending' sắp tới hạn trong cửa sổ [now, now+window].
 * Gọi bởi reminder.worker mỗi phút.
 */
export class ReminderService {
  async dispatchDue(now: Date, windowMinutes = 5): Promise<number> {
    const cutoff = new Date(now.getTime() + windowMinutes * 60_000);
    const due = db.doseEvents.filter(
      (e) => e.status === 'pending' && e.scheduledTime >= now && e.scheduledTime <= cutoff,
    );

    let sent = 0;
    for (const e of due) {
      // BUG-3 (dedupe): không kiểm đã gửi reminder cho dose này chưa.
      // Worker chạy mỗi phút + window 5 phút => mỗi liều bị gửi tới 5 lần.
      // BUG-4 (retry/error): pushProvider.send có thể throw => vòng lặp vỡ,
      // các dose còn lại trong 'due' không được gửi, và không có retry.
      await pushProvider.send(e.userId, `Đến giờ uống thuốc lúc ${e.scheduledTime}`);
      db.reminders.push({ doseEventId: e.id, channel: 'push', sentAt: now });
      sent++;
    }
    return sent;
  }
}
