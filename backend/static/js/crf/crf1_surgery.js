document.addEventListener("DOMContentLoaded", function () {

    const btn = document.getElementById("add-surgery");
    const body = document.getElementById("surgery-body");
    const total = document.getElementById("id_surgeries-TOTAL_FORMS");
    const toggle = document.getElementById("id_surgery_performed");
    const table = document.getElementById("surgery-table");

    if (!btn || !body || !total) return;

    function toggleTable() {
        const isYes = toggle?.value === "1";

        table.style.display = isYes ? "" : "none";

        if (isYes && body.children.length === 0) {
            btn.click();
        }

        btn.disabled = !isYes;
    }

    toggle?.addEventListener("change", toggleTable);
    toggleTable();

    btn.addEventListener("click", function () {

        let count = parseInt(total.value);

        let template = document.getElementById("surgery-empty")?.innerHTML;

        if (!template) return;

        template = template.replace(/__prefix__/g, count);

        const temp = document.createElement("tbody");
        temp.innerHTML = template;

        body.appendChild(temp.firstElementChild);

        total.value = count + 1;
    });

    body.addEventListener("click", function (e) {

        if (e.target.classList.contains("remove-surgery")) {

            const row = e.target.closest("tr");
            const del = row.querySelector("input[type='checkbox']");

            if (del) {
                del.checked = true;
                row.style.display = "none";
            } else {
                row.remove();
                total.value = body.querySelectorAll(".surgery-row").length;
            }
        }
    });

});