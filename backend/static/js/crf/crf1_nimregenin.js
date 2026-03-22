document.addEventListener("DOMContentLoaded", function () {

    const NimregeninHerbal = document.getElementById("id_nimregenin_herbal");
    const tableCard = document.getElementById("nimregenin-table");
    const addBtn = document.getElementById("add-nim");
    const tbody = document.getElementById("nimregenin-body");
    const totalForms = document.getElementById("id_nimregenins-TOTAL_FORMS");

    function toggleTable() {
        const valText = NimregeninHerbal.options[NimregeninHerbal.selectedIndex].text.toLowerCase();

        const hasRows = tbody.querySelectorAll(".nimr-row:not([style*='display: none'])").length > 0;

        if (valText === "yes" || hasRows) {
            tableCard.style.display = "";
        } else {
            tableCard.style.display = "none";
        }

        // ✅ HERE
        addBtn.disabled = valText !== "yes";
    }

    NimregeninHerbal.addEventListener("change", toggleTable);
    toggleTable();

    addBtn.addEventListener("click", function () {
        let count = parseInt(totalForms.value);
        let template = document.getElementById("nim-empty-form").innerHTML.replace(/__prefix__/g, count);

        const temp = document.createElement("tbody");
        temp.innerHTML = template;

        tbody.appendChild(temp.firstElementChild);
        totalForms.value = count + 1;

        toggleTable();
    });

    tbody.addEventListener("click", function (e) {
        if (e.target.classList.contains("remove-nim")) {
            const row = e.target.closest("tr");
            const del = row.querySelector("input[type='checkbox']");

            if (del) {
                del.checked = true;
                row.style.display = "none";
            } else {
                row.remove();
                totalForms.value = tbody.querySelectorAll(".nim-row").length;
            }

            toggleTable();
        }
    });

});