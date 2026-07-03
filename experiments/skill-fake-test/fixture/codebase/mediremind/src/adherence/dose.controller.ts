import { db } from '../common/db';
import { AdherenceService } from './adherence.service';

const adherence = new AdherenceService();

/**
 * POST /doses/:id/confirm  — patient bấm "Đã uống".
 * req.userId đến từ middleware auth (đã xác thực danh tính).
 */
export async function confirmDose(req: { params: { id: string }; userId: string }) {
  const dose = db.doseEvents.find((e) => e.id === req.params.id);
  if (!dose) return { status: 404, body: 'not found' };

  // BUG-5 (IDOR / permission): KHÔNG kiểm dose.userId === req.userId.
  // Bất kỳ user đã đăng nhập nào cũng xác nhận được liều của người khác.
  dose.status = 'taken';
  dose.takenAt = new Date();

  const rate = adherence.rateFor(dose.userId);
  return { status: 200, body: { id: dose.id, status: dose.status, adherenceRate: rate } };
}
