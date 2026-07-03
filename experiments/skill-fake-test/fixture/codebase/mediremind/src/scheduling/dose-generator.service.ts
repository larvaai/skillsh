import { Schedule } from './schedule.entity';
import { DoseEvent } from './dose-event.entity';
import { db } from '../common/db';

/**
 * Sinh các DoseEvent cho MỘT ngày từ các Schedule đang hoạt động.
 * Chạy mỗi sáng bởi reminder.worker (cron 00:05).
 */
export class DoseGeneratorService {
  generateForDay(userId: string, day: Date): DoseEvent[] {
    const schedules = db.schedules.filter((s) => s.userId === userId);
    const events: DoseEvent[] = [];

    for (const s of schedules) {
      // BUG-1 (timezone): dùng giờ server (new Date của day) chứ không quy về s.timezone.
      // User ở timezone khác sẽ nhận liều lệch giờ local.
      const weekday = day.getDay(); // 0..6 theo giờ server
      if (!s.daysOfWeek.includes(weekday)) continue;

      // BUG-2 (end-date): chỉ chặn start, KHÔNG lọc end_date.
      // Schedule đã hết hạn (end_date trong quá khứ) vẫn sinh liều.
      if (day < s.startDate) continue;

      for (const t of s.timesOfDay) {
        const [hh, mm] = t.split(':').map(Number);
        const scheduled = new Date(day);
        scheduled.setHours(hh, mm, 0, 0); // giờ server, không phải giờ user
        events.push({
          id: `${s.id}-${day.toISOString().slice(0, 10)}-${t}`,
          scheduleId: s.id,
          userId,
          scheduledTime: scheduled,
          status: 'pending',
          takenAt: null,
        });
      }
    }

    db.doseEvents.push(...events);
    return events;
  }
}
