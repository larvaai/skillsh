// LEGACY — cron nhắc thuốc bản đầu, viết trước khi tách ReminderService.
// Không còn được import ở đâu (đã thay bằng reminders/reminder.worker.ts).
// Giữ lại "phòng khi cần". Dùng biến toàn cục setInterval, không test, không timezone.
let timer: any = null;

export function startOldCron(sendFn: (uid: string, msg: string) => void) {
  timer = setInterval(() => {
    // logic cũ: quét toàn bộ, gửi hết, không cửa sổ, không dedupe
    console.log('[old cron] tick');
  }, 60_000);
}

export function stopOldCron() {
  if (timer) clearInterval(timer);
}
