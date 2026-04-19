  const searchBox = document.getElementById("search");
const resultsBox = document.getElementById("searchResults");
const tiles = document.querySelectorAll(".tile");
const btn = document.getElementById("searchBtn");

function doSearch() {
    let value = searchBox.value.toLowerCase();
    resultsBox.innerHTML = "";

    if (value === "") {
        resultsBox.style.display = "none";
        return;
    }

    resultsBox.style.display = "block";

    let found = false;

    tiles.forEach(tile => {
        let name = tile.getAttribute("data-name") || tile.innerText.toLowerCase();

        if (name.toLowerCase().includes(value)) {
            resultsBox.appendChild(tile.cloneNode(true));
            found = true;
        }
    });

    if (!found) {
        resultsBox.innerHTML = "<div style='padding:12px;color:#aaa'>No results found</div>";
    }
}

searchBox.addEventListener("input", doSearch);
btn.addEventListener("click", doSearch);
