document.addEventListener("DOMContentLoaded", () => {
    let allComplaints = [];
    let currentAudio = null;
    let currentPlayingBtn = null;
    let sortAscending = false;

    const tableBody = document.getElementById("tableBody");
    const searchInput = document.getElementById("searchInput");
    const startDateInput = document.getElementById("startDate");
    const endDateInput = document.getElementById("endDate");
    const resetBtn = document.getElementById("resetFilters");
    const sortDateHeader = document.getElementById("sortDate");
    const sortIcon = document.getElementById("sortIcon");

    async function fetchComplaints() {
        try {
            const res = await fetch("/api/complaints");
            allComplaints = await res.json();
            renderTable();
        } catch (err) {
            console.error("Failed to fetch complaints:", err);
        }
    }

    function renderTable() {
        let filtered = [...allComplaints];

        const searchVal = searchInput.value.toLowerCase().trim();
        const startDate = startDateInput.value;
        const endDate = endDateInput.value;

        if (searchVal) {
            filtered = filtered.filter(item => 
                item.date.includes(searchVal) || item.time.includes(searchVal)
            );
        }

        if (startDate) {
            filtered = filtered.filter(item => item.date >= startDate);
        }

        if (endDate) {
            filtered = filtered.filter(item => item.date <= endDate);
        }

        filtered.sort((a, b) => sortAscending ? a.timestamp - b.timestamp : b.timestamp - a.timestamp);

        tableBody.innerHTML = "";

        if (filtered.length === 0) {
            tableBody.innerHTML = `<tr><td colspan="4" class="text-center py-4 text-muted">No complaints found.</td></tr>`;
            return;
        }

        filtered.forEach(item => {
            const row = document.createElement("tr");

            row.innerHTML = `
                <td class="fw-bold">${item.date}</td>
                <td>${item.time}</td>
                <td>
                    <button class="btn btn-primary btn-sm play-btn" data-filename="${item.filename}">
                        <i class="bi bi-play-fill fs-5"></i>
                    </button>
                </td>
                <td class="text-end">
                    <button class="btn btn-outline-danger btn-sm delete-btn" data-filename="${item.filename}">
                        <i class="bi bi-trash-fill me-1"></i>Delete
                    </button>
                </td>
            `;

            tableBody.appendChild(row);
        });

        attachEventListeners();
    }

    function attachEventListeners() {
        document.querySelectorAll(".play-btn").forEach(btn => {
            btn.addEventListener("click", function () {
                const filename = this.getAttribute("data-filename");
                const audioUrl = `/audio/${filename}`;

                if (currentAudio && currentPlayingBtn === this) {
                    if (!currentAudio.paused) {
                        currentAudio.pause();
                        this.innerHTML = '<i class="bi bi-play-fill fs-5"></i>';
                    } else {
                        currentAudio.play();
                        this.innerHTML = '<i class="bi bi-pause-fill fs-5"></i>';
                    }
                    return;
                }

                if (currentAudio) {
                    currentAudio.pause();
                    if (currentPlayingBtn) {
                        currentPlayingBtn.innerHTML = '<i class="bi bi-play-fill fs-5"></i>';
                    }
                }

                currentAudio = new Audio(audioUrl);
                currentPlayingBtn = this;
                
                currentAudio.play();
                this.innerHTML = '<i class="bi bi-pause-fill fs-5"></i>';

                currentAudio.onended = () => {
                    this.innerHTML = '<i class="bi bi-play-fill fs-5"></i>';
                    currentAudio = null;
                    currentPlayingBtn = null;
                };
            });
        });

        document.querySelectorAll(".delete-btn").forEach(btn => {
            btn.addEventListener("click", async function () {
                const filename = this.getAttribute("data-filename");
                if (confirm(`Are you sure you want to delete ${filename}?`)) {
                    if (currentPlayingBtn && currentPlayingBtn.getAttribute("data-filename") === filename) {
                        if (currentAudio) currentAudio.pause();
                    }
                    
                    const res = await fetch(`/api/complaints/${filename}`, { method: "DELETE" });
                    if (res.ok) {
                        fetchComplaints();
                    }
                }
            });
        });
    }

    sortDateHeader.addEventListener("click", () => {
        sortAscending = !sortAscending;
        sortIcon.className = sortAscending ? "bi bi-sort-numeric-up ms-1" : "bi bi-sort-numeric-down ms-1";
        renderTable();
    });

    searchInput.addEventListener("input", renderTable);
    startDateInput.addEventListener("change", renderTable);
    endDateInput.addEventListener("change", renderTable);

    resetBtn.addEventListener("click", () => {
        searchInput.value = "";
        startDateInput.value = "";
        endDateInput.value = "";
        renderTable();
    });

    fetchComplaints();
});