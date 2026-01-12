# Unblocked Games Resources Clone

This is a static website clone of the Unblocked Games Resources site. It is designed to be hosted on GitHub Pages.

## Project Structure

- `index.html`: The main landing page listing all games.
- `game.html`: The player page that loads a specific game.
- `metadata.json`: A JSON database containing the list of games (source file).
- `data.js`: The encrypted game data loaded by the browser.
- `style.css`: The styling for the website.
- `script.js`: The logic to fetch games from the encrypted content and render them.

## How to Add Games

To add more games or update existing ones, you only need to edit the `metadata.json` file and run encryption.

1.  Open `metadata.json`.
2.  Add a new object to the array in the following format:

```json
{
  "id": "unique-game-id",
  "title": "Game Title",
  "image": "URL_TO_THUMBNAIL_IMAGE",
  "url": "URL_TO_GAME_EMBED_OR_IFRAME",
  "description": "Short description of the game."
}
```

3.  Run `python encrypt_content.py` to regenerate `data.js`.

**Important:** `metadata.json` is the source of truth, but `data.js` is what the website actually loads. Never deploy `metadata.json` to production if you want to avoid filters.

## How to Host on GitHub Pages

1.  Create a new repository on GitHub.
2.  Push all these files to the repository.
3.  Go to the repository **Settings**.
4.  Navigate to the **Pages** section (usually on the left sidebar).
5.  Under **Source**, select `Deploy from a branch`.
6.  Select your main branch (usually `main` or `master`) and the `/ (root)` folder.
7.  Click **Save**.
8.  GitHub will provide you with a URL where your site is live.

## Customization

-   **Styling:** Edit `style.css` to change colors, fonts, and layout.
-   **Content:** Edit `index.html` to change the header, footer, or intro text.
