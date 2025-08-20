from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
import gradio as gr
import json
import datetime

# الخطوة 1: إنشاء تطبيق FastAPI الرئيسي (هذا هو الخادم الأساسي)
app = FastAPI()

# --------------------------------------------------------------------------
# الجزء الخاص بواجهة Gradio (سيعمل في الخلفية الآن)
with gr.Blocks(theme=gr.themes.Default(primary_hue="blue")) as demo:
    # سنترك هذا الجزء فارغًا تقريبًا
    # لأننا سنعرض ملف HTML الرئيسي باستخدام FastAPI
    # لكننا نحتاج لهذه المكونات المخفية لتعمل ميزة الإبلاغ
    with gr.Row(visible=False):
        report_data_input = gr.Textbox(elem_id="report_data_input")
        submit_report_button = gr.Button(elem_id="submit_report_button")
        report_status_output = gr.Textbox(elem_id="report_status_output")

    # دالة بايثون لمعالجة البلاغ عند استدعائها
    def handle_report_function(report_json_string):
        try:
            report_data = json.loads(report_json_string)
            report_data['received_at'] = datetime.datetime.now().isoformat()
            print("تم استلام بلاغ جديد:", report_data)
            with open("reports.txt", "a", encoding="utf-8") as f:
                f.write(json.dumps(report_data, ensure_ascii=False) + "\n")
            return "Success"
        except Exception as e:
            print("حدث خطأ أثناء معالجة البلاغ:", e)
            return "Error"

    # ربط الزر المخفي بالدالة
    submit_report_button.click(
        fn=handle_report_function, 
        inputs=[report_data_input], 
        outputs=[report_status_output]
    )
# نهاية الجزء الخاص بـ Gradio
# --------------------------------------------------------------------------

# الخطوة 2: دمج واجهة Gradio مع تطبيق FastAPI ولكن على رابط فرعي
# هذا يسمح لميزات Gradio (مثل استقبال البلاغات) بالعمل في الخلفية
app = gr.mount_gradio_app(app, demo, path="/gradio")

# الخطوة 3: إنشاء رابط API لاستقبال البلاغات (هذا ليس ضرورياً مع الطريقة الجديدة ولكنه جيد كاحتياط)
# @app.post("/api/report") ... (يمكننا تجاهل هذا حاليًا لأننا نستخدم طريقة Gradio المخفية)


# الخطوة 4: (الأهم) إنشاء رابط لعرض ملف index.html الرئيسي
# هذا السطر يخبر الخادم: "عندما يطلب أي شخص الصفحة الرئيسية، قم بقراءة ملف index.html وإرساله له"
@app.get("/")
def read_index():
    return FileResponse("index.html")