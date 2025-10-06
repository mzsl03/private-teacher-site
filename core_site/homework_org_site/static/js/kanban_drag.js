document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById('kanban-container');
    const updateUrl = container.dataset.updateUrl;
    const csrfToken = container.dataset.csrfToken;

    const cards = document.querySelectorAll('.card');
    const columns = document.querySelectorAll('.column');

    cards.forEach(card => {
        card.addEventListener('dragstart', e => {
            e.dataTransfer.setData('id', card.dataset.id);
            card.style.opacity = '0.5';
        });
        card.addEventListener('dragend', e => {
            card.style.opacity = '1';
        });
    });

    columns.forEach(col => {
        col.addEventListener('dragover', e => {
            e.preventDefault();
            col.style.backgroundColor = '#eef6ff';
        });
        col.addEventListener('dragleave', e => {
            col.style.backgroundColor = '';
        });
        col.addEventListener('drop', async e => {
            e.preventDefault();
            col.style.backgroundColor = '';
            const id = e.dataTransfer.getData('id');
            const newStatus = col.dataset.status;
            const card = document.querySelector(`[data-id="${id}"]`);
            if (!card || !newStatus) return;
            const emptyMsg = col.querySelector('p');
            if (emptyMsg) emptyMsg.remove();
            const oldCol = card.parentElement;
            col.appendChild(card);
            const oldColumnCards = oldCol.querySelectorAll('.card');
            if (oldColumnCards.length === 0) {
                const msg = document.createElement('p');
                msg.textContent = oldCol.dataset.status === 'TODO'
                    ? 'Nothing to do...'
                    : oldCol.dataset.status === 'IN_PROGRESS'
                        ? 'No homework in progress...'
                        : 'No homework done...';
                oldCol.appendChild(msg);
            }
            await fetch(updateUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken,
                },
                body: JSON.stringify({id, status: newStatus})
            });
        });
    });
});
