import { Schedule } from '../scheduling/schedule.entity';
import { DoseEvent } from '../scheduling/dose-event.entity';

// Repo in-memory giả lập (slice demo). Thật sẽ là Postgres.
export const db = {
  schedules: [] as Schedule[],
  doseEvents: [] as DoseEvent[],
  reminders: [] as { doseEventId: string; channel: 'push' | 'sms'; sentAt: Date }[],
  caregiverLinks: [] as { caregiverId: string; patientId: string; scope: string }[],
};
