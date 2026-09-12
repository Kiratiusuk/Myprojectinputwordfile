import streamlit as st
from docxtpl import DocxTemplate
import io
import datetime

# 1. ตั้งค่าหน้าเพจให้ดูเป็นทางการ
st.set_page_config(page_title="ระบบออกใบสั่งซื้อ", page_icon="📝", layout="centered")

# 2. หัวข้อโปรแกรม
st.title("📝 ระบบออกใบขอสั่งซื้อพัสดุ/เวชภัณฑ์")
st.markdown("กรุณากรอกรายละเอียดด้านล่างให้ครบถ้วน เพื่อสร้างเอกสารใบขอสั่งซื้อ (Purchase Order)")
st.markdown("---")

# 3. ส่วนที่ 1: ข้อมูลการสั่งซื้อ (แบ่ง 2 คอลัมน์)
st.subheader("📌 1. ข้อมูลทั่วไป")
col1, col2 = st.columns(2)

with col1:
    po_number = st.text_input("เลขที่เอกสาร (PO No.)", placeholder="เช่น PO-671001")
    requester = st.text_input("ชื่อผู้ขอซื้อ")

with col2:
    po_date = st.date_input("วันที่ขอสั่งซื้อ", datetime.date.today())
    department = st.selectbox("แผนก/หน่วยงาน", ["แผนกจิตเวชและยาเสพติด", "เภสัชกรรม", "พัสดุ", "อื่นๆ"])

# 4. ส่วนที่ 2: รายละเอียดสินค้า (แบ่ง 3 คอลัมน์)
st.markdown("---")
st.subheader("📦 2. รายละเอียดสินค้า")
col3, col4, col5 = st.columns([2, 1, 1]) # แบ่งสัดส่วนความกว้างคอลัมน์

with col3:
    item_name = st.text_input("รายการสินค้า / เวชภัณฑ์")
with col4:
    quantity = st.number_input("จำนวน", min_value=1, value=1)
with col5:
    unit_price = st.number_input("ราคา/หน่วย (บาท)", min_value=0.0, value=100.0, step=10.0)

# คำนวณราคารวมอัตโนมัติ
total_price = quantity * unit_price
st.info(f"💰 **ราคารวมทั้งสิ้น:** {total_price:,.2f} บาท")

remark = st.text_area("หมายเหตุ / เหตุผลการขอซื้อ", height=100)

# 5. ปุ่มกดสร้างเอกสาร
st.markdown("---")
if st.button("📄 สร้างเอกสารใบขอสั่งซื้อ", type="primary", use_container_width=True):
    
    doc = DocxTemplate("template.docx")
    
    # ข้อมูลที่จะส่งไปหยอดในไฟล์ Word
    context = {
        "po_number": po_number,
        "date": po_date.strftime("%d/%m/%Y"),
        "requester": requester,
        "department": department,
        "item_name": item_name,
        "quantity": quantity,
        "unit_price": f"{unit_price:,.2f}",
        "total_price": f"{total_price:,.2f}",
        "remark": remark
    }
    
    doc.render(context)
    
    bio = io.BytesIO()
    doc.save(bio)
    
    st.success("✅ สร้างเอกสารสำเร็จ! กดปุ่มด้านล่างเพื่อดาวน์โหลดได้เลยครับ")
    st.download_button(
        label="⬇️ ดาวน์โหลดไฟล์ Word",
        data=bio.getvalue(),
        file_name=f"PO_{po_number}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        type="secondary"
    )