import streamlit as st
from docxtpl import DocxTemplate
import io

# 1. กำหนดหัวข้อหน้าเว็บ
st.title("📝 โปรแกรมสร้างใบขอสั่งซื้อสินค้า")

# 2. สร้างช่องให้กรอกข้อมูล
name = st.text_input("ชื่อผู้สั่งซื้อ")
item = st.text_input("ชื่อสินค้าที่ต้องการ")
amount = st.text_input("จำนวน (ชิ้น)")

# 3. สร้างปุ่มกด
if st.button("สร้างเอกสาร"):
    # เช็คว่ากรอกข้อมูลครบหรือยัง
    if name != "" and item != "" and amount != "":
        
        # 4. เรียกไฟล์ Word ต้นแบบมาใช้งาน
        doc = DocxTemplate("template.docx")
        
        # 5. เอาข้อมูลที่กรอกบนเว็บ ไปจับคู่กับคำในวงเล็บ {{ }} ในไฟล์ Word
        context = {
            "name": name,
            "item": item,
            "amount": amount
        }
        
        # สั่งให้แทนที่คำ
        doc.render(context)
        
        # 6. เตรียมไฟล์ที่เสร็จแล้วให้พร้อมดาวน์โหลด
        bio = io.BytesIO()
        doc.save(bio)
        
        # 7. แสดงปุ่มให้ดาวน์โหลดไปที่เครื่อง
        st.success("สร้างเอกสารสำเร็จ! กดดาวน์โหลดด้านล่างได้เลยครับ")
        st.download_button(
            label="📥 ดาวน์โหลดไฟล์ Word",
            data=bio.getvalue(),
            file_name=f"ใบสั่งซื้อ_{name}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    else:
        st.warning("⚠️ กรุณากรอกข้อมูลให้ครบถ้วนก่อนกดสร้างเอกสาร")