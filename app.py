import streamlit as st
from docxtpl import DocxTemplate
import io

# ตั้งค่าหน้าเพจ
st.set_page_config(page_title="ระบบสั่งซื้อแบบย่อ", page_icon="📝")

# หัวข้อโปรแกรม
st.markdown("### 📝 ระบบออกใบขอสั่งซื้อ (ฉบับย่อ)")
st.markdown("---")

# หัวข้อที่ 1: ใครคนสั่ง
st.markdown("#### 👤 1. ข้อมูลผู้สั่งซื้อ")
name = st.text_input("ชื่อ-นามสกุล (ผู้ขอสั่งซื้อ)")

# หัวข้อที่ 2: ซื้ออะไร
st.markdown("#### 📦 2. รายละเอียดสินค้า")
item = st.text_area("รายการสินค้าที่ต้องการสั่งซื้อ")

# ปุ่มกดสร้างเอกสาร
st.markdown("---")
if st.button("📄 สร้างเอกสาร"):
    
    # อ่านไฟล์ต้นแบบ
    doc = DocxTemplate("template.docx")
    
    # ข้อมูลที่จะส่งไปหยอดใน Word (เปลี่ยนเป็น name และ item แล้ว)
    context = {
        "name": name,
        "item": item
    }
    
    # สั่งประมวลผล
    doc.render(context)
    
    # แปลงไฟล์เพื่อเตรียมดาวน์โหลด
    bio = io.BytesIO()
    doc.save(bio)
    
    # แสดงปุ่มดาวน์โหลด
    st.success("✅ สร้างเอกสารสำเร็จ! กดดาวน์โหลดด้านล่างได้เลยครับ")
    st.download_button(
        label="⬇️ ดาวน์โหลดไฟล์ Word",
        data=bio.getvalue(),
        file_name="เอกสารสั่งซื้อ.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )