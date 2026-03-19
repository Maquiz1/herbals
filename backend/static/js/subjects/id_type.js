document.addEventListener("DOMContentLoaded", function () {
    // Result fields
    const IdType = document.getElementById("id_id_type");

    // Field to show/hide
    const otherIdTypeWrapper = document.getElementById("other-id-wrapper");

    function toggleIdType() {

        const value = String(IdType?.value || "");

        if (value === "96") {
            otherIdTypeWrapper.style.display = "block";
        } else {
            otherIdTypeWrapper.style.display = "none";
        }
    }

    // Initial state on page load
    toggleIdType();

    // Update when either result changes
    IdType.addEventListener("change", toggleIdType);
});
