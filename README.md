# Luyện thi A2 Flyers

Trang luyện thi Cambridge A2 Flyers của Ms Trâm English Hub: hai phần riêng: **Từ vựng** (515 từ theo 19 chủ đề, IPA, nghĩa Anh–Việt, thẻ lật, Word Hunt, phát âm) và **Speaking** (lý thuyết 4 Part, luyện tập Test 1–3 theo A2 Flyers 3 với kiểm tra đáp án, ghi âm).

**Ms Trâm English Hub** · Zalo/HP: 079 29 51 529 · 0898 123 696 · 12 Lê Đình Chinh, Quy Nhơn Nam · https://www.facebook.com/msTram.EClass/

## Mật khẩu

Trang được khóa bằng mật khẩu lớp. Nội dung trong `index.html` đã được mã hóa; `key.json` giữ khóa mở trang, được bảo vệ bằng mật khẩu.

**Đổi mật khẩu (giáo viên):** mở link riêng `https://mstramehub.github.io/flyers-vocabulary/#giao-vien` (mục này ẩn với học sinh), nhập mật khẩu cũ và mật khẩu mới, rồi dán mã được tạo vào file `key.json` trên GitHub và bấm Commit changes. Sau 1–2 phút mật khẩu mới có hiệu lực.

**Sửa nội dung trang:** dùng `tools/sitelock.py` (cần `pip install cryptography`):

```
python3 tools/sitelock.py decrypt source.html MẬT_KHẨU   # lấy bản đọc được
# ... sửa source.html ...
python3 tools/sitelock.py build source.html MẬT_KHẨU     # mã hóa lại vào index.html
```

Không commit `source.html` lên repo này vì repo đang công khai.
