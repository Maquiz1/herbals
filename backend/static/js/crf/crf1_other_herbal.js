document.addEventListener("DOMContentLoaded", function () {

    const btn = document.getElementById("add-herbal");
    const body = document.getElementById("herbal-body");
    const total = document.getElementById("id_otherherbals-TOTAL_FORMS");
    const toggle = document.getElementById("id_other_herbal");
    const table = document.getElementById("herbal-table");

    if (!btn || !body || !total) return;

    // =========================
    // TOGGLE
    // =========================
    function toggleTable() {
        if (!toggle || !table) return;
        table.style.display = toggle.value === "1" ? "" : "none";

        // ✅ AUTO-ADD FIRST ROW
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

        let template = document.getElementById("herbal-empty-form")?.innerHTML;

        if (!template) return;

        template = template.replace(/__prefix__/g, count);

        const temp = document.createElement("tbody");
        temp.innerHTML = template;

        body.appendChild(temp.firstElementChild);

        total.value = count + 1;
    });

    // =========================
    // REMOVE
    // =========================
    body.addEventListener("click", function (e) {

        if (e.target.classList.contains("remove-herbal")) {

            const row = e.target.closest("tr");
            const del = row.querySelector("input[type='checkbox']");

            if (del) {
                del.checked = true;
                row.style.display = "none";
            } else {
                row.remove();
                total.value = body.querySelectorAll(".herbal-row").length;
            }
        }
    });

});