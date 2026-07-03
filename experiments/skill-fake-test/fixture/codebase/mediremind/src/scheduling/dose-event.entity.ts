export type DoseStatus = 'pending' | 'taken' | 'missed' | 'skipped';

export interface DoseEvent {
  id: string;
  scheduleId: string;
  userId: string;
  scheduledTime: Date;
  status: DoseStatus;
  takenAt: Date | null;
}
