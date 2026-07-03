export interface Schedule {
  id: string;
  userId: string;
  medicationId: string;
  timesOfDay: string[];   // ["08:00", "20:00"]
  daysOfWeek: number[];   // 0..6
  startDate: Date;
  endDate: Date | null;   // null = vô thời hạn
  timezone: string;       // vd "Asia/Ho_Chi_Minh" — HIỆN chưa được dùng ở generator
}
