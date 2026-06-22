# Bao cao kiem thu chuc nang

## 1. Muc tieu

Kiem thu mot so chuc nang cot loi cua he thong Crowdfunding Platform nham xac minh cac luong nghiep vu chinh hoat dong dung yeu cau:

- Dang ky va dang nhap tai khoan nha dau tu.
- Dang ky tro thanh chu du an va quy trinh admin xet duyet.
- Hien thi danh sach du an cong khai va ghi nhan hanh vi xem du an.
- Xem vi, nap tien, rut tien va loc lich su giao dich.
- Tao giao dich dau tu cho du an dang mo.
- Giai ngan va hoan tra von giua chu du an va nha dau tu.

## 2. Moi truong kiem thu

- Backend: Django REST Framework.
- Database test: Django tu dong tao test database tu cau hinh hien tai.
- Cong cu kiem thu: Django `manage.py test`, DRF `APITestCase`.
- Lenh chay:

```powershell
python manage.py test accounts projects transactions
```

## 3. Pham vi va chuc nang duoc chon

| Nhom chuc nang | Ly do chon |
| --- | --- |
| Tai khoan | La diem vao cua he thong, can dam bao nguoi dung dang ky dung vai tro va dang nhap thanh cong. |
| Dang ky chu du an | Kiem tra quy trinh nang cap vai tro tu investor sang project owner va quyen xu ly cua admin. |
| Du an | La doi tuong trung tam cua nen tang crowdfunding, can dam bao chi hien thi du an hop le cho cong khai. |
| Vi va giao dich | La nhom chuc nang lien quan truc tiep den so du, nap tien, rut tien va truy vet lich su giao dich cua nha dau tu. |
| Dau tu | La luong giao dich quan trong giua nha dau tu va du an. |
| Dong tien chu du an | Kiem tra giai ngan, hoan tra va chia tien cho nha dau tu theo ty le gop von. |

## 4. Cac truong hop kiem thu

| Ma TC | Chuc nang | Dieu kien / Du lieu dau vao | Ket qua mong doi | Ket qua thuc te |
| --- | --- | --- | --- | --- |
| TC01 | Dang ky tai khoan | Email hop le, mat khau hop le, client gui role `ADMIN` | He thong tao user moi, ep role ve `INVESTOR`, tao wallet tu dong | Dat |
| TC02 | Dang nhap | Email va mat khau dung | Tra ve access token, refresh token va role cua user | Dat |
| TC03 | Dang nhap sai | Email dung, mat khau sai | Tra ve HTTP 401 Unauthorized | Dat |
| TC04 | Danh sach du an cong khai | Co 1 du an `OPEN`, 1 du an `PENDING` | API danh sach chi tra ve du an `OPEN` | Dat |
| TC05 | Xem chi tiet du an | Investor da dang nhap xem du an `OPEN` | Tra ve chi tiet du an va ghi nhan interaction `view`, `click` | Dat |
| TC06 | Tao lenh dau tu | Investor dau tu 200 vao du an `OPEN`; Stripe duoc mock | Tao transaction `INVEST` trang thai `PENDING`, luu payment intent id, chua tang `raised` | Dat |
| TC07 | Dau tu vuot muc goi von | So tien dau tu lam vuot `funding_target` | Tra ve HTTP 400 va khong tao transaction | Dat |
| TC08 | Giai ngan cho chu du an | Du an da `FUNDED`, tong dau tu bang muc goi von | Vi chu du an tang tien, du an danh dau da giai ngan, tao transaction `OWNER_DISBURSE` | Dat |
| TC09 | Hoan tra mot phan | Chu du an tra 50, hai nha dau tu gop 60/40 | Tien duoc chia 30/20, du an chuyen `REPAYING` | Dat |
| TC10 | Hoan tra day du | Chu du an tra du 100 | Du an chuyen `COMPLETED`, `total_repaid` bang 100 | Dat |
| TC11 | Xem so du vi | Investor da dang nhap, vi co so du 250 VND | API tra ve dung `balance` va `currency` cua vi | Dat |
| TC12 | Nap tien | Investor nap 500 VND; Stripe duoc mock | Tao transaction `FUND_IN` trang thai `PENDING`, tra ve `clientSecret` | Dat |
| TC13 | Rut tien thieu tai khoan ngan hang | Investor chua co bank account mac dinh | Tra ve HTTP 400 va thong bao khong tim thay tai khoan ngan hang mac dinh | Dat |
| TC14 | Rut tien thanh cong | Investor co 300 VND va bank account mac dinh, rut 120 VND | Vi con 180 VND, tao transaction `FUND_OUT` trang thai `SUCCESS` | Dat |
| TC15 | Loc lich su giao dich | Investor co nhieu giao dich, request `type=fund_in` | Chi tra ve giao dich `FUND_IN` cua user dang dang nhap | Dat |
| TC16 | Xem ho so dang ky chu du an khi chua nop | Investor chua co application | Tra ve HTTP 404 Application not found | Dat |
| TC17 | Nop ho so dang ky chu du an | Investor gui thong tin doanh nghiep hop le | Tao application trang thai `PENDING` | Dat |
| TC18 | Chan chu du an nop lai ho so | User da co role `PROJECT_OWNER` gui application | Tra ve HTTP 403, khong cho nop | Dat |
| TC19 | Admin xem danh sach ho so | Admin da dang nhap, he thong co application | Tra ve danh sach application kem email nguoi nop | Dat |
| TC20 | Admin duyet ho so | Application dang `PENDING` | Application thanh `APPROVED`, user duoc doi role sang `PROJECT_OWNER` | Dat |
| TC21 | Tu choi ho so thieu ly do | Admin reject nhung khong nhap `reject_reason` | Tra ve HTTP 400 va bao loi `reject_reason` | Dat |

## 5. Ket qua chay test

Ket qua thuc thi ngay 30/05/2026:

```text
Found 21 test(s).
System check identified no issues (0 silenced).
Ran 21 tests in 28.098s
OK
```

Trong qua trinh chay co log HTTP 401, 403, 404 va 400 o cac test am tinh. Day la ket qua mong doi cua cac ca dang nhap sai, chua co ho so dang ky, user khong du quyen, reject thieu ly do, dau tu vuot muc goi von va rut tien khi chua co tai khoan ngan hang mac dinh.

Qua kiem thu bo sung, phat hien loi khi rut tien: API chuyen `amount` sang `float` trong khi so du vi la `Decimal`, gay loi tinh toan tien te. Loi da duoc sua bang cach parse `amount` thanh `Decimal` trong view rut tien.

## 6. Danh gia

Tat ca 21/21 test case deu dat. Cac chuc nang duoc chon da bao phu duoc nhung luong nghiep vu quan trong: xac thuc nguoi dung, dang ky tro thanh chu du an, hien thi du an, quan ly vi va giao dich, tao giao dich dau tu, giai ngan va hoan tra tien. Cac dich vu ben ngoai nhu Stripe duoc mock trong test de dam bao kiem thu on dinh va khong tao giao dich that.
