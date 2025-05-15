// Configuration de base API
const API_BASE_URL = 'http://localhost:5000/api';
const itemModal = new bootstrap.Modal(document.getElementById('itemModal'));
const alertModal = new bootstrap.Modal(document.getElementById('alertModal'));
const loadingElement = document.getElementById('loading');

// Fonction pour afficher le loader
function showLoading() {
    loadingElement.classList.remove('d-none');
}

// Fonction pour cacher le loader
function hideLoading() {
    loadingElement.classList.add('d-none');
}

// Fonction pour afficher des alertes
function showAlert(title, message, type = 'success') {
    const alertTitle = document.getElementById('alert-title');
    const alertMessage = document.getElementById('alert-message');
    const alertHeader = document.getElementById('alert-header');
    
    alertTitle.textContent = title;
    alertMessage.textContent = message;
    
    // Définir la couleur d'en-tête en fonction du type
    alertHeader.className = 'modal-header';
    if (type === 'success') {
        alertHeader.classList.add('bg-success', 'text-white');
    } else if (type === 'error') {
        alertHeader.classList.add('bg-danger', 'text-white');
    } else if (type === 'info') {
        alertHeader.classList.add('bg-info', 'text-white');
    }
    
    alertModal.show();
}

// Fonction pour charger tous les items du menu
async function loadMenuItems(limit = 5) {
    try {
        showLoading();
        const response = await axios.get(`${API_BASE_URL}/menu`);
        const allItems = response.data;

        const menuListElement = document.getElementById('menu-list');

        if (allItems.length === 0) {
            menuListElement.innerHTML = `
                <div class="alert alert-info">
                    <i class="fas fa-info-circle me-2"></i>
                    Aucun item trouvé dans le menu. Ajoutez de nouveaux items pour commencer.
                </div>
            `;
            return;
        }

        const menuItems = limit ? allItems.slice(0, limit) : allItems;
        let menuHTML = '';

        menuItems.forEach(item => {
            menuHTML += `
                <div class="card menu-item mb-3">
                    <div class="card-body d-flex justify-content-between align-items-center">
                        <div>
                            <h5 class="card-title">${item.name}</h5>
                            <p class="card-text text-muted mb-0">${item.price.toFixed(2)} DH</p>
                        </div>
                        <button class="btn btn-outline-primary btn-sm view-details" data-name="${item.name}" data-price="${item.price}">
                            <i class="fas fa-edit me-1"></i> Modifier
                        </button>
                    </div>
                </div>
            `;
        });

        // Add "Voir plus / Voir moins" button
        if (allItems.length > 5) {
            menuHTML += `
                <div class="text-center mt-3">
                    <button id="toggle-view" class="btn btn-outline-secondary">
                        ${limit ? 'Voir plus' : 'Voir moins'}
                    </button>
                </div>
            `;
        }

        menuListElement.innerHTML = menuHTML;

        // Button to toggle view
        const toggleBtn = document.getElementById('toggle-view');
        if (toggleBtn) {
            toggleBtn.addEventListener('click', () => {
                loadMenuItems(limit ? null : 5); // toggle between all and 5
            });
        }

        // Event listeners for "Modifier" buttons
        document.querySelectorAll('.view-details').forEach(button => {
            button.addEventListener('click', () => {
                const name = button.getAttribute('data-name');
                const price = button.getAttribute('data-price');
                showItemDetails(name, price);
            });
        });

    } catch (error) {
        console.error('Erreur lors du chargement des items du menu:', error);
        showAlert('Erreur', 'Impossible de charger les items du menu. Veuillez réessayer.', 'error');
    } finally {
        hideLoading();
    }
}


// Fonction pour afficher les détails d'un item
function showItemDetails(name, price) {
    document.getElementById('edit-name').value = name;
    document.getElementById('edit-price').value = price;
    document.getElementById('original-name').value = name;
    
    itemModal.show();
}

// Fonction pour ajouter un nouvel item
async function addMenuItem(name, price) {
    try {
        showLoading();
        await axios.post(`${API_BASE_URL}/item/`, [{
            name: name,
            price: parseFloat(price)
        }]);
        
        showAlert('Succès', `L'item "${name}" a été ajouté au menu.`);
        loadMenuItems(); // Recharger la liste des items
        
        // Réinitialiser le formulaire
        document.getElementById('add-item-form').reset();
        
    } catch (error) {
        console.error('Erreur lors de l\'ajout de l\'item:', error);
        showAlert('Erreur', 'Impossible d\'ajouter l\'item au menu. Veuillez réessayer.', 'error');
    } finally {
        hideLoading();
    }
}

async function updateMenuItem(originalName, newName, newPrice) {
    try {
        showLoading();
        // Note : nous envoyons le nom original dans l'URL et dans le corps de la requête
        // pour s'assurer que l'API le trouve correctement
        await axios.put(`${API_BASE_URL}/item/${originalName}`, [{
            name: originalName,  // Utiliser le nom original pour la recherche
            price: parseFloat(newPrice)
        }]);
        
        // Si l'API a traité avec succès, et que nous voulons aussi changer le nom
        // nous faisons une seconde requête pour mettre à jour le nom
        if (newName !== originalName) {
            await axios.put(`${API_BASE_URL}/item/${originalName}`, [{
                name: newName,
                price: parseFloat(newPrice)
            }]);
        }
        
        showAlert('Succès', `L'item a été mis à jour avec succès.`);
        loadMenuItems(); // Recharger la liste des items
        itemModal.hide(); // Fermer le modal
        
    } catch (error) {
        console.error('Erreur lors de la mise à jour de l\'item:', error);
        showAlert('Erreur', 'Impossible de mettre à jour l\'item. Veuillez réessayer.', 'error');
    } finally {
        hideLoading();
    }
}

// Fonction pour supprimer un item
async function deleteMenuItem(name) {
    try {
        showLoading();
        await axios.delete(`${API_BASE_URL}/item/${name}`);
        
        showAlert('Succès', `L'item "${name}" a été supprimé du menu.`);
        loadMenuItems(); // Recharger la liste des items
        itemModal.hide(); // Fermer le modal
        
    } catch (error) {
        console.error('Erreur lors de la suppression de l\'item:', error);
        showAlert('Erreur', 'Impossible de supprimer l\'item. Veuillez réessayer.', 'error');
    } finally {
        hideLoading();
    }
}

// Fonction pour rechercher un item par nom
async function searchMenuItem(name) {
    try {
        showLoading();
        const response = await axios.get(`${API_BASE_URL}/item/${name}`);
        const item = response.data;
        
        // Afficher les détails de l'item trouvé
        showItemDetails(item.name, item.price);
        
    } catch (error) {
        console.error('Erreur lors de la recherche de l\'item:', error);
        if (error.response && error.response.status === 404) {
            showAlert('Non trouvé', `Aucun item avec le nom "${name}" n'a été trouvé.`, 'info');
        } else {
            showAlert('Erreur', 'Une erreur s\'est produite lors de la recherche. Veuillez réessayer.', 'error');
        }
    } finally {
        hideLoading();
    }
}

// Gestionnaires d'événements
document.addEventListener('DOMContentLoaded', () => {
    // Charger les items du menu au chargement de la page
    loadMenuItems();
    
    // Gestionnaire pour le formulaire d'ajout d'item
    document.getElementById('add-item-form').addEventListener('submit', (e) => {
        e.preventDefault();
        const name = document.getElementById('item-name').value.trim();
        const price = document.getElementById('item-price').value;
        
        if (name && price) {
            addMenuItem(name, price);
        }
    });
    
    // Gestionnaire pour le formulaire de recherche
    document.getElementById('search-item-form').addEventListener('submit', (e) => {
        e.preventDefault();
        const name = document.getElementById('search-name').value.trim();
        
        if (name) {
            searchMenuItem(name);
        }
    });
    
    // Gestionnaire pour le bouton de mise à jour
    document.getElementById('update-item').addEventListener('click', () => {
        const originalName = document.getElementById('original-name').value;
        const newName = document.getElementById('edit-name').value.trim();
        const newPrice = document.getElementById('edit-price').value;
        
        if (newName && newPrice) {
            updateMenuItem(originalName, newName, newPrice);
        }
    });
    
    // Gestionnaire pour le bouton de suppression
    document.getElementById('delete-item').addEventListener('click', () => {
        const name = document.getElementById('original-name').value;
        
        if (confirm(`Êtes-vous sûr de vouloir supprimer "${name}" du menu?`)) {
            deleteMenuItem(name);
        }
    });
});