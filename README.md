# Unblocked Games Resources Clone

This is a static website clone of the Unblocked Games Resources site. It is designed to be hosted on GitHub Pages.

## Project Structure

- `index.html`: The main landing page listing all games.
- `game.html`: The player page that loads a specific game.
- `content.json`: A JSON database containing the list of games, their titles, descriptions, images, and embed URLs.
- `style.css`: The styling for the website.
- `script.js`: The logic to fetch games from the JSON file and render them.

## How to Add Games

To add more games or update existing ones, you only need to edit the `content.json` file.

1.  Open `content.json`.
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

**Important:** The current `content.json` contains placeholder URLs (`https://example.com/...`) and placeholder images. You will need to find the actual embed URLs for the games you want to host. You can often find these by inspecting the source of other game sites or looking for "Embed" buttons on game distribution platforms.

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
