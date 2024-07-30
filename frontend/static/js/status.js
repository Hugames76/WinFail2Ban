async function fetchStatus() {
    const response = await fetch('http://127.0.0.1:5000/status');
    const data = await response.json();
    updateTables(data);
}

function updateTables(data) {
    const failedAttemptsTable = document.getElementById('failedAttemptsTable').getElementsByTagName('tbody')[0];
    failedAttemptsTable.innerHTML = '';
    for (const [ip, attempts] of Object.entries(data.failed_attempts)) {
        const row = failedAttemptsTable.insertRow();
        row.insertCell(0).textContent = ip;
        row.insertCell(1).textContent = attempts;
        row.insertCell(2).textContent = data.total_attempts[ip];
    }

    const blockedIpsTable = document.getElementById('blockedIpsTable').getElementsByTagName('tbody')[0];
    blockedIpsTable.innerHTML = '';
    for (const [ip, unblockTime] of Object.entries(data.blocked_ips)) {
        const row = blockedIpsTable.insertRow();
        row.insertCell(0).textContent = ip;
        row.insertCell(1).textContent = unblockTime;
    }
}

setInterval(fetchStatus, 5000);
fetchStatus();