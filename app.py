import gradio as gr
import json
import datetime

# --- لا يوجد تغيير في كود التصميم أو الـ HTML الخاص بك ---
css_code = """body, .gradio-container {  margin:0;  padding:0;  font-family: "Segoe UI", Tahoma, sans-serif;  background: #f7f9fc;  color: #111;}/* تمنع Gradio من فرض flex column على المكون html بالكامل */.gradio-container > div:first-child {  display: block !important;  width: 100% !important;}/* topbar */.topbar {  display:flex;  align-items:center;  gap:12px;  padding:12px 16px;  position:relative;  z-index:1000;}/* logo + menu button */.left-area { display:flex; align-items:center; gap:8px; min-width:0; }.menu-btn {  font-size:22px;  color:#0078ff;  background: transparent;  border: none;  cursor: pointer;  padding:6px;  border-radius:8px;  display:none;}.site-name {  font-weight:800;  color:#0078ff;  font-size:20px;  white-space:nowrap;}/* search */.search-bar { flex:1; min-width:0; }.search-bar input {  width:100%;  padding:8px 12px;  border-radius:20px;  border:1px solid #d0d7dd;  background: white;  box-shadow: 0 2px 8px rgba(15,30,40,0.03);  font-size:14px;}/* desktop nav */.nav-links { display:flex; gap:14px; align-items:center; }.nav-links a {  color:#111; text-decoration:none; font-weight:600; padding:6px 8px; border-radius:8px;}.nav-links a:hover { color:#0078ff; background: rgba(3,100,170,0.04); }/* side menu */.side-menu {  position: fixed;  top: 56px;  left: 12px;  width: 240px;  max-height: calc(100vh - 80px);  overflow:auto;  background: rgba(255,255,255,0.98);  backdrop-filter: blur(6px);  box-shadow: 0 18px 40px rgba(10,30,50,0.12);  border-radius: 12px;  padding:6px 6px;  z-index: 99999;  opacity: 0;  transform: translateY(-8px) scale(0.995);  pointer-events: none;  transition: opacity .28s ease, transform .28s ease;}.side-menu.visible {  opacity: 1;  transform: translateY(0) scale(1);  pointer-events: auto;}.side-menu a {  display:block;  padding:12px 14px;  color: #111;  text-decoration: none;  border-radius:8px;  font-weight:600;}.side-menu a:hover {  color: #0078ff;  background: rgba(3,100,170,0.04);}/* mobile */@media (max-width: 768px) {  .nav-links { display:none; }  .menu-btn { display:inline-block; }  .search-bar { display:none; }}/* Hero section */.hero {  text-align: center;  margin-top: 50px;  padding: 0 16px;}.hero h1 {  font-size: 36px;  color: #0b2633;  margin-bottom: 12px;}.hero p {  color: #394a52;  max-width: 720px;  margin: 0 auto 24px auto;  font-size: 18px;}.hero button {  position: relative;  overflow: hidden;  background-color: #0078ff;  color: white;  border: none;  padding: 14px 28px;  font-size: 16px;  border-radius: 30px;  cursor: pointer;  transition: background-color 0.3s ease, box-shadow 0.3s ease;}/* نص داخل الزر متحرك */.hero button span {  display: inline-block;  position: relative;  transition: transform 0.8s ease;}/* زر hover */.hero button:hover {  background-color: #005bb5;  box-shadow: 0 0 12px 4px rgba(0,120,255,0.7);}/* fade-in animation */@keyframes fadeIn {  from { opacity: 0; transform: translateY(10px); }  to { opacity: 1; transform: translateY(0); }}.fade-in {  animation: fadeIn 0.6s ease forwards;}/* Features Section */.features-section {  max-width: 900px;  margin: 40px auto 60px auto;  padding: 0 16px;  display: flex;  flex-direction: column;  gap: 48px;}.feature-item {  display: flex;  gap: 32px;  align-items: center;  justify-content: center;  flex-wrap: wrap;}.feature-item img,.feature-item video {  flex: 1 1 400px;  max-width: 480px;  border-radius: 12px;  box-shadow: 0 6px 20px rgba(0,0,0,0.08);}.feature-text {  flex: 1 1 400px;  max-width: 450px;}.feature-text h2 {  font-size: 26px;  color: #0b2633;  margin-bottom: 10px;  font-weight: 700;}.feature-text p {  color: #394a52;  font-size: 16px;  line-height: 1.5;}.feature-item.reverse {  flex-direction: row-reverse;}.support-buttons {  display: flex;  gap: 20px;  justify-content: center;}.support-buttons button {  background-color: #0078ff;  color: white;  border: none;  padding: 14px 32px;  font-size: 16px;  border-radius: 30px;  cursor: pointer;  transition: background-color 0.3s ease, box-shadow 0.3s ease;  box-shadow: 0 4px 10px rgba(0,120,255,0.5);}.support-buttons button:hover {  background-color: #005bb5;  box-shadow: 0 0 18px 6px rgba(0,120,255,0.75);}@media (max-width: 768px) {  .feature-item {    flex-direction: column;  }  .feature-item.reverse {    flex-direction: column;  }  .feature-item img,  .feature-item video,  .feature-text {    max-width: 100%;    flex: unset;  }}"""
html_full = """<div class="topbar">  <div class="left-area">    <button id="menuBtn" class="menu-btn" aria-label="Open menu" onclick="toggleMenu()">☰</button>    <div class="site-name">Às Space</div>  </div>  <div class="search-bar">    <input type="search" placeholder="Search..." aria-label="Search">  </div>  <div class="nav-links">    <a href="#">Home</a>    <a href="#">Sections</a>    <a href="#">My Account</a>  </div></div><nav id="sideMenu" class="side-menu" aria-hidden="true">  <a href="#" onclick="menuNavClick(event, 'home')">Home</a>  <a href="#" onclick="menuNavClick(event, 'sections')">Sections</a>  <a href="#" onclick="menuNavClick(event, 'image')">Image Generation</a>  <a href="#" onclick="menuNavClick(event, 'video')">Video Generation</a>  <a href="#" onclick="menuNavClick(event, 'support')">Support & Contact</a></nav><div class="hero">  <h1 id="mainTitle" style="opacity:0;">Welcome to Às Space</h1>  <p id="mainDesc" style="opacity:0;">Discover great AI tools that help you create, learn and grow. Mobile-first friendly design.</p>  <button id="ctaBtn"><span>Start Exploring</span></button></div><section class="features-section">  <div class="feature-item">    <img src="https://media.assettype.com/analyticsinsight/2024-07/c3ab0b8f-73cc-4245-a2a2-f78148c0077f/Top-10-Best-Free-AI-Image-Generator.jpg?w=1200&h=675&auto=format%2Ccompress&fit=max&enlarge=true" alt="AI Tools" />    <div class="feature-text">      <h2>Find the AI tool you need</h2>      <p>Discover and explore powerful AI tools tailored for your needs. Easily accessible and designed for productivity.</p>    </div>  </div>  <div class="feature-item reverse">    <video src="https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.webm" autoplay muted loop playsinline></video>    <div class="feature-text">      <h2>Explore Our Features</h2>      <p>Watch this quick video to see how you can navigate and utilize different sections of the app efficiently.</p>    </div>  </div>  <div class="support-buttons">    <button>Contact Us</button>    <button>Get Support</button>  </div></section><script>(function(){  const menu = document.getElementById('sideMenu');  const btn  = document.getElementById('menuBtn');  let timer = null;  window.toggleMenu = function(){    if(!menu) return;    if(menu.classList.contains('visible')){      hideMenu();    } else {      showMenu();    }  }  function showMenu(){    if(!menu) return;    menu.classList.add('visible');    menu.setAttribute('aria-hidden','false');    if(timer) { clearTimeout(timer); timer = null; }    timer = setTimeout(hideMenu, 12000);  }  function hideMenu(){    if(!menu) return;    menu.classList.remove('visible');    menu.setAttribute('aria-hidden','true');    if(timer) { clearTimeout(timer); timer = null; }  }  document.addEventListener('click', function(e){    if(!menu.classList.contains('visible')) return;    const isInsideMenu = menu.contains(e.target);    const isBtn = btn.contains(e.target);    if(!isInsideMenu && !isBtn){      hideMenu();    }  }, true);  document.addEventListener('keydown', function(e){    if(e.key === 'Escape') hideMenu();  });  window.hideSideMenu = hideMenu;  window.menuNavClick = function(ev, target){    ev.preventDefault();    hideMenu();    console.log("navigate to:", target);  }  // Animation for title and description fade-in  window.addEventListener('DOMContentLoaded', () => {    const title = document.getElementById('mainTitle');    const desc = document.getElementById('mainDesc');    const btn = document.getElementById('ctaBtn');    const btnText = btn.querySelector('span');    title.classList.add('fade-in');    setTimeout(() => {      desc.classList.add('fade-in');    }, 400);    btn.classList.add('fade-in');    btn.addEventListener('click', () => {      btnText.style.transform = 'translateX(-150%)';      setTimeout(() => {        btnText.style.transition = 'none';        btnText.style.transform = 'translateX(150%)';        requestAnimationFrame(() => {          btnText.style.transition = 'transform 0.8s ease';          btnText.style.transform = 'translateX(0)';        });      }, 1500);    });  });})();</script>"""

# +++ الجزء الجديد الذي أضفناه +++
# هذه الدالة هي التي ستحفظ البلاغ في ملف
def handle_report(report_json_string):
    try:
        # تحويل النص (JSON) القادم من الواجهة الأمامية إلى قاموس بايثون
        report_data = json.loads(report_json_string)
        
        # إضافة وقت وتاريخ استلام البلاغ
        report_data['received_at'] = datetime.datetime.now().isoformat()
        
        print("تم استلام بلاغ جديد:", report_data)

        # حفظ البلاغ في ملف نصي
        with open("reports.txt", "a", encoding="utf-8") as f:
            f.write(json.dumps(report_data, ensure_ascii=False) + "\n")
        
        return "Success" # إرجاع رسالة نجاح
    except Exception as e:
        print("حدث خطأ أثناء معالجة البلاغ:", e)
        return "Error" # إرجاع رسالة خطأ

# --- نهاية الجزء الجديد ---

with gr.Blocks(css=css_code) as demo:
    # الواجهة الرئيسية التي يراها المستخدم
    gr.HTML(html_full)
    
    # +++ المكونات المخفية التي تعمل كجسر بين الواجهة الأمامية والخلفية +++
    with gr.Row(visible=False):
        # صندوق نص مخفي لاستقبال بيانات البلاغ من الجافاسكريبت
        report_data_input = gr.Textbox(elem_id="report_data_input")
        # زر مخفي لتشغيل دالة الحفظ في البايثون
        submit_report_button = gr.Button(elem_id="submit_report_button")
        # صندوق نص مخفي لاستقبال نتيجة العملية (نجاح أو فشل)
        report_status_output = gr.Textbox(elem_id="report_status_output")

    # ربط الزر المخفي بالدالة. عندما يتم النقر عليه، يأخذ القيمة من صندوق النص ويرسلها للدالة
    submit_report_button.click(
        fn=handle_report, 
        inputs=[report_data_input], 
        outputs=[report_status_output]
    )
    # --- نهاية المكونات المخفية ---

if __name__ == "__main__":
    demo.launch(share=True)