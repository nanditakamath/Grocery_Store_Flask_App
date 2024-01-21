document.addEventListener('DOMContentLoaded', function () {
    const categoryButtons = document.querySelectorAll('.item-btn');
    const addItemModal = document.getElementById('addItem');

    categoryButtons.forEach(button => {
        button.addEventListener('click', function () {
            const categoryId = button.getAttribute('data-category-id');
            const form = addItemModal.querySelector('form');
            const categoryIdInput = form.querySelector('#category_id');
            categoryIdInput.value = categoryId;

        });
    });
});


const editCategoryModal = document.getElementById('editCategoryModal');
const deleteCategoryModal = document.getElementById('deleteCategoryModal');

const editButtonList = document.querySelectorAll('.category-edit-btn');
editButtonList.forEach(editButton => {
    editButton.addEventListener('click', function (event) {
        event.stopPropagation();
        const categoryId = editButton.getAttribute('data-category-id');
        const categoryName = editButton.getAttribute('data-category-name');
        const editCategoryModal = document.getElementById('editCategoryModal');
        const categoryIdInput = editCategoryModal.querySelector('#editCategoryId');
        const categoryNameInput = editCategoryModal.querySelector('#editCategoryName');
        categoryIdInput.value = categoryId;
        categoryNameInput.value = categoryName;
        const modal = new bootstrap.Modal(editCategoryModal);
        modal.show();
    });
});


// Handle delete confirmation
const deleteButtons = document.querySelectorAll('.category-delete-btn');
deleteButtons.forEach(button => {
    button.addEventListener('click', function () {
        const categoryId = button.getAttribute('data-category-id');
        const modal = new bootstrap.Modal(deleteCategoryModal);
        const confirmDeleteButton = document.getElementById('confirmDeleteCategory');
        confirmDeleteButton.setAttribute('data-category-id', categoryId); // Set category ID
        modal.show();
    });
});

// Handle actual delete action
const confirmDeleteButton = document.getElementById('confirmDeleteCategory');
confirmDeleteButton.addEventListener('click', function () {
    const categoryId = confirmDeleteButton.getAttribute('data-category-id');
    deleteCategory(categoryId);
    console.log(categoryId)
});

function deleteCategory(categoryId) {
    const url = `/delete_category/${categoryId}`;
    fetch(url, {
        method: 'DELETE',
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.reload();
            } else {
                console.error('Failed to delete category');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function editCategory(categoryId, newCategoryName) {
    const url = '/edit_category';
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        },
        body: JSON.stringify({
            categoryId: categoryId,
            newCategoryName: newCategoryName,
        }),
    })
        .then(() => {
            console.log('Category edited successfully');
            const categoryHeader = document.querySelector(`[data-category-id="${categoryId}"] .card-header h4`);
            if (categoryHeader) {
                categoryHeader.textContent = newCategoryName;
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

const editItemModal = document.getElementById('editItemModal');
const editItemButtonList = document.querySelectorAll('.edit-item-btn');

editItemButtonList.forEach(editButton => {
    editButton.addEventListener('click', function (event) {
        event.stopPropagation();
        const itemId = editButton.getAttribute('data-item-id');
        const itemName = editButton.getAttribute('data-item-name');
        const itemUnit = editButton.getAttribute('data-item-unit');
        const itemQuantity = editButton.getAttribute('data-item-quantity');
        const itemRate = editButton.getAttribute('data-item-rate');
        const editItemModal = document.getElementById('editItemModal');
        const itemIdInput = editItemModal.querySelector('#editItemId');
        const itemNameInput = editItemModal.querySelector('#editItemName');
        const itemUnitInput = editItemModal.querySelector('#editItemUnit');
        const itemQuantityInput = editItemModal.querySelector('#editItemQuantity');
        const itemRateInput = editItemModal.querySelector('#editItemRate');
        itemIdInput.value = itemId;
        itemNameInput.value = itemName;
        itemUnitInput.value = itemUnit;
        itemQuantityInput.value = itemQuantity;
        itemRateInput.value = itemRate;
        const modal = new bootstrap.Modal(editItemModal);
        modal.show();
    });
});

const saveItemButton = document.querySelector('#saveItemButton');

saveItemButton.addEventListener('click', function () {
    const editItemForm = document.getElementById('editItemForm');
    const formData = new FormData(editItemForm);

    fetch('/edit_item', {
        method: 'POST',
        body: formData,
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const editItemModal = new bootstrap.Modal(document.getElementById('editItemModal'));
                editItemModal.hide();

                window.location.reload();
            } else {
                console.error('Failed to edit item');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
});

const deleteItemModal = document.getElementById('deleteItemModal');
// Handle delete confirmation
const deleteItemButtons = document.querySelectorAll('.item-delete-btn');
deleteItemButtons.forEach(button => {
    button.addEventListener('click', function () {
        const itemId = button.getAttribute('data-item-id');
        const modal = new bootstrap.Modal(deleteItemModal);
        const confirmItemDeleteButton = document.getElementById('confirmDeleteItem');
        confirmItemDeleteButton.setAttribute('data-item-id', itemId); // Set category ID
        modal.show();
    });
});

// Handle actual delete action
const confirmItemDeleteButton = document.getElementById('confirmDeleteItem');
confirmItemDeleteButton.addEventListener('click', function () {
    const itemId = confirmItemDeleteButton.getAttribute('data-item-id');
    deleteItem(itemId);
    console.log(itemId)
});

function deleteItem(itemId) {
    const url = `/delete_item/${itemId}`;
    fetch(url, {
        method: 'DELETE',
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.reload();
            } else {
                console.error('Failed to delete item');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}



