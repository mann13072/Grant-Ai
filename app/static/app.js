const form = document.getElementById('grantForm');
const output = document.getElementById('output');
const alerts = document.getElementById('alerts');
const validationNode = document.getElementById('validationNode');
const validationText = document.getElementById('validationText');

function renderAlerts(violations) {
  alerts.innerHTML = '';
  if (violations.length === 0) {
    alerts.innerHTML = '<div class="border border-green-600 bg-green-950/40 rounded p-2 text-green-300">All BMWK budget checks passed.</div>';
    validationNode.classList.remove('border-red-600');
    validationNode.classList.add('border-green-600');
    validationText.classList.remove('text-red-300');
    validationText.classList.add('text-green-400');
    validationText.textContent = 'Rules currently satisfied.';
    return;
  }

  validationNode.classList.remove('border-green-600');
  validationNode.classList.add('border-red-600');
  validationText.classList.remove('text-green-400');
  validationText.classList.add('text-red-300');
  validationText.textContent = 'Violation detected. Adjust work package budgets.';

  violations.forEach((v) => {
    const box = document.createElement('div');
    box.className = 'border border-red-600 bg-red-950/40 rounded p-2 text-red-300';
    box.textContent = v;
    alerts.appendChild(box);
  });
}

async function submitForm(event) {
  event.preventDefault();
  const payload = {
    language: document.getElementById('language').value,
    cad_summary: document.getElementById('cad_summary').value,
    sap_metrics: document.getElementById('sap_metrics').value,
    personnel_cost: Number(document.getElementById('personnel_cost').value),
    third_party_cost: Number(document.getElementById('third_party_cost').value),
  };

  const response = await fetch('/api/transform', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  const data = await response.json();
  renderAlerts(data.budget_guard.violations);
  output.textContent = data.preview;
}

form.addEventListener('submit', submitForm);
form.dispatchEvent(new Event('submit'));
