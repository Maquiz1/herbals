document.addEventListener("DOMContentLoaded", function () {

    const otherMedical = document.getElementById("id_other_medical");
    const table = document.getElementById("other-medical-table");

    function toggleTable() {
        const val = otherMedical.options[otherMedical.selectedIndex].text.toLowerCase();
        table.style.display = (val === "yes") ? "" : "none";
    }

    otherMedical.addEventListener("change", toggleTable);
    toggleTable();

    // =========================
    // ADD ROW (FIXED)
    // =========================
    document.getElementById("add-row").addEventListener("click", function () {

        const totalForms = document.getElementById("id_othermedicals-TOTAL_FORMS");
        const formCount = parseInt(totalForms.value);

        const template = document.getElementById("empty-form-template").innerHTML;

        const newRow = template.replace(/__prefix__/g, formCount);

        document.getElementById("formset-body").insertAdjacentHTML("beforeend", newRow);

        totalForms.value = formCount + 1;
    });

});