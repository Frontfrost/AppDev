const API_BASE = "http://127.0.0.1:8000";

const exprDisplay = document.getElementById("expr-display");
const resultDisplay = document.getElementById("result-display");
const todayHistory = document.getElementById("today-history");
const clearHistoryBtn = document.getElementById("clear-history-btn");

let currentExpr = "";
let isEvaluated = false;

document.querySelectorAll(".btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    const char = btn.getAttribute("data-input");
    const action = btn.getAttribute("data-action");

    if (char) handleInput(char);
    if (action) handleAction(action);
  });
});

function handleInput(char) {
  if (isEvaluated && /[0-9.]/.test(char)) {
    currentExpr = "";
  }
  isEvaluated = false;
  currentExpr += char;
  exprDisplay.textContent = currentExpr;
}

function handleAction(action) {
  if (action === "clear") {
    currentExpr = "";
    exprDisplay.textContent = "";
    resultDisplay.textContent = "0";
    isEvaluated = false;
  } else if (action === "sign") {
    if (!currentExpr) return;
    currentExpr = currentExpr.startsWith("-") ? currentExpr.slice(1) : "-" + currentExpr;
    exprDisplay.textContent = currentExpr;
  } else if (action === "calculate") {
    if (!currentExpr) return;
    sendCalculation(currentExpr);
  }
}

// ยิง Request ไปยัง Backend
async function sendCalculation(rawExpr) {
  const exprToSend = rawExpr.replace(/÷/g, "/").replace(/×/g, "*");

  try {
    const res = await fetch(`${API_BASE}/calculate?expr=${encodeURIComponent(exprToSend)}`, {
      method: "POST",
    });
    const data = await res.json();

    if (data.ok) {
      resultDisplay.textContent = data.result;
      isEvaluated = true;
      loadHistory();
    } else {
      resultDisplay.textContent = "Error";
    }
  } catch (err) {
    console.error(err);
    resultDisplay.textContent = "Error";
  }
}

// โหลดประวัติการคำนวณ
async function loadHistory() {
  try {
    const res = await fetch(`${API_BASE}/history`);
    if (!res.ok) return;
    const list = await res.json();

    todayHistory.innerHTML = "";
    list.forEach((item) => {
      const div = document.createElement("div");
      div.className = "history-item";
      div.innerHTML = `
        <div class="h-expr">${item.expr}</div>
        <div class="h-res">${item.result}</div>
      `;
      div.onclick = () => {
        currentExpr = String(item.result);
        exprDisplay.textContent = item.expr;
        resultDisplay.textContent = item.result;
        isEvaluated = true;
      };
      todayHistory.appendChild(div);
    });
  } catch (err) {
    console.warn("History fetch failed:", err);
  }
}

// ล้างประวัติ
clearHistoryBtn.addEventListener("click", async () => {
  try {
    await fetch(`${API_BASE}/history`, { method: "DELETE" });
    todayHistory.innerHTML = "";
  } catch (err) {
    console.warn("Clear history failed:", err);
  }
});

// โหลดประวัติรอบแรกเมื่อเปิดเว็บ
loadHistory();