// function hasRealDataRows() {
//     return Array.from(tbody.querySelectorAll(".radio-row")).some(row => {

//         // ignore hidden (deleted) rows
//         if (row.style.display === "none") return false;

//         const inputs = row.querySelectorAll("input, select, textarea");

//         return Array.from(inputs).some(input => {
//             return (
//                 input.type !== "checkbox" &&
//                 input.value &&
//                 input.value.trim() !== ""
//             );
//         });
//     });
// }