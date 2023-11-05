import random
import math
import os

# Lấy thư mục làm việc hiện tại
thu_muc_hien_tai = os.getcwd()
# Đường dẫn tệp xuất kết quả
duong_dan_tep = os.path.join(thu_muc_hien_tai, "kq.txt")

# Số lượng phòng khám và bác sĩ
so_phong = 10
so_bac_si = 30

# Số ngày trong tháng
so_ngay = 30

# Số lần lặp luyện kim
so_lan_luyen_kim = 1000


# khởi tạo lich xếp ban đầu có xung đột xảy ra
def lich_xep_voi_xung_dot():
    # Tạo một mảng lịch_xếp với các giá trị ban đầu là None (không có bác sĩ làm việc)
    lich_xep = [[None for _ in range(so_ngay)] for _ in range(so_phong)]

    # Khởi tạo ngày ban đầu
    ngay = 0

    # Tạo danh sách bác sĩ với tên là "Bác sĩ 1", "Bác sĩ 2",...
    bac_si = [f"Bác sĩ {i}" for i in range(1, so_bac_si + 1)]

    for _ in range(so_ngay):
        # Trộn ngẫu nhiên danh sách bác sĩ để sử dụng trong ngày
        random.shuffle(bac_si)

        for phong in range(so_phong):
            if bac_si:
                # Lấy bác sĩ đầu tiên từ danh sách và gán cho ô trong lịch_xếp
                bac_si_hien_tai = bac_si.pop()
                lich_xep[phong][ngay] = bac_si_hien_tai
            else:
                # Nếu danh sách bác sĩ đã rỗng, tái tạo danh sách và trộn lại
                bac_si = [f"Bác sĩ {i}" for i in range(1, so_bac_si + 1)]
                random.shuffle(bac_si)

                # Lấy bác sĩ đầu tiên từ danh sách và gán cho ô trong lịch_xếp
                bac_si_hien_tai = bac_si.pop()
                lich_xep[phong][ngay] = bac_si_hien_tai

                # Thêm xung đột nhiều lần cho mỗi ngày (ở đây thêm xung đột )
                for _ in range(2):
                    ngay_lap = random.randint(
                        0, so_ngay - 1
                    )  # Chọn ngẫu nhiên một ngày
                    lich_xep[phong][ngay_lap] = bac_si_hien_tai

        ngay += 1

    return lich_xep


# xuất ra các ngày có xung đột khi khởi tạo ban đầu
def xuat_ngay_xung_dot(lich_xep):
    ngay_xung_dot = []  # Danh sách chứa các ngày có xung đột

    for ngay in range(so_ngay):
        bac_si_dang_lam = (
            set()
        )  # Tạo một tập hợp để theo dõi các bác sĩ đang làm việc trong ngày
        co_xung_dot = False

        for phong in range(so_phong):
            bac_si = lich_xep[phong][
                ngay
            ]  # Lấy thông tin về bác sĩ làm việc trong phòng và ngày đó
            if bac_si is not None:
                if bac_si in bac_si_dang_lam:
                    co_xung_dot = True  # Nếu một bác sĩ làm việc ở nhiều phòng cùng một ngày, có xung đột
                    break  # Ngừng kiểm tra tiếp

                bac_si_dang_lam.add(bac_si)  # Thêm bác sĩ đang làm việc vào tập hợp

        if co_xung_dot:
            ngay_xung_dot.append(
                ngay + 1
            )  # Nếu có xung đột, thêm ngày có xung đột vào danh sách

    return ngay_xung_dot


# Hàm mục tiêu (objective function) - đánh giá chất lượng lịch xếp
def ham_muc_tieu(lich_xep):
    so_xung_dot = 0  # Khởi tạo số xung đột ban đầu là 0

    # Duyệt qua từng ngày trong lịch xếp
    for ngay in range(so_ngay):
        bac_si_dang_lam = (
            set()
        )  # Tạo một tập hợp để theo dõi bác sĩ đang làm việc trong ngày
        for phong in range(so_phong):
            bac_si = lich_xep[phong][
                ngay
            ]  # Lấy thông tin về bác sĩ làm việc trong phòng và ngày đó
            if bac_si is not None:
                if bac_si in bac_si_dang_lam:
                    so_xung_dot += 1  # Nếu một bác sĩ làm việc ở nhiều phòng cùng một ngày, tăng số xung đột lên 1
                bac_si_dang_lam.add(bac_si)  # Thêm bác sĩ đang làm việc vào tập hợp

        if len(bac_si_dang_lam) != so_phong:
            # Nếu số bác sĩ đang làm việc không đủ số phòng, cộng thêm số lượng bác sĩ thiếu vào số xung đột
            so_xung_dot += abs(len(bac_si_dang_lam) - so_phong)

    return so_xung_dot  # Trả về số xung đột, đánh giá chất lượng lịch xếp


# Kiểm tra ràng buộc: một bác sĩ không được làm việc trong nhiều phòng
def khong_bac_si_khong_lam_nhieu_phong(lich_xep, bac_si, phong, ngay):
    # Kiểm tra cùng một ngày trong các phòng khám khác
    for other_phong in range(so_phong):
        if other_phong != phong and lich_xep[other_phong][ngay] == bac_si:
            return False

    return True


# Thuật toán luyện kim
def luyen_kim(lich_xep):
    lich_xep_hien_tai = lich_xep
    nang_luong_hien_tai = ham_muc_tieu(lich_xep_hien_tai)

    for _ in range(so_lan_luyen_kim):
        # Chọn một phần lịch xếp con
        phong1, ngay1 = random.randint(0, so_phong - 1), random.randint(0, so_ngay - 1)
        phong2, ngay2 = random.randint(0, so_phong - 1), random.randint(0, so_ngay - 1)

        # Lấy bác sĩ trong các ô đã chọn
        bac_si1, bac_si2 = (
            lich_xep_hien_tai[phong1][ngay1],
            lich_xep_hien_tai[phong2][ngay2],
        )

        # Kiểm tra ràng buộc
        if khong_bac_si_khong_lam_nhieu_phong(
            lich_xep_hien_tai, bac_si1, phong1, ngay1
        ):
            # Hoán đổi bác sĩ trong hai ô
            lich_xep_hien_tai[phong1][ngay1], lich_xep_hien_tai[phong2][ngay2] = (
                lich_xep_hien_tai[phong2][ngay2],
                lich_xep_hien_tai[phong1][ngay1],
            )

            nang_luong_moi = ham_muc_tieu(lich_xep_hien_tai)

            # Tính sự khác biệt về chất lượng
            delta_nang_luong = nang_luong_moi - nang_luong_hien_tai

            # Chấp nhận hoặc từ chối hoán đổi dựa trên xác suất
            if delta_nang_luong < 0 or random.random() < math.exp(
                -delta_nang_luong / 0.1
            ):
                nang_luong_hien_tai = nang_luong_moi
            else:
                # Hoàn tác hoán đổi
                lich_xep_hien_tai[phong1][ngay1], lich_xep_hien_tai[phong2][ngay2] = (
                    lich_xep_hien_tai[phong2][ngay2],
                    lich_xep_hien_tai[phong1][ngay1],
                )

    return lich_xep_hien_tai, nang_luong_hien_tai


# Khởi tạo lịch xếp ban đầu
lich_xep_ban_dau = lich_xep_voi_xung_dot()

# Xuất ra lịch xếp ban đầu
print("Lịch xếp ban đầu:")
for ngay in range(so_ngay):
    print(f"Ngày {ngay + 1}:")
    for phong in range(so_phong):
        print(lich_xep_ban_dau[phong][ngay], end="\t")
    print()
print("Chất lượng ban đầu:", ham_muc_tieu(lich_xep_ban_dau))

# xuất các ngày có xung đột
ngay_xung_dot = xuat_ngay_xung_dot(lich_xep_ban_dau)
if ngay_xung_dot:
    print("Các ngày bị xung đột khi tạo lịch:")
    print(ngay_xung_dot)

# Đưa vào thuật toán
if ham_muc_tieu(lich_xep_ban_dau) == 0:
    print("Chất lượng ban đầu đã đạt 0. Không cần áp dụng thuật toán.")
else:
    # Áp dụng thuật toán luyện kim
    lich_xep_cuoi_cung, nang_luong_cuoi_cung = luyen_kim(lich_xep_ban_dau)

    print("\nLịch xếp sau khi áp dụng luyện kim:")

    # In lịch xếp theo từng ngày và từng phòng
    for ngay in range(so_ngay):
        print(f"Ngày {ngay + 1}:")
        for phong in range(so_phong):
            print(lich_xep_cuoi_cung[phong][ngay], end="\t")
        print()

    print("Chất lượng cuối cùng:", nang_luong_cuoi_cung)

# Xuất ra số ngày làm việc của từng bác sĩ
so_ngay_lam_viec_bac_si = {f"Bác sĩ {bac_si}": 0 for bac_si in range(1, so_bac_si + 1)}
for ngay in range(so_ngay):
    for phong in range(so_phong):
        bac_si = lich_xep_cuoi_cung[phong][ngay]
        if bac_si is not None:
            so_ngay_lam_viec_bac_si[bac_si] += 1

print("\nSố ngày làm việc của mỗi bác sĩ:")
for bac_si, so_ngay_lam_viec in so_ngay_lam_viec_bac_si.items():
    print(f"{bac_si}: {so_ngay_lam_viec} ngày")

# Ghi kết quả vào tệp văn bản
with open(duong_dan_tep, "w", encoding="utf-8") as f:
    f.write("Lịch xếp sau khi áp dụng luyện kim:\n")

    # Ghi tên phòng từ 1 đến 10 cho mỗi cột
    ten_phong = [f"Phòng {i}" for i in range(1, so_phong + 1)]
    f.write("\t")
    f.write("\t\t".join(ten_phong) + "" + "\n")

    for ngay in range(so_ngay):
        f.write(f"Ngày {ngay + 1}:\n")
        f.write("\t")
        for phong in range(so_phong):
            if lich_xep_cuoi_cung[phong][ngay] is not None:
                f.write(lich_xep_cuoi_cung[phong][ngay] + "\t")
            else:
                f.write("\t")
        f.write("\n")
    f.write(f" Chất lượng cuối cùng: {nang_luong_cuoi_cung}\n")
    f.write("\nSố ngày làm việc của mỗi bác sĩ:\n")
    for bac_si, so_ngay_lam_viec in so_ngay_lam_viec_bac_si.items():
        f.write(f"{bac_si}: {so_ngay_lam_viec} ngày\n")
