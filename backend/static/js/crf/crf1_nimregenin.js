document.addEventListener("DOMContentLoaded", function () {

    const nimBtn = document.getElementById("add-nim");
    const nimBody = document.getElementById("nimregenin-body");
    const nimTotal = document.getElementById("id_nimregenins-TOTAL_FORMS");
    const nimToggle = document.getElementById("id_nimregenin_herbal");
    const nimTable = document.getElementById("nimregenin-table");

    // =========================
    // SAFETY CHECK (🔥 IMPORTANT)
    // =========================
    if (!nimBtn || !nimBody || !nimTotal) {
        console.warn("Nimregenin formset not initialized");
        return;
    }

    // =========================
    // TOGGLE TABLE
    // =========================
    function toggleNimTable() {
        if (!nimToggle || !nimTable) return;

        nimTable.style.display = nimToggle.value === "1" ? "" : "none";
    }

    nimToggle?.addEventListener("change", toggleNimTable);
    toggleNimTable();

    // =========================
    // ADD ROW
    // =========================
    nimBtn.addEventListener("click", function () {

        let count = parseInt(nimTotal.value);

        let template = document.getElementById("nim-empty-form")?.innerHTML;

        if (!template) {
            console.error("Nim template not found");
            return;
        }

        template = template.replace(/__prefix__/g, count);

        const temp = document.createElement("tbody");
        temp.innerHTML = template;

        nimBody.appendChild(temp.firstElementChild);

        nimTotal.value = count + 1;
    });

    // =========================
    // REMOVE ROW
    // =========================
    nimBody.addEventListener("click", function (e) {

        if (e.target.classList.contains("remove-nim")) {

            const row = e.target.closest("tr");
            const deleteInput = row.querySelector("input[type='checkbox']");

            if (deleteInput) {
                deleteInput.checked = true;
                row.style.display = "none";
            } else {
                row.remove();
                nimTotal.value = nimBody.querySelectorAll(".nim-row").length;
            }
        }
    });

});