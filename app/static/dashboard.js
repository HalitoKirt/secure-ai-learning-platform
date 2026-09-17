function getEventOutcome(event, eventData) {
  return (
    event.status ||
    eventData.status ||
    eventData.action ||
    eventData.policy_action ||
    eventData.risk_level ||
    eventData.reason ||
    "recorded"
  );
} 

async function loadEvents() {
  const eventsContainer = document.getElementById("events");
  const summaryContainer = document.getElementById("eventSummary");

  eventsContainer.innerHTML = "Loading telemetry...";

    try {
    const response = await fetch("/api/telemetry/recent");
    const data = await response.json();

    const events = data.events || [];

    summaryContainer.innerHTML =
      `Loaded ${events.length} telemetry events.`;

    eventsContainer.innerHTML = "";

    events.reverse().forEach(event => {
      const eventData = event.data || {};
      const card = document.createElement("div");
      card.className = "event";

      card.innerHTML = `
        <div class="event-title">${event.event_type || "unknown_event"}</div>
        <div class="event-time">${event.timestamp || "no timestamp"}</div>
        <div>Outcome: ${getEventOutcome(event, eventData)}</div>
        <div>Component: ${eventData.component || "n/a"}</div>
        <div>Mode: ${eventData.mode || "n/a"}</div>
      `;

      eventsContainer.appendChild(card);
    });
  } catch (error) {
    eventsContainer.innerHTML =
      `<div class="event">Failed to load telemetry events.</div>`;
    console.error(error);
  }
}

function showProcessingStages() {
  const demoStatus = document.getElementById("demoStatus");

  demoStatus.innerHTML = `
    <div class="pipeline">
      <div>🔍 Security inspection started</div>
      <div>📚 RAG retrieval in progress</div>
      <div>🤖 Agent processing response</div>
      <div>🛡 Output guardrail validation</div>
      <div>📡 SOC telemetry update pending</div>
    </div>
  `;
}

async function runDemo(event) {
  event.preventDefault();

  const mode = document.getElementById("mode").value;
  const question = document.getElementById("question").value;
  const demoStatus = document.getElementById("demoStatus");
  const demoResponse = document.getElementById("demoResponse");

  showProcessingStages();
  demoResponse.textContent = "";

  try {
    const response = await fetch("/demo/ask", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        mode: mode,
        question: question
      })
    });

    const data = await response.json();

    if (!response.ok) {
      demoStatus.innerHTML = "Demo request failed.";
      demoResponse.textContent = JSON.stringify(data, null, 2);
      await loadEvents();
      return;
    }

    demoStatus.innerHTML =
      "✅ Demo request completed. Security checks, RAG, agent execution, output validation, and telemetry logging finished.";

    demoResponse.textContent = data.answer || JSON.stringify(data, null, 2);

    await loadEvents();
  } catch (error) {
    demoStatus.innerHTML = "Demo request failed.";
    demoResponse.textContent = error.toString();
    console.error(error);
  }
}

document
  .getElementById("demoForm")
  .addEventListener("submit", runDemo);

loadEvents();
