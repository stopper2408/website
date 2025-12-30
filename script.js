let allGames = [];

document.addEventListener('DOMContentLoaded', () => {
    // Check if we are on the index page or game page
    const gamesGrid = document.getElementById('games-grid');
    const searchInput = document.getElementById('search-input');

    if (gamesGrid) {
        fetchGames();
        
        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                filterGames(e.target.value);
            });
        }
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
        const card = document.createElement('a');
        card.href = `game.html?id=${game.id}`;
        card.className = 'game-card';
        
        card.innerHTML = `
            <img src="${game.image}" alt="${game.title}" loading="lazy">
            <div class="game-info">
                <h3>${game.title}</h3>
                <p>${game.description}</p>
                <div class="play-btn">Watch Now</div>
            </div>
        `;
        
        gamesGrid.appendChild(card);
    });
}

function filterGames(searchTerm) {
    const term = searchTerm.toLowerCase();
    const filtered = allGames.filter(game => 
        game.title.toLowerCase().includes(term) || 
        game.description.toLowerCase().includes(term)
    );
    renderGames(filtered);
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
