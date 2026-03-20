document.addEventListener("DOMContentLoaded", function () {

    const btn = document.getElementById("add-radio");
    const body = document.getElementById("radio-body");
    const total = document.getElementById("id_radiotherapies-TOTAL_FORMS");
    const toggle = document.getElementById("id_radiotherapy_performed");
    const table = document.getElementById("radio-table");

    if (!btn || !body || !total) return;

    // =========================
    // TOGGLE TABLE
    // =========================
    function toggleTable() {
        const isYes = toggle?.value === "1";

        table.style.display = isYes ? "" : "none";

        // auto-add first row
        if (isYes && body.children.length === 0) {
            btn.click();
        }

        btn.disabled = !isYes;
    }

    toggle?.addEventListener("change", toggleTable);
    toggleTable();

    // =========================
    // ADD ROW
    // =========================
    btn.addEventListener("click", function () {

        let count = parseInt(total.value);

        let template = document.getElementById("radio-empty")?.innerHTML;

        if (!template) return;

        template = template.replace(/__prefix__/g, count);

        const temp = document.createElement("tbody");
        temp.innerHTML = template;

        body.appendChild(temp.firstElementChild);

        total.value = count + 1;
    });

    // =========================
    // REMOVE ROW
    // =========================
    body.addEventListener("click", function (e) {

        if (e.target.classList.contains("remove-radio")) {

            const row = e.target.closest("tr");
            const del = row.querySelector("input[type='checkbox']");

            if (del) {
                del.checked = true;
                row.style.display = "none";
            } else {
                row.remove();
                total.value = body.querySelectorAll(".radio-row").length;
            }
        }
    });

});