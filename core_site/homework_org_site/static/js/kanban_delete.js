document.addEventListener("DOMContentLoaded", () => {
  const deleteBtn = document.getElementById("delete-done-btn");
  const container = document.getElementById("kanban-container");
  if (!deleteBtn || !container) return;

  const csrfToken = container.dataset.csrfToken;

  deleteBtn.addEventListener("click", async () => {
    if (!confirm("Are you sure you want to delete all done homeworks?")) return;

    const response = await fetch("/delete_done/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
    });

    const data = await response.json();
    if (data.success) {
      alert(`Deleted ${data.deleted} done homework(s).`);
      window.location.reload();
    } else {
      alert("Something went wrong while deleting!");
    }
  });
});