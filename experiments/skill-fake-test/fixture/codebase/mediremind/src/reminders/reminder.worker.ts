import { DoseGeneratorService } from '../scheduling/dose-generator.service';
import { ReminderService } from './reminder.service';
import { db } from '../common/db';

const generator = new DoseGeneratorService();
const reminders = new ReminderService();

// cron 00:05 mỗi ngày: sinh liều cho hôm nay
export async function nightlyGenerate() {
  const today = new Date();
  const userIds = [...new Set(db.schedules.map((s) => s.userId))];
  for (const uid of userIds) generator.generateForDay(uid, today);
}

// cron mỗi phút: bắn reminder tới hạn
export async function everyMinute() {
  await reminders.dispatchDue(new Date());
}
