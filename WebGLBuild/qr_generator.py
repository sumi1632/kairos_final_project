import qrcode

def generate_qr_codes(base_url):
    # 테이블 1 QR 코드 생성
    qr1 = qrcode.QRCode(version=1, box_size=10, border=5)
    qr1.add_data(f"{base_url}/table/1")
    qr1.make(fit=True)
    img1 = qr1.make_image(fill_color="black", back_color="white")
    img1.save("table1_qr.png")
    
    # 테이블 2 QR 코드 생성
    qr2 = qrcode.QRCode(version=1, box_size=10, border=5)
    qr2.add_data(f"{base_url}/table/2")
    qr2.make(fit=True)
    img2 = qr2.make_image(fill_color="black", back_color="white")
    img2.save("table2_qr.png")

if __name__ == "__main__":
    # 실제 접속 가능한 IP 주소와 포트
    base_url = "http://172.30.1.27:5000"  # 여기를 실제 IP 주소로 변경
    generate_qr_codes(base_url) 