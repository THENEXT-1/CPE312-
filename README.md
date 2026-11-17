# BaanD — Model as a Service

โปรเจกต์ CPE312 สำหรับสาธิตบริการทำนายค่าบ้านในแคลิฟอร์เนียด้วย Random Forest, Flask และ Docker หน้าเว็บ BaanD ให้ทดลองกรอกข้อมูลย่านตัวอย่างและเรียก API ได้ ค่าทำนายใช้หน่วย $100,000 ตามชุดข้อมูล California Housing และเป็นค่าประมาณจากโมเดลเพื่อการศึกษา

## โครงสร้างโฟลเดอร์

```text
ml_service/
├─ app.py
├─ train_model.py
├─ requirements.txt
├─ Dockerfile
├─ .gitignore
├─ README.md
├─ templates/main.html
├─ static/images/         # ภาพประกอบ Hero และการ์ดย่าน
└─ model/                 # สร้าง model.pkl ตอนฝึกโมเดล
```

## เริ่มใช้งานด้วย Python

ใช้ Python 3.15 ให้ตรงกับ Dockerfile:

```powershell
cd ml_service
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python train_model.py
python app.py
```

เปิด `http://127.0.0.1:5000/` สำหรับหน้าเว็บ และ `http://127.0.0.1:5000/health` สำหรับตรวจสถานะ ครั้งแรกที่ฝึกโมเดล scikit-learn จะดาวน์โหลด California Housing dataset จึงต้องเชื่อมต่ออินเทอร์เน็ต

## Build และรันด้วย Docker

```powershell
cd ml_service
docker build -t ds-ml-service .
docker run --rm -p 5000:5000 ds-ml-service
```

Dockerfile ฝึกโมเดลระหว่าง build image แล้วเปิดบริการผ่าน Gunicorn ที่พอร์ต 5000

## API

`GET /health` ส่งคืนสถานะและลำดับฟีเจอร์ ตัวอย่าง:

```json
{"ok":true,"features":["MedInc","HouseAge","AveRooms","AveBedrms","Population","AveOccup","Latitude","Longitude"]}
```

`POST /predict` รับ JSON ที่มีตัวเลข 8 ค่า เรียงตามลำดับข้างต้น:

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:5000/predict -Method Post -ContentType "application/json" -Body '{"features":[8.3,25.0,6.0,1.0,1200,3.0,34.2,-118.3]}'
```

ผลลัพธ์มีรูปแบบ `{"prediction":4.03}` โดยประมาณ หรือราว $403,000 ตัวเลขจริงขึ้นกับผลการฝึกและเวอร์ชันไลบรารี หากข้อมูลไม่ครบหรือมีค่าที่ไม่ใช่ตัวเลข API ตอบ HTTP 400 พร้อม `error`

## หน้าเว็บและภาพหน้าจอ

หน้าแรกมีตัวอย่างย่าน, ฟอร์ม 8 ฟีเจอร์, สถานะกำลังทำนาย, ผลลัพธ์เป็นดอลลาร์ และตัวอย่างคำสั่ง API/Docker ภาพหน้าจอสำหรับแนบรายงานให้ถ่ายจากหน้าเว็บหลังรันบริการและกดทำนายสำเร็จ

## ปัญหาที่พบบ่อย

- `TemplateNotFound`: ตรวจว่าไฟล์อยู่ที่ `templates/main.html`
- ไม่พบ `model/model.pkl`: รัน `python train_model.py` ก่อนเปิดแอป (Docker ฝึกให้ระหว่าง build)
- ดาวน์โหลด dataset ไม่ได้: ตรวจอินเทอร์เน็ตและลองรัน `python train_model.py` อีกครั้ง
- `gunicorn` ไม่พบ: ติดตั้ง dependencies จาก `requirements.txt` ใหม่
- พอร์ต 5000 ถูกใช้: เปลี่ยนการแมปพอร์ต เช่น `docker run --rm -p 8080:5000 ds-ml-service` แล้วเข้า `http://127.0.0.1:8080/`
- PowerShell ปิดกั้นการ activate venv: ใช้ `python -m pip install -r requirements.txt` โดยไม่ activate หรือปรับ execution policy ตามนโยบายเครื่อง

## ส่งงาน

หลังตรวจหน้าเว็บและ API แล้ว ให้ถ่ายภาพหน้าจอผลทำนาย, push โค้ดขึ้น GitHub และส่งลิงก์ repository ผ่าน Google Form ของรายวิชา

