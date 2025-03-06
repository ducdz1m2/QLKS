DELIMITER $$
CREATE DEFINER=`qlks_admin`@`%` FUNCTION `CanBookRoom`(p_MaPhong INT) RETURNS tinyint(1)
    DETERMINISTIC
BEGIN
    DECLARE room_status VARCHAR(20);
    
    -- Lấy trạng thái phòng từ bảng Phong
    SELECT TrangThai INTO room_status 
    FROM room_phong 
    WHERE MaPhong = p_MaPhong;

    -- Trả về 1 nếu phòng trống, 0 nếu không
    RETURN IF(room_status = 'Trống', 1, 0);
END$$
DELIMITER ;
