const deleteDialog = document.getElementById("delete-dialog");
const deleteLinks = document.getElementsByClassName("delete-project");
console.log(deleteLinks);
deleteDialog.querySelector("button[type='reset']").addEventListener("click", (e) => {
    deleteDialog.close();
});

deleteDialog.addEventListener("submit", (event) => {
    console.log("submit");
    console.log(event);
    event.preventDefault();

    let endpoint = event.target.action;

    (async () => {
        deleteDialog.close();
        let response = await fetch(endpoint);
        if (response.ok) {
            location.reload();
        }
    });
});

function showDialog(projectName, action) {
    let form = deleteDialog.querySelector("form");
    form.action = action;

    let spanProjectName = deleteDialog.querySelector("span#delete-project-name");
    spanProjectName.innerHTML = projectName + "/";

    deleteDialog.showModal();
}

Array.from(deleteLinks).forEach((elmt) => {
    elmt.addEventListener("click", (event) => {
        event.preventDefault();
        event.stopPropagation();
        event.stopImmediatePropagation();

        let projectParent = event.target.closest("tr.project");
        showDialog(projectParent.id, event.target.href);
    });
});
