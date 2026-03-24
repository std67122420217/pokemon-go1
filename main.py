import os  # <--- ต้องมีบรรทัดนี้ด้วยครับ!
from pokemon import create_app

app = create_app()

if __name__ == '__main__':
    # ดึงค่า Port จากระบบ (Render จะส่งมาให้) ถ้าไม่มีให้ใช้ 5000 (รันในเครื่องเรา)
    port = int(os.environ.get("PORT", 5000))
    
    # รันแค่บรรทัดเดียวพอครับ โดยตั้งค่าให้รองรับทั้งในเครื่องและบน Render
    app.run(host='0.0.0.0', port=port, debug=True)