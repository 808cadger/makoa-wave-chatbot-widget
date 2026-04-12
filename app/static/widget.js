(function () {
  const config = window.MAKOA_WAVE_WIDGET_CONFIG || {};
  const apiBase = (config.apiBase || window.location.origin).replace(/\/$/, "");
  const title = config.title || "Chat with Makoa~Wave";
  const placeholder = config.placeholder || "Type your message...";
  const context = config.context || "";

  const style = document.createElement("style");
  style.textContent = `
    .mw-launcher {
      position: fixed;
      right: 20px;
      bottom: 20px;
      z-index: 2147483647;
      width: 64px;
      height: 64px;
      border: 0;
      border-radius: 999px;
      background: linear-gradient(135deg, #0d7c6d, #17a58d);
      color: #fff;
      font: 600 15px/1 system-ui, sans-serif;
      box-shadow: 0 18px 40px rgba(13, 124, 109, 0.35);
      cursor: pointer;
    }
    .mw-panel {
      position: fixed;
      right: 20px;
      bottom: 96px;
      z-index: 2147483647;
      width: min(360px, calc(100vw - 24px));
      height: 520px;
      display: none;
      flex-direction: column;
      overflow: hidden;
      border-radius: 24px;
      border: 1px solid rgba(18, 49, 47, 0.12);
      background: #fff;
      box-shadow: 0 24px 80px rgba(18, 49, 47, 0.18);
      font-family: system-ui, sans-serif;
    }
    .mw-panel.open { display: flex; }
    .mw-header {
      padding: 16px 18px;
      background: linear-gradient(135deg, #0d7c6d, #17a58d);
      color: #fff;
      font-weight: 700;
    }
    .mw-messages {
      flex: 1;
      padding: 16px;
      overflow-y: auto;
      background: #f6fbf9;
    }
    .mw-msg {
      max-width: 85%;
      margin-bottom: 12px;
      padding: 12px 14px;
      border-radius: 16px;
      white-space: pre-wrap;
      line-height: 1.45;
      font-size: 14px;
    }
    .mw-user {
      margin-left: auto;
      background: #dff5ee;
      color: #12312f;
    }
    .mw-bot {
      background: #fff;
      color: #12312f;
      border: 1px solid rgba(18, 49, 47, 0.08);
    }
    .mw-form {
      display: flex;
      gap: 10px;
      padding: 14px;
      border-top: 1px solid rgba(18, 49, 47, 0.08);
      background: #fff;
    }
    .mw-input {
      flex: 1;
      border: 1px solid rgba(18, 49, 47, 0.16);
      border-radius: 14px;
      padding: 12px;
      font: inherit;
      outline: none;
    }
    .mw-send {
      border: 0;
      border-radius: 14px;
      padding: 0 16px;
      background: #12312f;
      color: #fff;
      font: 600 14px/1 system-ui, sans-serif;
      cursor: pointer;
    }
  `;
  document.head.appendChild(style);

  const launcher = document.createElement("button");
  launcher.className = "mw-launcher";
  launcher.type = "button";
  launcher.textContent = "Chat";

  const panel = document.createElement("section");
  panel.className = "mw-panel";
  panel.innerHTML = `
    <div class="mw-header">${title}</div>
    <div class="mw-messages" aria-live="polite"></div>
    <form class="mw-form">
      <input class="mw-input" type="text" placeholder="${placeholder}" />
      <button class="mw-send" type="submit">Send</button>
    </form>
  `;

  document.body.appendChild(launcher);
  document.body.appendChild(panel);

  const messages = panel.querySelector(".mw-messages");
  const form = panel.querySelector(".mw-form");
  const input = panel.querySelector(".mw-input");

  function addMessage(text, role) {
    const node = document.createElement("div");
    node.className = `mw-msg ${role === "user" ? "mw-user" : "mw-bot"}`;
    node.textContent = text;
    messages.appendChild(node);
    messages.scrollTop = messages.scrollHeight;
  }

  launcher.addEventListener("click", function () {
    panel.classList.toggle("open");
    if (panel.classList.contains("open")) {
      input.focus();
    }
  });

  form.addEventListener("submit", async function (event) {
    event.preventDefault();
    const message = input.value.trim();
    if (!message) return;

    addMessage(message, "user");
    input.value = "";
    input.disabled = true;

    try {
      const response = await fetch(`${apiBase}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message, context }),
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || "Request failed");
      }
      addMessage(data.reply, "assistant");
    } catch (error) {
      addMessage("Sorry, the chat is temporarily unavailable. Can you try again?", "assistant");
      console.error("Makoa~Wave widget error:", error);
    } finally {
      input.disabled = false;
      input.focus();
    }
  });

  addMessage("Aloha. Ask me anything and I’ll reply in your language. What can I help with?", "assistant");
})();
