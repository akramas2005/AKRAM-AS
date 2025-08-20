# app.py

# استيراد المكتبات اللازمة من فلاسك لمعالجة الطلبات والملفات
from flask import Flask, request, jsonify, send_from_directory
import json
import datetime
import os

# هذا السطر يقوم بإنشاء الخادم وتحديد أن الملفات الثابتة (مثل index.html) موجودة في نفس المجلد
app = Flask(__name__, static_url_path='', static_folder='.')

# هذا هو الرابط الذي سيستقبل البلاغات. لن يعمل إلا مع طلبات POST
@app.route('/api/report', methods=['POST'])
def handle_report():
    report_data = request.json  # الحصول على بيانات البلاغ التي أرسلها الجافاسكريبت

    # إضافة وقت وتاريخ استلام البلاغ لتوثيقه
    report_data['received_at'] = datetime.datetime.now().isoformat()
    
    # لغرض المتابعة، سنطبع البلاغ في سجلات التشغيل (Logs) الخاصة بالـ Space
    print("تم استلام بلاغ جديد:", report_data)

    # الأهم: حفظ البلاغ في ملف نصي. "a" تعني إضافة سطر جديد في كل مرة
    try:
        with open("reports.txt", "a", encoding="utf-8") as f:
            f.write(json.dumps(report_data, ensure_ascii=False) + "\n")
    except Exception as e:
        print("حدث خطأ أثناء حفظ البلاغ:", e)
        # في حالة حدوث خطأ، يتم إرسال رد خطأ
        return jsonify({"status": "error", "message": "لا يمكن حفظ البلاغ"}), 500

    # إرسال رد بنجاح العملية إلى متصفح المستخدم
    return jsonify({"status": "success", "message": "تم استلام البلاغ بنجاح"})

# هذا الجزء ضروري لعرض ملف الـ HTML الرئيسي الخاص بك عندما يزور شخص ما رابط الـ Space
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')