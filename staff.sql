
INSERT INTO `staff_phongban` (`MaPhongBan`, `TenPhongBan`) VALUES
(1, 'FB'),
(2, 'HK'),
(3, 'receptionist'),
(4, 'engineer');

INSERT INTO `staff_nhanvien` (`MaNhanVien`, `HoTen`, `NgaySinh`, `SoDienThoai`, `user_id`, `MaPhongBan_id`) VALUES
(1, 'staff', '2004-09-11', '0397765046', 3, 1),
(2, 'letan', '2025-01-01', '0000000000', 4, 3),
(3, 'HK', '2025-01-01', '0000000000', 5, 2),
(4, 'FB', '2025-01-01', '111111111', 6, 1),
(5, 'ENG', '2025-01-01', '22222222', 7, 4);
