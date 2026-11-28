"use strict";

const byId = (name) => document.getElementById(name);
const form = byId("claim-form");
const fields = byId("claim-fields");
const orderInput = byId("order-id");
const itemInput = byId("item-name");
const descriptionInput = byId("description");
const submitButton = byId("submit-claim");
const sampleButtons = [...document.querySelectorAll("[data-sample]")];
const statusBadge = byId("result-status");
const responseArea = byId("response-area");
const responseText = byId("response-text");
const responseMeta = byId("response-meta");
const copyStatus = byId("copy-status");
const priceFormat = new Intl.NumberFormat("vi-VN", { style: "currency", currency: "VND" });
const orders = new Map();

const samples = {
  standard: ["ORD-101", "Canh rong biển", "Tôi vừa nhận đơn và muốn báo thiếu món."],
  escalation: ["ORD-104", "Pizza hải sản cỡ vừa", "Đơn vừa giao chỉ có lon nước."],
  clarification: ["ORD-102", "", "Đơn vừa nhận bị giao thiếu, nhờ kiểm tra giúp tôi."],
};

const modeLabels = {
  fake: "Chế độ AI giả",
  missing: "Thiếu API key",
  configured: "Đã cấu hình AI thật",
};

const statusLabels = {
  idle: "Chưa gửi",
  busy: "Đang xử lý",
  error: "Cần kiểm tra",
  review: "Phản hồi hỗ trợ",
  refund: "Hoàn tiền mô phỏng",
  escalated: "Chuyển CSKH mô phỏng",
};

function setMode(mode, label) {
  const indicator = byId("mode");
  indicator.dataset.mode = mode;
  indicator.textContent = label;
}

function updateOrderPreview() {
  const order = orders.get(orderInput.value.trim().toUpperCase());
  const preview = byId("order-preview");
  const suggestions = byId("item-list");
  const items = byId("order-items");
  suggestions.replaceChildren();
  items.replaceChildren();
  preview.hidden = !order;
  if (!order) return;

  byId("order-restaurant").textContent = `${order.id} · ${order.restaurant}`;
  for (const item of order.items) {
    const option = document.createElement("option");
    option.value = item.name;
    suggestions.append(option);
    const line = document.createElement("li");
    line.textContent = `${item.name} · ${priceFormat.format(item.price)}`;
    items.append(line);
  }
}

async function loadDemo() {
  try {
    const response = await fetch("/api/demo");
    if (!response.ok) throw new Error();
    const data = await response.json();
    setMode(data.mode, modeLabels[data.mode] || "Chưa rõ cấu hình");
    for (const order of data.orders) {
      orders.set(order.id, order);
      const option = document.createElement("option");
      option.value = order.id;
      option.label = order.restaurant;
      byId("order-list").append(option);
    }
    updateOrderPreview();
  } catch {
    setMode("missing", "Chưa kết nối bản thử");
  }
}

function selectSample(name) {
  for (const button of sampleButtons) {
    button.setAttribute("aria-pressed", String(button.dataset.sample === name));
  }
}

function showState(state, message = "", data = null) {
  statusBadge.dataset.state = state;
  statusBadge.textContent = statusLabels[state];
  byId("empty-result").hidden = state !== "idle";
  responseArea.hidden = state === "idle";
  responseArea.dataset.state = state;
  responseText.textContent = message;
  responseMeta.hidden = !data;
  byId("copy-actions").hidden = !data;
  copyStatus.textContent = "";

  if (data) {
    byId("result-model").textContent = data.models.join(", ") || "—";
    byId("result-tools").textContent = String(data.tool_calls);
    byId("result-tokens").textContent = `${data.tokens_in} / ${data.tokens_out}`;
  }
}

function setBusy(busy) {
  fields.disabled = busy;
  submitButton.textContent = busy ? "Đang kiểm tra…" : "Kiểm tra yêu cầu";
  byId("result-panel").setAttribute("aria-busy", String(busy));
  for (const button of sampleButtons) button.disabled = busy;
}

for (const button of sampleButtons) {
  button.addEventListener("click", () => {
    const [order, item, description] = samples[button.dataset.sample];
    orderInput.value = order;
    itemInput.value = item;
    descriptionInput.value = description;
    selectSample(button.dataset.sample);
    updateOrderPreview();
    showState("idle");
    submitButton.focus({ preventScroll: true });
  });
}

orderInput.addEventListener("input", updateOrderPreview);
form.addEventListener("input", () => selectSample(null));
form.addEventListener("reset", () => {
  selectSample(null);
  showState("idle");
  requestAnimationFrame(updateOrderPreview);
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const order = orderInput.value.trim();
  const item = itemInput.value.trim();
  const description = descriptionInput.value.trim();
  const text = [order && `Mã đơn ${order}.`, item && `Món bị thiếu là ${item}.`, description]
    .filter(Boolean).join("\n");

  if (!text) {
    showState("error", "Nhập mã đơn, tên món hoặc mô tả sự cố để bắt đầu.");
    orderInput.focus();
    return;
  }

  setBusy(true);
  showState("busy", "Đang kiểm tra thông tin đơn hàng…");
  try {
    const response = await fetch("/api/claim", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    const result = await response.json();
    if (!response.ok) {
      showState("error", result.error || "Chưa xử lý được yêu cầu. Hãy thử lại.");
      return;
    }
    showState(result.status, result.output, result);
  } catch {
    showState("error", "Mất kết nối với bản thử. Kiểm tra terminal còn chạy rồi gửi lại.");
  } finally {
    setBusy(false);
  }
});

byId("copy-output").addEventListener("click", async () => {
  try {
    await navigator.clipboard.writeText(responseText.textContent);
    copyStatus.textContent = "Đã sao chép";
  } catch {
    copyStatus.textContent = "Bạn có thể bôi đen phản hồi để sao chép.";
  }
});

loadDemo();
