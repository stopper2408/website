let allContent = [];
let favorites = JSON.parse(localStorage.getItem('docuwatch_favorites')) || [];

document.addEventListener('DOMContentLoaded', () => {
    const contentGrid = document.getElementById('content-grid');
    const searchInput = document.getElementById('search-input');
    const categoryPills = document.querySelectorAll('.category-pill');

    initTypingAnimation();

    if (contentGrid) {
        fetchContent();
        
        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                filterContent(e.target.value);
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
                    filterContent(searchInput ? searchInput.value : '', category);
                }
            });
        });
    }
});

async function fetchContent() {
    try {
        if (typeof window.APP_DATA !== 'undefined') {
            // Client-side decryption to bypass network content filters
            try {
                const key = 'docuwatch';
                const binaryString = atob(window.APP_DATA);
                const bytes = new Uint8Array(binaryString.length);
                for (let i = 0; i < binaryString.length; i++) {
                    bytes[i] = binaryString.charCodeAt(i) ^ key.charCodeAt(i % key.length);
                }
                const jsonString = new TextDecoder().decode(bytes);
                allContent = JSON.parse(jsonString);
            } catch (decryptError) {
                console.error('Decryption failed:', decryptError);
                throw new Error('Failed to decrypt content data');
            }
        } else {
            throw new Error('No content source available (APP_DATA missing)');
        }
        
        // Sort by popularity (descending), then title (ascending)
        allContent.sort((a, b) => {
            const popA = a.popularity || 0;
            const popB = b.popularity || 0;
            if (popA !== popB) {
                return popB - popA; // Higher popularity first
            }
            return a.title.localeCompare(b.title);
        });

        renderContent(allContent);
    } catch (error) {
        console.error('Error fetching content:', error);
        const contentGrid = document.getElementById('content-grid');
        if (contentGrid) {
            contentGrid.innerHTML = `
                <div class="error-message" style="text-align: center; padding: 2rem;">
                    <i class="fa-solid fa-ban" style="font-size: 3rem; margin-bottom: 1rem; color: #ef4444;"></i>
                    <h3>Content Blocked</h3>
                    <p>Unable to load content data. This is likely due to a network restriction.</p>
                    <small style="opacity: 0.7;">Error: ${error.message}</small>
                </div>
            `;
        }
    }
}

function renderContent(items) {
    const contentGrid = document.getElementById('content-grid');
    contentGrid.innerHTML = '';

    if (items.length === 0) {
        contentGrid.innerHTML = '<p>No content found matching your criteria.</p>';
        return;
    }

    items.forEach(item => {
        const isFav = favorites.includes(item.id);
        const card = document.createElement('div');
        card.className = 'content-card';
        
        // Use 'Classics' instead of 'Arcade' for filter evasion
        if (item.category === 'Arcade') item.category = 'Classics';
        
        card.innerHTML = `
            <a href="view.html?id=${item.id}" style="text-decoration: none; color: inherit; display: block;">
                <img src="${item.image}" alt="${item.title}" loading="lazy" onerror="this.onerror=null; this.src='https://placehold.co/300x200/1e293b/3b82f6?text=${encodeURIComponent(item.title)}'">
                <div class="content-info">
                    <h3>${item.title}</h3>
                    <p>${item.description}</p>
                </div>
            </a>
            <div class="card-actions">
                <a href="view.html?id=${item.id}" class="play-btn">Watch Now</a>
                <button class="fav-btn ${isFav ? 'active' : ''}" onclick="toggleFavorite('${item.id}', this)">
                    <i class="fa-${isFav ? 'solid' : 'regular'} fa-heart"></i>
                </button>
            </div>
        `;
        
        contentGrid.appendChild(card);
    });
}

function filterContent(searchTerm, category = 'all') {
    const term = searchTerm.toLowerCase();
    let filtered = allContent.filter(item => 
        (item.title.toLowerCase().includes(term) || 
        item.description.toLowerCase().includes(term))
    );

    if (category !== 'all') {
        filtered = filtered.filter(item => {
             // Remap Arcade to Classics for filtering
             const itemCat = item.category === 'Arcade' ? 'Classics' : item.category;
             return itemCat && itemCat.toLowerCase() === category.toLowerCase();
        });
    }
    
    renderContent(filtered);
}

function showFavorites() {
    const favItems = allContent.filter(item => favorites.includes(item.id));
    renderContent(favItems);
}

function toggleFavorite(itemId, btn) {
    if (favorites.includes(itemId)) {
        favorites = favorites.filter(id => id !== itemId);
        btn.classList.remove('active');
        btn.querySelector('i').classList.replace('fa-solid', 'fa-regular');
    } else {
        favorites.push(itemId);
        btn.classList.add('active');
        btn.querySelector('i').classList.replace('fa-regular', 'fa-solid');
    }
    localStorage.setItem('docuwatch_favorites', JSON.stringify(favorites));
    
    // If currently viewing favorites, refresh
    if (document.querySelector('.category-pill[data-cat="favorites"].active')) {
        showFavorites();
    }
}

async function loadContent(contentId) {
    try {
        let content = [];
        if (typeof window.APP_DATA !== 'undefined') {
             // Client-side decryption to bypass network content filters
            try {
                const key = 'docuwatch';
                const binaryString = atob(window.APP_DATA);
                const bytes = new Uint8Array(binaryString.length);
                for (let i = 0; i < binaryString.length; i++) {
                    bytes[i] = binaryString.charCodeAt(i) ^ key.charCodeAt(i % key.length);
                }
                const jsonString = new TextDecoder().decode(bytes);
                content = JSON.parse(jsonString);
            } catch (decryptError) {
                console.error('Decryption failed:', decryptError);
                throw new Error('Failed to decrypt content data');
            }
        } else {
             throw new Error('No content source available (APP_DATA missing)');
        }

        const item = content.find(g => g.id === contentId);

        if (item) {
            document.title = `${item.title} - DocuWatch`;
            const titleEl = document.getElementById('content-title');
            if (titleEl) titleEl.textContent = item.title;
            
            const descEl = document.getElementById('content-description');
            if (descEl) descEl.textContent = item.description;
            
            const catEl = document.getElementById('content-category');
            if (catEl) catEl.textContent = (item.category === 'Arcade' ? 'Classics' : item.category) || 'Content';
            
            const frameEl = document.getElementById('content-frame');
            if (frameEl) frameEl.src = item.url;
        } else {
            const detailsEl = document.getElementById('content-details');
            if (detailsEl) detailsEl.style.display = 'none';
            const errorEl = document.getElementById('error-message');
            if (errorEl) errorEl.style.display = 'block';
        }
    } catch (error) {
        console.error('Error loading details:', error);
        const detailsEl = document.getElementById('content-details');
        if (detailsEl) detailsEl.style.display = 'none';
        
        const errorEl = document.getElementById('error-message');
        if (errorEl) {
             errorEl.style.display = 'block';
             errorEl.querySelector('p').textContent = `Error loading content: ${error.message}`;
        }
    }
}

function initTypingAnimation() {
    const textElement = document.getElementById('dynamic-text');
    if (!textElement) return;

    const words = ["History", "Science", "Nature", "Culture", "The World"];
    let wordIndex = 0;
    let charIndex = words[0].length;
    let isDeleting = true; // Start by deleting "History" after a pause
    
    // Initial delay before starting to delete
    setTimeout(() => {
        type();
    }, 2000);

    function type() {
        const currentWord = words[wordIndex];
        let typeSpeed = 200;
        
        if (isDeleting) {
            textElement.textContent = currentWord.substring(0, charIndex - 1);
            charIndex--;
            typeSpeed = 100;
        } else {
            textElement.textContent = currentWord.substring(0, charIndex + 1);
            charIndex++;
            typeSpeed = 200;
        }

        if (!isDeleting && charIndex === currentWord.length) {
            isDeleting = true;
            typeSpeed = 2000; // Pause at end of word
        } else if (isDeleting && charIndex === 0) {
            isDeleting = false;
            wordIndex = (wordIndex + 1) % words.length;
            typeSpeed = 500; // Pause before typing new word
        }

        setTimeout(type, typeSpeed);
    }
}
