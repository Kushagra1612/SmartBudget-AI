export function formatRupees(value) {

    const number = Number(value);

    const formatted = Math.abs(number).toLocaleString("en-IN", {
        maximumFractionDigits: 0,
    });

    return number < 0 ? `-₹${formatted}` : `₹${formatted}`;

}