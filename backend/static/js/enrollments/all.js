$(document).ready(function () {

    function togglePreviousDate() {
        const val = $("#id_pt_type").val();

        if (val === "follow_up") {
            $("#previous-date-wrapper").show();
        } else {
            $("#previous-date-wrapper").hide();
            $("#id_previous_date").val("");
        }
    }

    $("#id_pt_type").on("change", togglePreviousDate);

    togglePreviousDate();
});