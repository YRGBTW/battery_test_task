const API = "http://localhost:8000/api/v1";

async function request(url, options = {}) {
  try {
    const res = await fetch(url, options);
    if (!res.ok) {
      const data = await res.json().catch(() => ({}));
      const msg = data.detail || res.statusText || "Unknown error";
      throw new Error(msg);
    }
    if (res.status === 204) return null;
    return res.json();
  } catch (err) {
    alert("⚠️ Ошибка: " + err.message);
    console.error("API error:", err);
  }
}

async function loadData() {
  const [devs, bats] = await Promise.all([
    request(API + "/devices/"),
    request(API + "/batteries/")
  ]);
  if (devs && bats) {
    renderDevices(devs);
    renderBatteries(bats, devs);
  }
}

// ==== CRUD DEVICES ====
async function createDevice() {
  const name = d("device-name").value;
  const version = d("device-version").value;
  await request(API + "/devices/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, version, state: true })
  });
  loadData();
}

async function deleteDevice(id) {
  await request(API + "/devices/" + id, { method: "DELETE" });
  loadData();
}

async function toggleDevice(id, state) {
  await request(API + `/devices/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ state: !state })
  });
  loadData();
}

async function editDevice(id, currentName, currentVersion) {
  const name = prompt("Новое имя устройства:", currentName);
  const version = prompt("Новая версия:", currentVersion);
  if (name === null || version === null) return;
  await request(API + `/devices/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, version })
  });
  loadData();
}

// ==== CRUD BATTERIES ====
async function createBattery() {
  const name = d("battery-name").value;
  const voltage = parseFloat(d("battery-voltage").value);
  const capacity = parseFloat(d("battery-capacity").value);
  const lifespan = parseInt(d("battery-lifespan").value);
  await request(API + "/batteries/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, voltage, capacity, lifespan })
  });
  loadData();
}

async function deleteBattery(id) {
  await request(API + "/batteries/" + id, { method: "DELETE" });
  loadData();
}

async function editBattery(b) {
  const name = prompt("Новое имя батареи:", b.name);
  const voltage = prompt("Новое напряжение:", b.voltage);
  const capacity = prompt("Новая ёмкость:", b.capacity);
  const lifespan = prompt("Новый срок службы:", b.lifespan);
  if (name === null) return;
  await request(API + `/batteries/${b.id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      name,
      voltage: parseFloat(voltage),
      capacity: parseFloat(capacity),
      lifespan: parseInt(lifespan)
    })
  });
  loadData();
}

// ==== ASSIGN ====
async function assignBattery(batteryId, deviceId) {
  if (!deviceId) return alert("Выберите устройство!");
  await request(`${API}/batteries/${batteryId}/assign/${deviceId}`, {
    method: "POST"
  });
  loadData();
}

// ==== RENDER ====
function renderDevices(devs) {
  const container = d("devices");
  container.innerHTML = "";
  devs.forEach(dev => {
    const stateLabel = dev.state ? "🟢 ON" : "🔴 OFF";
    container.innerHTML += `
      <div class="item">
        <b>${dev.name}</b> (v${dev.version}) — ${stateLabel}<br>
        ID: ${dev.id}<br>
        <button onclick="toggleDevice(${dev.id}, ${dev.state})">Toggle</button>
        <button onclick="editDevice(${dev.id}, '${dev.name}', '${dev.version}')">✏️ Edit</button>
        <button onclick="deleteDevice(${dev.id})">🗑 Delete</button>
      </div>`;
  });
}

function renderBatteries(bats, devs) {
  const container = d("batteries");
  container.innerHTML = "";
  bats.forEach(b => {
    const assigned = b.device_id ? `🔗 Device ${b.device_id}` : "❌ Not assigned";
    const options = devs.map(d => `<option value="${d.id}">${d.name}, ID: ${d.id}</option>`).join("");
    container.innerHTML += `
      <div class="item">
        <b>${b.name}</b> — ${b.voltage}V, ${b.capacity}Ah, ${b.lifespan}y<br>
        ${assigned}<br>
        <select id="sel-${b.id}">
          <option value="">-- choose device --</option>${options}
        </select>
        <button onclick="assignBattery(${b.id}, d('sel-${b.id}').value)">Assign</button>
        <button onclick="editBattery(${JSON.stringify(b).replace(/"/g, "&quot;")})">✏️ Edit</button>
        <button onclick="deleteBattery(${b.id})">🗑 Delete</button>
      </div>`;
  });
}

function d(id) {
  return document.getElementById(id);
}

loadData();
