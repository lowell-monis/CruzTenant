document.addEventListener('DOMContentLoaded', () => {
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

  // Info Tab Switching Logic
  const tabBtns = document.querySelectorAll('.tab-btn');
  const tabPanels = document.querySelectorAll('.tab-panel');

  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetId = btn.getAttribute('data-tab');
      tabBtns.forEach(b => b.classList.remove('active'));
      tabPanels.forEach(p => p.classList.remove('active'));

      btn.classList.add('active');
      const targetPanel = document.getElementById(targetId);
      if (targetPanel) {
        targetPanel.classList.add('active');
      }
    });
  });

  let sampleCases = [];

  fetch('/api/sample-cases')
    .then(res => res.json())
    .then(data => {
      if (data.status === 'success') {
        sampleCases = data.cases;
        renderSamplePills();
      }
    })
    .catch(err => console.error('failed to load sample cases:', err));

  function renderSamplePills() {
    samplePills.innerHTML = '';
    sampleCases.forEach((c, index) => {
      const pill = document.createElement('button');
      pill.className = `pill-btn ${index === 0 ? 'active' : ''}`;
      pill.textContent = c.title;
      pill.addEventListener('click', () => loadSampleCase(c, pill));
      samplePills.appendChild(pill);
    });

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
    landlordNameInput.value = c.landlord_name || 'Bayshore Coastal Rental Mgmt';
    inputTextarea.value = c.input_text;
    
    if (c.id === 'case_1') {
      calcCurrentRent.value = 2800;
      calcProposedRent.value = 3304;
    } else if (c.id === 'case_3') {
      calcCurrentRent.value = 2800;
      calcProposedRent.value = 2800;
    }
    updateRentCalculator();
  }

  function updateRentCalculator() {
    const curr = parseFloat(calcCurrentRent.value) || 0;
    const prop = parseFloat(calcProposedRent.value) || 0;
    
    if (curr <= 0) return;
    
    const pct = ((prop - curr) / curr) * 100.0;
    const maxLegalRent = curr * (1 + 0.088);
    const excessMonthly = Math.max(0, prop - maxLegalRent);
    
    resIncreasePct.textContent = `${pct.toFixed(2)}%`;
    resIncreasePct.className = pct > 8.8 ? 'text-danger' : 'text-success';
    
    resMaxLegalRent.textContent = `$${maxLegalRent.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;
    
    if (excessMonthly > 0) {
      resExcessMonthly.textContent = `$${excessMonthly.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})} / mo`;
      resExcessMonthly.className = 'text-warning';
    } else {
      resExcessMonthly.textContent = '$0.00 (within cap)';
      resExcessMonthly.className = 'text-success';
    }
  }

  calcCurrentRent.addEventListener('input', updateRentCalculator);
  calcProposedRent.addEventListener('input', updateRentCalculator);

  clearBtn.addEventListener('click', () => {
    inputTextarea.value = '';
    agentTraceSection.style.display = 'none';
    resultsSection.style.display = 'none';
  });

  analyzeBtn.addEventListener('click', () => {
    const text = inputTextarea.value.trim();
    if (!text) {
      alert('please enter lease text or select a sample case.');
      return;
    }

    analyzeBtn.disabled = true;
    analyzeBtn.innerHTML = `
      <svg class="spin" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12a9 9 0 1 1-6.219-8.56"></path></svg>
      running Gemma 4...
    `;

    agentTraceSection.style.display = 'block';
    resultsSection.style.display = 'none';
    timelineContainer.innerHTML = '<div class="timeline-item"><span class="step-icon">Step 1</span><div class="step-content"><h5>initializing Gemma 4 tool engine...</h5><p>parsing text for Santa Cruz legal compliance...</p></div></div>';

    fetch('/api/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        text: text,
        tenant_name: tenantNameInput.value || 'Jane Doe',
        landlord_name: landlordNameInput.value || 'Bayshore Coastal Rental Mgmt'
      })
    })
    .then(res => res.json())
    .then(data => {
      analyzeBtn.disabled = false;
      analyzeBtn.innerHTML = `
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
        analyze document
      `;

      if (data.agent_trace) {
        renderAgentTrace(data.agent_trace);
      }
      renderAnalysisResults(data);
    })
    .catch(err => {
      console.error('analysis error:', err);
      analyzeBtn.disabled = false;
      analyzeBtn.innerHTML = `
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
        analyze document
      `;
      
      renderAnalysisResults({
        status: 'error',
        message: 'API rate limit or network error: Live AI analysis unavailable. Please consult verified Santa Cruz legal aid resources below.',
        violations: ['ERROR: Live AI document analysis unavailable due to API rate limit or missing API key.'],
        recommendations: ['consult verified Santa Cruz legal aid resources below for human legal advice.'],
        dispute_letter: 'ERROR: Live AI document analysis unavailable due to API rate limit or missing API key. No automated dispute letter will be generated.',
        legal_aid_resources: [
          {
            name: "Senior Citizens Legal Services - Santa Cruz",
            address: "501 Soquel Ave, Suite F, Santa Cruz, CA 95062",
            phone: "(831) 426-8824",
            services: ["eviction defense", "rent increase disputes", "housing discrimination"]
          },
          {
            name: "California Rural Legal Assistance (CRLA) - Watsonville/Santa Cruz",
            address: "21 Carr St, Watsonville, CA 95076",
            phone: "(831) 724-2253",
            services: ["tenant rights", "substandard housing litigation", "unlawful detainer defense"]
          },
          {
            name: "Conflict Resolution Center of Santa Cruz County",
            address: "147 S River St, Suite 206, Santa Cruz, CA 95060",
            phone: "(831) 475-6117",
            services: ["landlord-tenant mediation", "rent dispute settlement"]
          },
          {
            name: "Santa Cruz County Law Library Tenant Self-Help",
            address: "701 Ocean Street, Room 080, Santa Cruz, CA 95060",
            phone: "(831) 457-2525",
            services: ["legal form filing", "tenant answer assistance", "municipal code research"]
          }
        ]
      });
    });
  });

  function renderAgentTrace(traceSteps) {
    timelineContainer.innerHTML = '';
    agentStatusBadge.textContent = `${traceSteps.length} trace steps`;

    traceSteps.forEach((step, idx) => {
      const item = document.createElement('div');
      item.className = 'timeline-item';
      
      let iconClass = step.type && step.type.includes('tool') ? 'step-icon tool' : 'step-icon';

      let bodyHtml = `<p>${step.content || ''}</p>`;
      if (step.tool_args) {
        bodyHtml += `<div class="code-block">tool arguments: ${JSON.stringify(step.tool_args, null, 2)}</div>`;
      }
      if (step.result) {
        bodyHtml += `<div class="code-block">tool output: ${JSON.stringify(step.result, null, 2)}</div>`;
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

  function renderAnalysisResults(data) {
    resultsSection.style.display = 'block';

    if (data.status === 'error') {
      statusBanner.className = 'status-banner illegal';
      statusBanner.innerHTML = `⚠️ ${data.message || 'API rate limit reached. Live AI analysis is currently unavailable.'}`;
      
      violationsList.innerHTML = '<div class="violation-card" style="border-left-color: var(--warning); background: rgba(245, 158, 11, 0.08);">ERROR: Live AI analysis unavailable due to API rate limit or missing API key.</div>';
      
      recommendationsList.innerHTML = '<div class="recommendation-card">consult verified Santa Cruz legal aid resources below for human legal advice.</div>';
      
      disputeLetterBox.textContent = data.dispute_letter || 'ERROR: Live AI document analysis unavailable due to API rate limit or missing API key. No automated dispute letter will be generated.';
    } else if (data.is_illegal) {
      statusBanner.className = 'status-banner illegal';
      statusBanner.innerHTML = `⚠️ statutory violation detected: identified ${data.violations_count} unlawful terms under Santa Cruz Municipal Code or California law.`;
      
      violationsList.innerHTML = '';
      (data.violations || []).forEach(v => {
        const div = document.createElement('div');
        div.className = 'violation-card';
        div.textContent = v;
        violationsList.appendChild(div);
      });

      recommendationsList.innerHTML = '';
      (data.recommendations || []).forEach(r => {
        const div = document.createElement('div');
        div.className = 'recommendation-card';
        div.textContent = r;
        recommendationsList.appendChild(div);
      });

      disputeLetterBox.textContent = data.dispute_letter || 'No document generated.';
    } else {
      statusBanner.className = 'status-banner legal';
      statusBanner.innerHTML = `✅ compliant notice: no statutory violations detected. terms comply with Santa Cruz cap rules.`;
      
      violationsList.innerHTML = '<div class="violation-card" style="border-left-color: var(--success); background: rgba(52, 211, 153, 0.08);">no statutory violations detected in submitted text.</div>';
      
      recommendationsList.innerHTML = '<div class="recommendation-card">retain all written communications and verify notice service dates.</div>';
      
      disputeLetterBox.textContent = data.dispute_letter || 'No document generated.';
    }

    legalAidList.innerHTML = '';
    (data.legal_aid_resources || []).forEach(aid => {
      const div = document.createElement('div');
      div.className = 'aid-card';
      div.innerHTML = `
        <strong>${aid.name}</strong><br>
        📍 ${aid.address} | 📞 ${aid.phone}<br>
        <span style="color: var(--text-dim); font-size: 0.78rem;">services: ${aid.services.join(', ')}</span>
      `;
      legalAidList.appendChild(div);
    });

    resultsSection.scrollIntoView({ behavior: 'smooth' });
  }

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
