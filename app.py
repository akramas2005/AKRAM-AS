import gradio as gr
import json
import datetime
import os

# ==============================================================================
# النسخة الكاملة والنهائية لواجهة الشات مدمجة هنا
# ==============================================================================
html_full = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Às Space - AI Tools (Study Assistant slice)</title>
<style>
  :root { --kbd: 0px; --accent:#0078ff; --bg:#f7f9fc; --muted:#7b8a93; --danger:#ff4d4f; }

  body {
    margin:0; padding:0; font-family: "Segoe UI", Tahoma, sans-serif; background: var(--bg); color: #111;
  }
  .wrap{max-width:980px; margin:18px auto; padding:12px;}
  header.appbar{display:flex; align-items:center; gap:12px; padding:10px 6px;}
  .site-name{font-weight:800; color:var(--accent); font-size:20px;}
  .lead{color:var(--muted); margin:6px 0 18px 0; font-size:14px;}

  .sections-grid{display:flex; flex-direction:column; gap:20px; align-items:center;}
  .card {
    width: min(420px, 94%);
    height: calc(85vh - 120px);
    max-height:760px;
    border-radius: var(--card-radius);
    overflow:hidden;
    position:relative;
    background: linear-gradient(180deg, rgba(0,0,0,0.12), rgba(0,0,0,0.06)), url('https://images.unsplash.com/photo-1518972559570-7cc1309f6f3b?q=80&w=1400&auto=format&fit=crop&ixlib=rb-4.0.3&s=bd14a4a2b5bf327c3b6f6e8fc4c6b3b7') center/cover no-repeat;
    box-shadow: 0 18px 50px rgba(6,30,60,0.12);
    display:flex;
    flex-direction:column;
    transition: transform .18s ease, box-shadow .18s ease;
    transform-origin: center top;
    -webkit-font-smoothing:antialiased;
    -moz-osx-font-smoothing:grayscale;
  }

  @media (hover: hover) and (pointer: fine) {
    .card:hover {
      transform: scale(1.03);
      box-shadow: 0 30px 80px rgba(6,30,60,0.18);
    }
  }

  .card .overlay{
    flex:1; display:flex; flex-direction:column; justify-content:space-between; padding:20px;
    background: linear-gradient(to top, rgba(0,0,0,0.45), rgba(0,0,0,0.12) 45%, rgba(0,0,0,0.03) 80%);
    color: #fff;
    position:relative;
    z-index:1;
  }

  .card h3{margin:0; font-size:22px; font-weight:800; text-shadow:0 4px 18px rgba(0,0,0,0.35);}
  .card p{margin:8px 0 0; font-size:15px; color:rgba(255,255,255,0.95);}
  .card .meta-row{display:flex; justify-content:space-between; align-items:end; gap:10px;}
  .chat-btn{
    background: linear-gradient(90deg,var(--accent),#00aaff);
    border:none; color:white; padding:12px 16px; font-weight:800; border-radius:999px;
    box-shadow: 0 8px 24px rgba(0,120,255,0.18);
    cursor:pointer; transition: transform .18s ease, box-shadow .18s ease, opacity .12s;
  }
  .chat-btn:active{ transform:translateY(1px) scale(.997); }

  .chat-panel{
    position:fixed; inset:0; z-index:11000; display:flex; flex-direction:column;
    padding:12px; background:linear-gradient(180deg, rgba(12,18,24,0.42), rgba(12,18,24,0.55));
    backdrop-filter: blur(8px) saturate(1.02);
    opacity:0; 
    pointer-events:none;
    transform: translateY(6px);
    will-change: opacity, transform;
    visibility: hidden;
    transition: opacity .28s cubic-bezier(.2,.9,.25,1), transform .28s cubic-bezier(.2,.9,.25,1), visibility 0s .3s;
    align-items: center;
    justify-content: flex-end;
  }
  .chat-panel.show{ 
    opacity:1; 
    pointer-events:auto; 
    transform: translateY(0);
    visibility: visible;
    transition: opacity .28s cubic-bezier(.2,.9,.25,1), transform .28s cubic-bezier(.2,.9,.25,1), visibility 0s;
  }

  .chat-shell{
    width: min(950px, 98%);
    max-width:970px;
    height: calc(92vh);
    background: linear-gradient(180deg, rgba(255,255,255,0.98), rgba(255,255,255,0.96));
    border-radius:16px; overflow:hidden; box-shadow: 0 30px 80px rgba(6,30,60,0.18);
    display:flex; flex-direction:column;
    position:relative;
    margin: 0 0 20px 0;
  }
  
  .chat-header{display:flex; gap:12px; align-items:center; padding:12px 16px; border-bottom:1px solid #eef3f7;}
  .back-btn{border: none; background:transparent; font-size:18px; cursor:pointer; padding:8px; border-radius:8px;}
  .persona-name{font-weight:800; font-size:16px; color:#0b2633;}
  .persona-desc{color:var(--muted); font-size:13px;}

  .messages{flex:1; overflow:auto; padding:18px; display:flex; flex-direction:column; gap:10px;}
  .msg {
    max-width: min(86%, 680px);
    padding:10px 12px;
    border-radius:12px; line-height:1.35; font-size:14px; box-shadow: 0 6px 18px rgba(6,30,60,0.04);
    word-wrap: break-word;
    position: relative;
    will-change: transform, opacity, height, padding, width, margin;
    opacity:0; transform: translateY(8px);
    transition: opacity 0.4s ease, transform 0.4s ease, height 0.35s ease, padding 0.35s ease, width 0.35s ease, margin 0.35s ease;
  }
  .msg.show{ opacity:1; transform:translateY(0); }
  .msg.user{ align-self:flex-end; background:linear-gradient(90deg,var(--accent),#00aaff); color:white;}
  .msg.assistant{ align-self:flex-start; background: #fff; color:#0b2633;}

  .msg .bubble { overflow: hidden; }
  .bubble-content { transition: opacity .3s ease; }

  .msg-actions{ display:flex; align-items:center; gap:6px; margin-top:6px; opacity:.95; }
  .msg-actions .act-btn {
    width:26px; height:26px; display:inline-flex; align-items:center; justify-content:center;
    border:none; background:transparent; border-radius:6px; cursor:pointer;
    transition: all .2s ease;
  }
  .msg-actions .act-btn svg { transition: all .2s ease; }
  .msg-actions .act-btn:hover { transform: scale(1.1); }
  .msg-actions .act-btn[data-active="true"] { background: rgba(0,120,255,0.08); }
  .msg-actions .divider{ width:1px; height:14px; background:#e8eef3; margin:0 4px; }
  
  .feedback-row{ margin-top:6px; display:none; flex-direction:column; gap:6px; width:100%;}
  .feedback-input{ width:100%; padding:8px 10px; border:1px solid #e6ecf3; border-radius:8px; font-size:13px; box-sizing:border-box;}
  .feedback-actions{ display:flex; gap:8px; justify-content:flex-end; }
  .mini-btn{ padding:6px 10px; border:none; border-radius:8px; font-weight:700; cursor:pointer; font-size:12px; }
  .mini-btn.send{ background: var(--accent); color:#fff; }
  .mini-btn.cancel{ background:#f0f4f8; }

  /* --- NEW CSS FOR ANIMATIONS --- */
  .msg-actions .act-btn.pop-animation { animation: pop 0.4s cubic-bezier(.18, .89, .32, 1.28); }
  @keyframes pop {
    0% { transform: scale(1); }
    50% { transform: scale(1.4); }
    100% { transform: scale(1); }
  }
  
  .msg.fading-out {
    opacity: 0 !important;
    transform: translateY(-10px) scale(0.95) !important;
    height: 0 !important;
    padding-top: 0 !important;
    padding-bottom: 0 !important;
    margin-top: -10px !important;
    margin-bottom: 0 !important;
    z-index: -1;
  }

  .bubble-content.fading-out { opacity: 0; }
  
  .msg.shrinking {
    width: 60px !important;
    min-height: 38px !important;
    height: 38px !important;
    padding: 8px !important;
    border-radius: 999px !important;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .typing .dots{ display:inline-flex; gap:6px; align-items:center; }
  .typing .dot{ width:8px; height:8px; border-radius:50%; background:#cbd8e3; opacity:.4; transform: translateY(0); animation: tip 900ms infinite ease-in-out; }
  .typing .dot:nth-child(2){ animation-delay:120ms; }
  .typing .dot:nth-child(3){ animation-delay:240ms; }
  @keyframes tip {
    0% { transform: translateY(0); opacity:.35; }
    50% { transform: translateY(-6px); opacity:1; }
    100% { transform: translateY(0); opacity:.35; }
  }
  /* --- END NEW CSS --- */
</style>
</head>
<body>
  <div class="wrap">
    <main class="sections-grid" role="main">
      <article class="card" id="studyCard">
        <div class="overlay">
          <div>
            <h3>Study Assistant</h3>
            <p>Smart study companion: summaries, explanations, quizzes and personalized study plans.</p>
          </div>
          <div class="meta-row">
            <div style="font-size:13px; opacity:.95">Last update • persona tuned</div>
            <button class="chat-btn" id="openChatBtn">Chat Now</button>
          </div>
        </div>
      </article>
    </main>
  </div>
  
  <div class="chat-panel" id="chatPanel">
    <div class="chat-shell">
        <div class="chat-header">
            </div>
        <div class="messages" id="messages"></div>
        <div class="composer">
            <textarea id="composerInput" placeholder="Ask something..."></textarea>
            <button id="sendBtn">Send</button>
        </div>
    </div>
  </div>

<script>
(function() {
    const messagesEl = document.getElementById('messages');
    const openChatBtn = document.getElementById('openChatBtn');
    const chatPanel = document.getElementById('chatPanel');
    const composer = document.getElementById('composerInput');
    const sendBtn = document.getElementById('sendBtn');
    
    // Fallback for elements that might not exist in the simplified HTML
    const backBtn = document.getElementById('backBtn');
    const editCancelBtn = document.getElementById('editCancelBtn');

    let messages = [];
    let editIndex = null;
    let pendingAttachment = null; // Assuming no attachments for this simplified version

    function genId(){ return 'm-'+Math.random().toString(36).slice(2,9); }
    function escapeHtml(str){ if(!str) return ''; return String(str).replace(/[&<>"]/g, s => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[s])); }
    function toast(msg, duration=1900){ console.log(`Toast: ${msg}`); }
    function saveSession(){ console.log("Session saved."); }
    function updateSendVisibility(){}
    function autoGrowTextarea(){}
    function startRotatorIfNeeded(){}
    function findPrevUserIndex(idx) {
        for(let i = idx - 1; i >= 0; i--) {
            if(messages[i].role === 'user') return i;
        }
        return -1;
    }
    
    function simulatedAssistantReply(prompt) {
        return "This is a new, smart, and insightful response to your query about: '" + (prompt || "your last message") + "'.";
    }

    function createMessageElement(m, idx) {
        const div = document.createElement('div');
        div.className = 'msg ' + (m.role === 'user' ? 'user' : 'assistant');
        div.dataset.index = idx;
        div.dataset.id = m.id;

        const bubble = document.createElement('div');
        bubble.className = 'bubble';
        
        const bubbleContent = document.createElement('div');
        bubbleContent.className = 'bubble-content';
        bubbleContent.innerHTML = escapeHtml(m.content).replace(/\n/g, '<br>');
        
        bubble.appendChild(bubbleContent);

        if (m.role === 'assistant') {
            const actions = document.createElement('div');
            actions.className = 'msg-actions';
            const meta = m.meta || {};
            actions.innerHTML = `
                <button class="act-btn" data-act="regen" title="Regenerate"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#0b2633" stroke-width="2"><path d="M21 12a9 9 0 1 1-3-6.7"/><polyline points="21 3 21 9 15 9"/></svg></button>
                <span class="divider"></span>
                <button class="act-btn" data-act="like" title="Like" data-active="${!!meta.liked}"><svg width="16" height="16" viewBox="0 0 24 24" stroke-width="2" stroke="${!!meta.liked ? 'var(--accent)' : '#0b2633'}" fill="${!!meta.liked ? 'var(--accent)' : 'none'}"><path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3"></path></svg></button>
                <button class="act-btn" data-act="dislike" title="Dislike" data-active="${!!meta.disliked}"><svg width="16" height="16" viewBox="0 0 24 24" stroke-width="2" stroke="${!!meta.disliked ? 'var(--danger)' : '#0b2633'}" fill="${!!meta.disliked ? 'var(--danger)' : 'none'}"><path d="M10 15v4a3 3 0 0 0 3 3l4-9V2H5.72a2 2 0 0 0-2 1.7l-1.38 9a2 2 0 0 0 2 2.3zM17 2h3a2 2 0 0 1 2 2v7a2 2 0 0 1-2 2h-3"></path></svg></button>
            `;
            const feedbackRow = document.createElement('div');
            feedbackRow.className = 'feedback-row';
            feedbackRow.innerHTML = `
              <input class="feedback-input" type="text" placeholder="Tell us why..." value="${escapeHtml(meta.feedback || '')}">
              <div class="feedback-actions">
                <button class="mini-btn send" data-act="sendFeedback">Send</button>
                <button class="mini-btn cancel" data-act="cancelFeedback">Cancel</button>
              </div>
            `;
            if(meta.awaitingFeedback) feedbackRow.style.display = 'flex';
            
            bubble.appendChild(actions);
            bubble.appendChild(feedbackRow);
        }
        div.appendChild(bubble);
        return div;
    }

    function appendMessage(m, idx) {
        const messageEl = createMessageElement(m, idx);
        messagesEl.appendChild(messageEl);
        requestAnimationFrame(() => {
            setTimeout(() => {
                messageEl.classList.add('show');
            }, 20);
        });
        messagesEl.scrollTop = messagesEl.scrollHeight;
        return messageEl;
    }
    
    function showTypingIndicator() {
        const typingEl = document.createElement('div');
        typingEl.className = 'msg assistant typing show';
        typingEl.dataset.typing = 'true';
        typingEl.innerHTML = '<div class="dots"><span class="dot"></span><span class="dot"></span><span class="dot"></span></div>';
        messagesEl.appendChild(typingEl);
        messagesEl.scrollTop = messagesEl.scrollHeight;
        return typingEl;
    }

    function sendMessage() {
        const text = composer.value.trim();
        if (!text) return;
        
        const userMessage = {id: genId(), role: 'user', content: text};
        messages.push(userMessage);
        appendMessage(userMessage, messages.length - 1);
        
        composer.value = '';

        const typingEl = showTypingIndicator();

        setTimeout(() => {
            typingEl.remove();
            const replyText = simulatedAssistantReply(text);
            const assistantMessage = {id: genId(), role: 'assistant', content: replyText, meta: {}};
            messages.push(assistantMessage);
            appendMessage(assistantMessage, messages.length - 1);
        }, 1500);
    }
    
    function handleEditAndResend(editedIndex, newContent) {
        const editedMsgId = messages[editedIndex].id;
        messages[editedIndex].content = newContent;
        
        const userMsgEl = messagesEl.querySelector(`.msg[data-id="${editedMsgId}"]`);
        if (userMsgEl) {
            const bubbleContent = userMsgEl.querySelector('.bubble-content');
            if (bubbleContent) bubbleContent.innerHTML = escapeHtml(newContent).replace(/\n/g, '<br>');
        }

        const subsequentMessageElements = Array.from(messagesEl.querySelectorAll('.msg')).filter(m => parseInt(m.dataset.index, 10) > editedIndex);
        subsequentMessageElements.forEach((m, i) => {
            setTimeout(() => {
                m.classList.add('fading-out');
                m.addEventListener('transitionend', () => m.remove(), { once: true });
            }, i * 80);
        });
        messages.splice(editedIndex + 1);

        const typingEl = showTypingIndicator();
        
        setTimeout(() => {
            typingEl.remove();
            const newReplyText = simulatedAssistantReply(newContent);
            const newAssistantMessage = {id: genId(), role: 'assistant', content: newReplyText, meta: {}};
            messages.push(newAssistantMessage);
            appendMessage(newAssistantMessage, messages.length - 1);
        }, 2000);
    }

    messagesEl.addEventListener('click', async (e) => {
        const el = e.target.closest('button[data-act]');
        if (!el) return;

        const container = el.closest('.msg');
        if (!container) return;

        const idx = Number(container.dataset.index);
        let msg = messages[idx];
        if (!msg) return;

        const act = el.dataset.act;
        el.classList.add('pop-animation');
        el.addEventListener('animationend', () => el.classList.remove('pop-animation'), { once: true });

        if (act === 'like' || act === 'dislike') {
            msg.meta = msg.meta || {};
            if (act === 'like') {
                msg.meta.liked = !msg.meta.liked;
                msg.meta.disliked = false;
            } else {
                msg.meta.disliked = !msg.meta.disliked;
                msg.meta.liked = false;
            }
            msg.meta.awaitingFeedback = act === 'dislike' && msg.meta.disliked;
            
            const likeBtn = container.querySelector('[data-act="like"]');
            const dislikeBtn = container.querySelector('[data-act="dislike"]');
            const likeSvg = likeBtn.querySelector('svg');
            const dislikeSvg = dislikeBtn.querySelector('svg');
            const feedbackRow = container.querySelector('.feedback-row');

            likeBtn.dataset.active = msg.meta.liked;
            likeSvg.style.stroke = msg.meta.liked ? 'var(--accent)' : '#0b2633';
            likeSvg.style.fill = msg.meta.liked ? 'var(--accent)' : 'none';
            
            dislikeBtn.dataset.active = msg.meta.disliked;
            dislikeSvg.style.stroke = msg.meta.disliked ? 'var(--danger)' : '#0b2633';
            dislikeSvg.style.fill = msg.meta.disliked ? 'var(--danger)' : 'none';

            if(feedbackRow) feedbackRow.style.display = msg.meta.awaitingFeedback ? 'flex' : 'none';
            saveSession();

        } else if (act === 'regen') {
            const userPromptMsg = messages.slice(0, idx).reverse().find(m => m.role === 'user');
            
            const subsequentMessageElements = Array.from(messagesEl.querySelectorAll('.msg')).filter(m => parseInt(m.dataset.index, 10) > idx);
            subsequentMessageElements.forEach((m, i) => {
                setTimeout(() => m.classList.add('fading-out'), i * 80);
            });
            
            setTimeout(() => {
                 messages.splice(idx + 1);
                 subsequentMessageElements.forEach(m => m.remove());
            }, subsequentMessageElements.length * 80 + 400);

            const bubbleContent = container.querySelector('.bubble-content');
            bubbleContent.classList.add('fading-out');

            setTimeout(() => {
                bubbleContent.innerHTML = '';
                container.classList.add('shrinking');
                
                setTimeout(() => {
                    bubbleContent.innerHTML = '<div class="dots typing"><span class="dot"></span><span class="dot"></span><span class="dot"></span></div>';
                    bubbleContent.classList.remove('fading-out');
                }, 350);
            }, 300);
            
            setTimeout(() => {
                msg.content = simulatedAssistantReply(userPromptMsg?.content);
                msg.meta = {};
                
                const newMsgEl = createMessageElement(msg, idx);
                bubbleContent.classList.add('fading-out');
                
                setTimeout(() => {
                    container.classList.remove('shrinking');
                    container.innerHTML = newMsgEl.innerHTML;
                    messagesEl.scrollTop = messagesEl.scrollHeight;
                    saveSession();
                }, 400);

            }, 2500);

        } else if (act === 'cancelFeedback') {
            msg.meta.awaitingFeedback = false;
            msg.meta.disliked = false;
            container.querySelector('.feedback-row').style.display = 'none';
            const dislikeBtn = container.querySelector('[data-act="dislike"]');
            dislikeBtn.dataset.active = false;
            dislikeBtn.querySelector('svg').style.stroke = '#0b2633';
            dislikeBtn.querySelector('svg').style.fill = 'none';
            saveSession();
        }
    });

    if (openChatBtn) {
        openChatBtn.addEventListener('click', () => {
            chatPanel.classList.add('show');
            if (messages.length === 0) {
                initializeDemo();
            }
        });
    }
    
    if (backBtn) {
        backBtn.addEventListener('click', () => {
            chatPanel.classList.remove('show');
        });
    }
    
    // Check if sendBtn exists before adding listener
    if (sendBtn) {
        sendBtn.addEventListener('click', sendMessage);
    }
    // Check if composer exists before adding listener
    if (composer) {
        composer.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                if(sendBtn) sendBtn.click();
                else if(sendInsideBtn) sendInsideBtn.click();
            }
        });
    }
    
    function initializeDemo() {
        messages = [
            {id: genId(), role: 'user', content: 'Explain photosynthesis.'},
            {id: genId(), role: 'assistant', content: 'Photosynthesis is the process used by plants...', meta: {}},
            {id: genId(), role: 'user', content: 'Thanks!'},
        ];
        messagesEl.innerHTML = '';
        messages.forEach((msg, idx) => {
            appendMessage(msg, idx);
        });
    }
    
    // Ensure the script only initializes the demo if the button is clicked, not on page load
    // initializeDemo();

})();
</script>
</body>
</html>
"""

# ==============================================================================
# Python Backend Part (No changes needed here)
# ==============================================================================
def handle_report_function(report_json_string):
    try:
        if not report_json_string:
            return "Empty request, ignored."
        report_data = json.loads(report_json_string)
        report_data['received_at'] = datetime.datetime.now().isoformat()
        print("New report received:", report_data)
        with open("reports.txt", "a", encoding="utf-8") as f:
            f.write(json.dumps(report_data, ensure_ascii=False) + "\n")
        return "Success"
    except Exception as e:
        print("Error processing report:", e)
        return "Error"

with gr.Blocks(css=".gradio-container {display: block !important;}") as demo:
    gr.HTML(html_full)
    with gr.Row(visible=False):
        report_data_input = gr.Textbox(elem_id="report_data_input")
        submit_report_button = gr.Button(elem_id="submit_report_button")
        report_status_output = gr.Textbox(elem_id="report_status_output")
    submit_report_button.click(
        fn=handle_report_function, 
        inputs=[report_data_input], 
        outputs=[report_status_output]
    )

demo.launch()


