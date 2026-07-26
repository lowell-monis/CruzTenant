document.addEventListener('DOMContentLoaded', () => {
  // DOM Elements
  const samplePills = document.getElementById('samplePills');
  const tenantNameInput = document.getElementById('tenantName');
  const landlordNameInput = document.getElementById('landlordName');
  const inputTextarea = document.getElementById('inputText');
  const analyzeBtn = document.getElementById('analyzeBtn');
  const clearBtn = document.getElementById('clearBtn');
  
  const calcCurrentRent = document.getElementById('calcCurrentRent');
  const calcProposedRent = document.getElementById('calcProposedRent');
  const resIncreasePct = document.getElementById('resIncreasePct');
  const resMaxLegalRent = document.getElementById('resMaxLegalRent');
  const resExcessMonthly = document.getElementById('resExcessMonthly');
  
  const agentTraceSection = document.getElementById('agentTraceSection');
  const agentStatusBadge = document.getElementById('agentStatusBadge');
  const timelineContainer = document.getElementById('timelineContainer');
  
  const resultsSection = document.getElementById('resultsSection');
  const statusBanner = document.getElementById('statusBanner');
  const violationsList = document.getElementById('violationsList');
  const recommendationsList = document.getElementById('recommendationsList');
  const legalAidList = document.getElementById('legalAidList');
  const disputeLetterBox = document.getElementById('disputeLetterBox');
  const printLetterBtn = document.getElementById('printLetterBtn');

  let sampleCases = [];

  // Fetch Sample Cases on Init
  fetch('/api/sample-cases')
    .then(res => res.json())
    .then(data => {
      if (data.status === 'success') {
        sampleCases = data.cases;
        renderSamplePills();
      }
    })
    .catch(err => console.error('Failed to load sample cases:', err));

  function renderSamplePills() {
    samplePills.innerHTML = '';
    sampleCases.forEach((c, index) => {
      const pill = document.createElement('button');
      pill.className = `pill-btn ${index === 0 ? 'active' : ''}`;
      pill.textContent = c.title;
      pill.addEventListener('click', () => loadSampleCase(c, pill));
      samplePills.appendChild(pill);
    });

    // Auto-load first sample case
    if (sampleCases.length > 0) {
      loadSampleCase(sampleCases[0]);
    }
  }

  function loadSampleCase(c, activePill = null) {
    if (activePill) {
      document.querySelectorAll('.pill-btn').forEach(p => p.classList.remove('active'));
      activePill.classList.add('active');
    }

    tenantNameInput.value = c.tenant_name || 'Alex Rivera';
    landlordNameInput.value = c.landlord_name || 'Property Mgmt Co';
    inputTextarea.value = c.input_text;
    
    // Auto sync rent calculator if available in case 1
    if (c.id === 'case_1') {
      calcCurrentRent.value = 2800;
      calcProposedRent.value = 3304;
    } else if (c.id === 'case_3') {
      calcCurrentRent.value = 2800;
      calcProposedRent.value = 2800;
    }
    updateRentCalculator();
  }

  // Interactive Calculator Logic
  function updateRentCalculator() {
    const curr = parseFloat(calcCurrentRent.value) || 0;
    const prop = parseFloat(calcProposedRent.value) || 0;
    
    if (curr <= 0) return;
    
    const pct = ((prop - curr) / curr) * 100.0;
    const maxLegalRent = curr * (1 + 0.088); // 8.8% cap under SC CPI
    const excessMonthly = Math.max(0, prop - maxLegalRent);
    
    resIncreasePct.textContent = `${pct.toFixed(2)}%`;
    resIncreasePct.className = pct > 8.8 ? 'text-danger' : 'text-success';
    
    resMaxLegalRent.textContent = `$${maxLegalRent.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;
    
    if (excessMonthly > 0) {
      resExcessMonthly.textContent = `$${excessMonthly.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})} / mo`;
      resExcessMonthly.className = 'text-warning';
    } else {
      resExcessMonthly.textContent = '$0.00 (Within Cap)';
      resExcessMonthly.className = 'text-success';
    }
  }

  calcCurrentRent.addEventListener('input', updateRentCalculator);
  calcProposedRent.addEventListener('input', updateRentCalculator);

  // Clear Input Button
  clearBtn.addEventListener('click', () => {
    inputTextarea.value = '';
    agentTraceSection.style.display = 'none';
    resultsSection.style.display = 'none';
  });

  // Analyze Button Click (Trigger Agent Execution)
  analyzeBtn.addEventListener('click', () => {
    const text = inputTextarea.value.trim();
    if (!text) {
      alert('Please enter lease text, a notice, or select a sample case to analyze.');
      return;
    }

    analyzeBtn.disabled = true;
    analyzeBtn.innerHTML = `
      <svg class="spin" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12a9 9 0 1 1-6.219-8.56"></path></svg>
      Running Gemma 4 Agent...
    `;

    agentTraceSection.style.display = 'block';
    resultsSection.style.display = 'none';
    timelineContainer.innerHTML = '<div class="timeline-item"><span class="step-icon">Agent</span><div class="step-content"><h5>Initializing Gemma 4 Tool Engine...</h5><p>Parsing text for Santa Cruz legal compliance...</p></div></div>';

    fetch('/api/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        text: text,
        tenant_name: tenantNameInput.value || 'Jane Doe',
        landlord_name: landlordNameInput.value || 'Property Mgmt Co'
      })
    })
    .then(res => res.json())
    .then(data => {
      analyzeBtn.disabled = false;
      analyzeBtn.innerHTML = `
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
        Analyze with Gemma 4 Agent
      `;

      if (data.status === 'success') {
        renderAgentTrace(data.agent_trace);
        renderAnalysisResults(data);
      } else {
        alert('Analysis Error: ' + (data.message || 'Unknown error'));
      }
    })
    .catch(err => {
      console.error('Agent analysis error:', err);
      analyzeBtn.disabled = false;
      analyzeBtn.innerHTML = 'Analyze with Gemma 4 Agent';
      alert('Failed to connect to backend server.');
    });
  });

  // Render Tool Execution Timeline Trace
  function renderAgentTrace(traceSteps) {
    timelineContainer.innerHTML = '';
    agentStatusBadge.textContent = `${traceSteps.length} Trace Steps`;

    traceSteps.forEach((step, idx) => {
      const item = document.createElement('div');
      item.className = 'timeline-item';
      
      let stepTag = step.type === 'tool_call' ? 'TOOL CALL' : (step.type === 'tool_result' ? 'RESULT' : 'THOUGHT');
      let iconClass = step.type.includes('tool') ? 'step-icon tool' : 'step-icon';

      let bodyHtml = `<p>${step.content || ''}</p>`;
      if (step.tool_args) {
        bodyHtml += `<div class="code-block">Tool Arguments: ${JSON.stringify(step.tool_args, null, 2)}</div>`;
      }
      if (step.result) {
        bodyHtml += `<div class="code-block">Tool Output: ${JSON.stringify(step.result, null, 2)}</div>`;
      }

      item.innerHTML = `
        <span class="${iconClass}">Step ${step.step}</span>
        <div class="step-content">
          <h5>${step.title}</h5>
          ${bodyHtml}
        </div>
      `;
      timelineContainer.appendChild(item);
    });
  }

  // Render Final Legal Diagnosis & Dispute Form
  function renderAnalysisResults(data) {
    resultsSection.style.display = 'block';

    if (data.is_illegal) {
      statusBanner.className = 'status-banner illegal';
      statusBanner.innerHTML = `⚠️ STATUTORY VIOLATION DETECTED: Identified ${data.violations_count} unlawful terms under Santa Cruz Municipal Code / CA Law.`;
    } else {
      statusBanner.className = 'status-banner legal';
      statusBanner.innerHTML = `✅ COMPLIANT NOTICE: No immediate municipal violations detected. Terms appear legal under Santa Cruz cap rules.`;
    }

    // Render Violations List
    violationsList.innerHTML = '';
    data.violations.forEach(v => {
      const div = document.createElement('div');
      div.className = 'violation-card';
      div.textContent = v;
      violationsList.appendChild(div);
    });

    // Render Recommendations
    recommendationsList.innerHTML = '';
    data.recommendations.forEach(r => {
      const div = document.createElement('div');
      div.className = 'recommendation-card';
      div.textContent = r;
      recommendationsList.appendChild(div);
    });

    // Render Legal Aid Contacts
    legalAidList.innerHTML = '';
    (data.legal_aid_resources || []).forEach(aid => {
      const div = document.createElement('div');
      div.className = 'aid-card';
      div.innerHTML = `
        <strong>${aid.name}</strong><br>
        📍 ${aid.address} | 📞 ${aid.phone}<br>
        <span style="color: var(--text-dim); font-size: 0.78rem;">Services: ${aid.services.join(', ')}</span>
      `;
      legalAidList.appendChild(div);
    });

    // Render Formal Dispute Letter
    disputeLetterBox.textContent = data.dispute_letter;

    // Scroll to results smoothly
    resultsSection.scrollIntoView({ behavior: 'smooth' });
  }

  // Print/Export Letter Handler
  printLetterBtn.addEventListener('click', () => {
    const printWin = window.open('', '_blank');
    printWin.document.write(`
      <html>
        <head>
          <title>Santa Cruz Formal Tenant Dispute Document</title>
          <style>
            body { font-family: 'Courier New', monospace; padding: 40px; line-height: 1.6; font-size: 14px; }
            h2 { font-family: sans-serif; text-align: center; }
          </style>
        </head>
        <body>
          <pre>${disputeLetterBox.textContent}</pre>
          <script>window.print();</script>
        </body>
      </html>
    `);
    printWin.document.close();
  });
});
