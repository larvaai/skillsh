import { db } from '../common/db';

/**
 * Caregiver chỉ được XEM dữ liệu của patient mà họ có CaregiverLink (scope view-only).
 * Dùng ở các route báo cáo adherence của caregiver.
 */
export function canCaregiverView(caregiverId: string, patientId: string): boolean {
  const link = db.caregiverLinks.find(
    (l) => l.caregiverId === caregiverId && l.patientId === patientId,
  );
  return !!link && link.scope === 'view-only';
}
