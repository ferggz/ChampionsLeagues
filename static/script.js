    const searchInput = document.getElementById("searchInput");
    const noResults = document.getElementById("noResults");
    const table = document.querySelector("table");
    const compactButton = document.getElementById("compactButton");
    const headers = document.querySelectorAll("th[data-column]");

    let sortDirection = {};

    function normalize(text) {
        return text
            .toLowerCase()
            .normalize("NFD")
            .replace(/[\u0300-\u036f]/g, "")
            .replace(/\s+/g, "");
    }

    function getRows() {
        return Array.from(document.querySelectorAll(".team-row"));
    }

    function filterRows() {
        const rows = getRows();
        const searchText = normalize(searchInput.value);
        let visibleCount = 0;

        rows.forEach(function (row) {
            const teamName = normalize(
                row.querySelector(".team-link span").textContent
            );

            if (teamName.includes(searchText)) {
                row.style.display = "";
                visibleCount++;
            } else {
                row.style.display = "none";
            }
        });

        noResults.style.display = visibleCount === 0 ? "block" : "none";
    }

    function getCellValue(row, column) {
        const columnIndex = {
            position: 0,
            pj: 2,
            pg: 3,
            pe: 4,
            pp: 5,
            gf: 6,
            ga: 7,
            dg: 8
        };

        return parseInt(row.cells[columnIndex[column]].textContent);
    }

    compactButton.addEventListener("click", function () {
        table.classList.toggle("compact");

        if (table.classList.contains("compact")) {
            compactButton.textContent = "Expandir tabla";
        } else {
            compactButton.textContent = "Compactar tabla";
        }
    });

    headers.forEach(function (header) {
        header.addEventListener("click", function () {
            const column = header.dataset.column;
            const rows = getRows();

            sortDirection[column] = !sortDirection[column];

            rows.sort(function (a, b) {
                const aValue = getCellValue(a, column);
                const bValue = getCellValue(b, column);

                if (sortDirection[column]) {
                    return aValue - bValue;
                } else {
                    return bValue - aValue;
                }
            });

            rows.forEach(function (row) {
                table.appendChild(row);
            });

            filterRows();
        });
    });

    searchInput.addEventListener("input", filterRows);