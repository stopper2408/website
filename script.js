let allGames = [];
let favorites = JSON.parse(localStorage.getItem('docuwatch_favorites')) || [];

document.addEventListener('DOMContentLoaded', () => {
    const gamesGrid = document.getElementById('games-grid');
    const searchInput = document.getElementById('search-input');
    const categoryPills = document.querySelectorAll('.category-pill');

    if (gamesGrid) {
        fetchGames();
        
        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                filterGames(e.target.value);
            });
        }

        categoryPills.forEach(pill => {
            pill.addEventListener('click', () => {
                // Remove active class from all
                categoryPills.forEach(p => p.classList.remove('active'));
                // Add active to clicked
                pill.classList.add('active');
                
                const category = pill.dataset.cat;
                if (category === 'favorites') {
                    showFavorites();
                } else {
                    filterGames(searchInput ? searchInput.value : '', category);
                }
            });
        });
    }
});

async function fetchGames() {
    try {
        const response = await fetch('games.json');
        allGames = await response.json();
        renderGames(allGames);
    } catch (error) {
        console.error('Error fetching content:', error);
        const gamesGrid = document.getElementById('games-grid');
        if (gamesGrid) {
            gamesGrid.innerHTML = '<p>Error loading archives. Please try again later.</p>';
        }
    }
}

function renderGames(games) {
    const gamesGrid = document.getElementById('games-grid');
    gamesGrid.innerHTML = '';

    if (games.length === 0) {
        gamesGrid.innerHTML = '<p>No content found matching your criteria.</p>';
        return;
    }

    games.forEach(game => {
        const isFav = favorites.includes(game.id);
        const card = document.createElement('div');
        card.className = 'game-card';
        
        card.innerHTML = `
            <a href="game.html?id=${game.id}" style="text-decoration: none; color: inherit; display: block;">
                <img src="${game.image}" alt="${game.title}" loading="lazy">
                <div class="game-info">
                    <h3>${game.title}</h3>
                    <p>${game.description}</p>
                </div>
            </a>
            <div class="card-actions">
                <a href="game.html?id=${game.id}" class="play-btn">Watch Now</a>
                <button class="fav-btn ${isFav ? 'active' : ''}" onclick="toggleFavorite('${game.id}', this)">
                    <i class="fa-${isFav ? 'solid' : 'regular'} fa-heart"></i>
                </button>
            </div>
        `;
        
        gamesGrid.appendChild(card);
    });
}

function filterGames(searchTerm, category = 'all') {
    const term = searchTerm.toLowerCase();
    let filtered = allGames.filter(game => 
        game.title.toLowerCase().includes(term) || 
        game.description.toLowerCase().includes(term)
    );

    // Note: Real category filtering would require categories in JSON. 
    // For now, we just show all unless it's favorites.
    
    renderGames(filtered);
}

function showFavorites() {
    const favGames = allGames.filter(game => favorites.includes(game.id));
    renderGames(favGames);
}

function toggleFavorite(gameId, btn) {
    if (favorites.includes(gameId)) {
        favorites = favorites.filter(id => id !== gameId);
        btn.classList.remove('active');
        btn.querySelector('i').classList.replace('fa-solid', 'fa-regular');
    } else {
        favorites.push(gameId);
        btn.classList.add('active');
        btn.querySelector('i').classList.replace('fa-regular', 'fa-solid');
    }
    localStorage.setItem('docuwatch_favorites', JSON.stringify(favorites));
    
    // If currently viewing favorites, refresh
    if (document.querySelector('.category-pill[data-cat="favorites"].active')) {
        showFavorites();
    }
}

async function loadGame(gameId) {
    try {
        const response = await fetch('games.json');
        const games = await response.json();
        const game = games.find(g => g.id === gameId);

        if (game) {
            document.title = `${game.title} - DocuWatch`;
            document.getElementById('game-title').textContent = game.title;
            document.getElementById('game-description').textContent = game.description;
            document.getElementById('game-frame').src = game.url;
        } else {
            document.getElementById('game-details').style.display = 'none';
            document.getElementById('error-message').style.display = 'block';
        }
    } catch (error) {
        console.error('Error loading details:', error);
    }
}
