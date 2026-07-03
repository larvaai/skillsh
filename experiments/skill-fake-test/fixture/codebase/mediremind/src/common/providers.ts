// Cổng gửi push/sms ra ngoài (Expo/Twilio). Ở slice demo là stub.
export const pushProvider = {
  async send(userId: string, message: string): Promise<void> {
    // thật sẽ gọi HTTP tới provider; có thể throw khi provider lỗi/timeout.
    if (!userId) throw new Error('missing userId');
  },
};
