DELIMITER $$
CREATE DEFINER=`qlks_admin`@`%` PROCEDURE `AddCustomer`(IN `tenKhachHang` VARCHAR(100), IN `diaChi` VARCHAR(100), IN `soDienThoai` VARCHAR(12))
BEGIN
   INSERT INTO customer_khachhang(TenKhachHang, DiaChi, SoDienThoai) VALUES (tenKhachHang, diaChi, soDienThoai);
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`qlks_admin`@`%` PROCEDURE `AddInvoices`(IN `ngayLapHoaDon` DATE, IN `tongTien` INT(200), IN `maSuDung_id` INT(10))
BEGIN 
INSERT INTO invoices_hoadon (NgayLapHoaDon, TongTien, MaSuDung_id)
VALUES (ngayLapHoaDon, tongTien, maSuDung_id);
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`qlks_admin`@`%` PROCEDURE `AddRoom`(IN `p_soPhong` VARCHAR(10), IN `p_TrangThai` VARCHAR(20), IN `p_MaLoai_id` INT)
BEGIN
    INSERT INTO room_phong (SoPhong, TrangThai, MaLoai_id) 
    VALUES (p_soPhong, p_TrangThai, p_MaLoai_id);
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`qlks_admin`@`%` PROCEDURE `AddService`(IN `p_TenDichVu` VARCHAR(100), IN `p_GiaDichVu` DECIMAL(10,2))
BEGIN
    IF p_GiaDichVu < 0 THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Giá dịch vụ không hợp lệ';
    ELSE
        INSERT INTO service_dichvu (TenDichVu, GiaDichVu)
        VALUES (p_TenDichVu, p_GiaDichVu);
    END IF;
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`qlks_admin`@`%` PROCEDURE `AddStaff`(
    IN p_HoTen VARCHAR(255),
    IN p_NgaySinh DATE,
    IN p_SoDienThoai VARCHAR(20),
    IN p_MaPhongBan_id INT
)
BEGIN
    INSERT INTO staff_nhanvien (HoTen, NgaySinh, SoDienThoai, MaPhongBan_id) 
    VALUES (p_HoTen, p_NgaySinh, p_SoDienThoai, p_MaPhongBan_id);
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`qlks_admin`@`%` PROCEDURE `DeleteCustomer`(IN `maKhachHang` INT)
BEGIN
    DELETE FROM customer_khachhang 
    WHERE MaKhachHang = maKhachHang;
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`qlks_admin`@`%` PROCEDURE `DeleteInvoices`(IN `p_MaHoaDon` INT)
BEGIN
    DELETE FROM invoices_hoadon WHERE MaHoaDon = p_MaHoaDon;
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`qlks_admin`@`%` PROCEDURE `DeleteRoom`(IN p_MaPhong INT)
BEGIN
    DELETE FROM room_phong WHERE MaPhong = p_MaPhong;
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`qlks_admin`@`%` PROCEDURE `DeleteService`(IN `p_MaDichVu` INT)
BEGIN
    IF NOT EXISTS (SELECT 1 FROM service_dichvu WHERE MaDichVu = p_MaDichVu) 
    THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Dịch vụ không tồn tại';
    ELSE
        DELETE FROM service_dichvu WHERE MaDichVu = p_MaDichVu;
    END IF;
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`qlks_admin`@`%` PROCEDURE `DeleteStaff`(IN p_MaNhanVien INT)
BEGIN
    DELETE FROM staff_nhanvien WHERE MaNhanVien = p_MaNhanVien;
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`qlks_admin`@`%` PROCEDURE `GetALLInvoicesType`()
SELECT * FROM service_sudungdichvu$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`qlks_admin`@`%` PROCEDURE `GetAllCustomer`()
BEGIN
   select *
   from customer_khachhang;
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`qlks_admin`@`%` PROCEDURE `GetAllInvoices`()
BEGIN
    SELECT *
    FROM invoices_hoadon;
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`qlks_admin`@`%` PROCEDURE `GetAllMaUseService`()
begin
select MaSuDung
from service_sudungdichvu
;
end$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`qlks_admin`@`%` PROCEDURE `GetAllPhongBan`()
begin
select * from staff_phongban;
end$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`qlks_admin`@`%` PROCEDURE `GetAllRentRoom`()
BEGIN
  SELECT *
  FROM customer_thuephong ct
  JOIN customer_khachhang ck ON 
  ct.MaKhachHang_id = ck.MaKhachHang
  JOIN room_phong rp ON ct.MaPhong_id = 
  rp.MaPhong;
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`qlks_admin`@`%` PROCEDURE `GetAllRoomType`()
BEGIN 
    SELECT * FROM room_loaiphong;
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`qlks_admin`@`%` PROCEDURE `GetAllRooms`()
BEGIN
    SELECT p.MaPhong, p.SoPhong, p.TrangThai, l.TenLoai
    FROM room_phong p
    JOIN room_loaiphong l ON p.MaLoai_id = l.MaLoai;
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`qlks_admin`@`%` PROCEDURE `GetAllService`()
BEGIN
    SELECT * FROM service_dichvu;
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`qlks_admin`@`%` PROCEDURE `GetAllStaff`()
BEGIN
	select * 
    from staff_nhanvien sn
join staff_phongban sp on sn.MaPhongBan_id = sp.MaPhongBan
;
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`qlks_admin`@`%` PROCEDURE `GetAllUsage`()
BEGIN
    SELECT 
        sddv.MaSuDung,
        p.SoPhong,
        kh.TenKhachHang,
        dv.TenDichVu,
        sddv.SoLuong,
        sddv.NgaySuDung,
        dv.GiaDichVu,
        (sddv.SoLuong * dv.GiaDichVu) AS ThanhTien
    FROM service_sudungdichvu sddv
    INNER JOIN service_dichvu dv 
    ON sddv.MaDichVu_id = dv.MaDichVu
    INNER JOIN customer_thuephong tp
    ON sddv.MaThue_id = tp.MaThue
    INNER JOIN room_phong p
    ON tp.MaPhong_id = p.MaPhong
    INNER JOIN customer_khachhang kh
    ON tp.MaKhachHang_id = kh.MaKhachHang
    ORDER BY sddv.NgaySuDung DESC;
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`qlks_admin`@`%` PROCEDURE `GetCustomer`(IN `maKhachHang` INT(11))
BEGIN
  SELECT *
  FROM customer_khachhang ck
  WHERE ck.MaKhachHang = maKhachHang;
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`qlks_admin`@`%` PROCEDURE `GetDetailInvoices`()
begin
select *
from invoices_hoadon
where MaHoaDon = maHoaDon;
end$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`qlks_admin`@`%` PROCEDURE `GetDetailRoom`(IN `p_MaPhong` INT)
begin
select *
from room_phong
where MaPhong = p_MaPhong;

end$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`qlks_admin`@`%` PROCEDURE `GetDetailStaff`(IN `p_MaNhanVien` INT(15))
begin
select *
from staff_nhanvien
where MaNhanVien = p_MaNhanVien;

end$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`qlks_admin`@`%` PROCEDURE `GetInvoices`(IN `maHoaDon` INT(15))
BEGIN
SELECT * 
FROM invoices_hoadon hd
WHERE hd.MaHoaDon = maHoaDon;
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`qlks_admin`@`%` PROCEDURE `GetPhongBanById`(IN `p_MaPhongBan` INT)
begin
select tenphongban from staff_phongban;
end$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`qlks_admin`@`%` PROCEDURE `GetRoomById`(IN p_MaPhong INT)
BEGIN
    SELECT * FROM room_phong WHERE MaPhong = p_MaPhong;
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`qlks_admin`@`%` PROCEDURE `GetService`(IN `p_MaDichVu` INT)
BEGIN
    SELECT * FROM service_dichvu
    WHERE MaDichVu = p_MaDichVu;
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`qlks_admin`@`%` PROCEDURE `SearchInvoices`(IN `p_MaHoaDon` INT, IN `p_NgayLapHoaDon` DATE, IN `p_TongTien` DECIMAL(15,2), IN `p_MaSuDung` INT)
BEGIN
    -- Truy vấn tìm kiếm hóa đơn
    SELECT 
        hd.MaHoaDon, 
        hd.NgayLapHoaDon, 
        hd.TongTien, 
        hd.MaSuDung_id
    FROM invoices_hoadon hd
    JOIN service_sudungdichvu dv ON hd.MaSuDung_id = dv.MaSuDung 
    WHERE 
        (p_MaHoaDon IS NULL OR hd.MaHoaDon = p_MaHoaDon)
        AND (p_NgayLapHoaDon IS NULL OR hd.NgayLapHoaDon = p_NgayLapHoaDon)
        AND (p_TongTien IS NULL OR hd.TongTien = p_TongTien)
        AND (p_MaSuDung IS NULL OR hd.MaSuDung_id = p_MaSuDung);
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`qlks_admin`@`%` PROCEDURE `SearchRooms`(
    IN p_SoPhong VARCHAR(10),
    IN p_TrangThai VARCHAR(20),
    IN p_TenLoai VARCHAR(50)  -- Đổi từ p_MaLoai thành p_TenLoai
)
BEGIN
    SELECT 
        p.MaPhong, 
        p.SoPhong, 
        p.TrangThai, 
        p.MaLoai_id, 
        l.TenLoai
    FROM room_phong p
    JOIN room_loaiphong l ON p.MaLoai_id = l.MaLoai  -- JOIN để lấy TenLoai
    WHERE 
        (p_SoPhong IS NULL OR p.SoPhong LIKE CONCAT('%', p_SoPhong, '%')) 
        AND (p_TrangThai IS NULL OR p.TrangThai = p_TrangThai)
        AND (p_TenLoai IS NULL OR l.TenLoai LIKE CONCAT('%', p_TenLoai, '%'));  -- Lọc theo TenLoai
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`qlks_admin`@`%` PROCEDURE `SearchStaff`(
    IN p_HoTen VARCHAR(255), 
    IN p_MaNhanVien INT, 
    IN p_MaPhongBan INT
)
BEGIN
    SELECT 
        s.MaNhanVien, 
        s.HoTen, 
        s.NgaySinh, 
        s.SoDienThoai, 
        s.MaPhongBan_id, 
        p.TenPhongBan
    FROM staff_nhanvien s
    JOIN staff_phongban p ON s.MaPhongBan_id = p.MaPhongBan  -- JOIN để lấy TenPhongBan
    WHERE 
        (p_HoTen IS NULL OR s.HoTen LIKE CONCAT('%', p_HoTen, '%')) 
        AND (p_MaNhanVien IS NULL OR s.MaNhanVien = p_MaNhanVien)
        AND (p_MaPhongBan IS NULL OR s.MaPhongBan_id = p_MaPhongBan);
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`qlks_admin`@`%` PROCEDURE `UpdateCustomer`(IN `maKhachHang` INT(11), IN `tenKhachHang` VARCHAR(100), IN `DiaChi` VARCHAR(100), IN `soDienThoai` VARCHAR(15))
BEGIN
    UPDATE customer_khachhang ck
    SET ck.TenKhachHang = tenKhachHang, ck.DiaChi = diaChi, ck.SoDienThoai = soDienThoai
    WHERE ck.MaKhachHang = maKhachHang;
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`qlks_admin`@`%` PROCEDURE `UpdateInvoices`(IN `h_maHoaDon` INT(15), IN `h_ngayLapHoaDon` DATE, IN `h_maSuDung_id` INT(10), IN `h_tongTien` DECIMAL(30))
BEGIN
    UPDATE invoices_hoadon hd
    SET hd.NgayLapHoaDon = h_ngayLapHoaDon, hd.TongTien = h_tongTien, hd.MaSuDung_id = h_maSuDung_id
    WHERE hd.MaHoaDon = h_maHoaDon;
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`qlks_admin`@`%` PROCEDURE `UpdateRoom`(
    IN p_soPhong INT,
    IN p_TrangThai VARCHAR(50),
    IN p_MaLoai INT,
    IN p_MaPhong INT
)
BEGIN
    UPDATE room_phong 
    SET soPhong = p_soPhong, TrangThai = p_TrangThai, MaLoai_id = p_MaLoai
    WHERE MaPhong = p_MaPhong;
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`qlks_admin`@`%` PROCEDURE `UpdateService`(IN `p_MaDichVu` INT, IN `p_TenDichVu` VARCHAR(100), IN `p_GiaDichVu` DECIMAL(10,2))
BEGIN
    IF NOT EXISTS (SELECT 1 FROM service_dichvu WHERE MaDichVu = p_MaDichVu) 
    THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Dịch vụ không tồn tại';
    ELSEIF p_GiaDichVu < 0 THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Giá dịch vụ không hợp lệ';
    ELSE
        UPDATE service_dichvu
        SET 
            TenDichVu = p_TenDichVu,
            GiaDichVu = p_GiaDichVu
        WHERE MaDichVu = p_MaDichVu;
    END IF;
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`qlks_admin`@`%` PROCEDURE `UpdateStaff`(
    IN p_MaNhanVien INT,
    IN p_HoTen VARCHAR(255),
    IN p_NgaySinh DATE,
    IN p_SoDienThoai VARCHAR(20),
    IN p_MaPhongBan_id INT
)
BEGIN
    UPDATE staff_nhanvien 
    SET HoTen = p_HoTen, 
        NgaySinh = p_NgaySinh, 
        SoDienThoai = p_SoDienThoai, 
        MaPhongBan_id = p_MaPhongBan_id
    WHERE MaNhanVien = p_MaNhanVien;
END$$
DELIMITER ;
