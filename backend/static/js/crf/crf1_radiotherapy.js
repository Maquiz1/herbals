document.addEventListener("DOMContentLoaded", function () {

    const btn = document.getElementById("add-radio");
    const body = document.getElementById("radio-body");
    const total = document.getElementById("id_radiotherapies-TOTAL_FORMS");
    const toggle = document.getElementById("id_radiotherapy_performed");
    const table = document.getElementById("radio-table");

    if (!btn || !body || !total || !toggle || !table) return;

    // =========================
    // HELPER: CHECK YES (SAFE FK)
    // =========================
    function isYes(select) {
        return select.options[select.selectedIndex].text.toLowerCase() === "yes";
    }

    // =========================
    // TOGGLE TABLE (CONSISTENT WITH OTHER MEDICAL)
    // =========================
    function toggleTable() {

        const yesSelected = isYes(toggle);

        const hasRows =
            body.querySelectorAll(".radio-row:not([style*='display: none'])").length > 0;

        if (yesSelected || hasRows) {
            table.style.display = "";
        } else {
            table.style.display = "none";
        }

        // disable add button if not YES
        btn.disabled = !yesSelected;

        // auto-add first row if YES and empty
        if (yesSelected && body.children.length === 0) {
            btn.click();
        }
    }

    toggle.addEventListener("change", toggleTable);
    toggleTable();

    // =========================
    // ADD ROW
    // =========================
    btn.addEventListener("click", function () {

        let count = parseInt(total.value);

        let template = document.getElementById("radio-empty")?.innerHTML;

        if (!template) {
            console.error("Radiotherapy empty form template missing!");
            return;
        }

        template = template.replace(/__prefix__/g, count);

        const temp = document.createElement("tbody");
        temp.innerHTML = template;

        body.appendChild(temp.firstElementChild);

        total.value = count + 1;

        toggleTable(); // refresh visibility
    });

    // =========================
    // REMOVE ROW (SMART DELETE)
    // =========================
    body.addEventListener("click", function (e) {

        if (e.target.classList.contains("remove-radio")) {

            const row = e.target.closest("tr");
            const del = row.querySelector("input[type='checkbox']");

            if (del) {
                // existing row → soft delete
                del.checked = true;
                row.style.display = "none";
            } else {
                // new row → remove
                row.remove();
                total.value = body.querySelectorAll(".radio-row").length;
            }

            toggleTable(); // refresh after delete
        }
    });

    // =========================
    // AUTO-HIDE END DATE IF ONGOING = YES
    // =========================
    body.addEventListener("change", function (e) {

        if (e.target.name.includes("radiotherapy_ongoing")) {

            const row = e.target.closest("tr");

            const ongoingSelect = e.target;
            const endInput = row.querySelector("input[name*='radiotherapy_end']");

            if (!endInput) return;

            const isOngoingYes =
                ongoingSelect.options[ongoingSelect.selectedIndex].text.toLowerCase() === "yes";

            if (isOngoingYes) {
                endInput.value = "";
                endInput.closest("td").style.display = "none";
            } else {
                endInput.closest("td").style.display = "";
            }
        }
    });

    // =========================
    // INITIALIZE EXISTING ROWS (UPDATE MODE)
    // =========================
    function initExistingRows() {
        body.querySelectorAll(".radio-row").forEach(row => {

            const ongoingSelect = row.querySelector("select[name*='radiotherapy_ongoing']");
            const endInput = row.querySelector("input[name*='radiotherapy_end']");

            if (!ongoingSelect || !endInput) return;

            const isOngoingYes =
                ongoingSelect.options[ongoingSelect.selectedIndex].text.toLowerCase() === "yes";

            if (isOngoingYes) {
                endInput.closest("td").style.display = "none";
            }
        });
    }

    initExistingRows();

    // =========================
    // PREVENT EMPTY ROWS ON SUBMIT
    // =========================
    document.querySelector("form").addEventListener("submit", function () {

        body.querySelectorAll(".radio-row").forEach(row => {

            const inputs = row.querySelectorAll("input, select, textarea");

            let hasValue = false;

            inputs.forEach(input => {
                if (input.type !== "checkbox" && input.value.trim() !== "") {
                    hasValue = true;
                }
            });

            // mark empty rows for deletion
            if (!hasValue) {
                const del = row.querySelector("input[type='checkbox']");
                if (del) del.checked = true;
            }
        });
    });

});