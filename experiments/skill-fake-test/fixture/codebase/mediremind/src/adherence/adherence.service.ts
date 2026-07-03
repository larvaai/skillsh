import { db } from '../common/db';

export class AdherenceService {
  /**
   * Tỉ lệ tuân thủ = số liều 'taken' / tổng số liều "đáng lẽ đã uống".
   * Trả 0..1.
   */
  rateFor(userId: string): number {
    const events = db.doseEvents.filter((e) => e.userId === userId);

    // BUG-6 (chia cho 0): user chưa có DoseEvent nào => events.length = 0 => NaN.
    const taken = events.filter((e) => e.status === 'taken').length;

    // BUG-7 (đếm không nhất quán): mẫu số gồm CẢ 'skipped' (liều user chủ động bỏ,
    // không nên tính là trượt) và cả 'pending' (chưa tới giờ) => rate bị kéo tụt sai.
    const denominator = events.length;

    return taken / denominator;
  }
}
