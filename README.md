# Interim Intellectual Hub

A sophisticated Django-based blogging platform designed for intellectuals, writers, and poets to share their thoughts, ideas, and creative content.

![Interim Intellectual Hub](static/logo.png)

## Features

### 🎨 Modern UI with Dark Mode
- Lively, intellectual color scheme with elegant typography
- Robust dark mode support with persistent user preference
- No flash of unstyled content (FOUC) when switching themes
- Responsive design that works on all devices

### 📝 Rich Content Support
- Markdown support for blog post creation and display
- Proper handling of paragraphs and formatting (especially for poetry/stanzas)
- Custom categories including dedicated Poetry section
- Tag system for content organization and discovery

### 👤 User Authentication System
- Custom user registration and authentication
- User profiles with customizable information
- Public profiles for viewing author information
- Restricted features for registered users only (posting, commenting, liking)

### 🔔 Interactive Elements
- Modern notification system in bottom-right corner
- Auto-dismissing notifications with smooth animations
- Like functionality for posts
- Commenting system

### 👑 Admin Features
- Admin dashboard with user statistics
- Content management capabilities
- Full control over posts, comments, and user accounts

### Technology Stack

- **Backend**: Django 4.x (Python web framework)
- **Frontend**: HTML5, CSS3, JavaScript
- **CSS Framework**: Tailwind CSS
- **Icons**: Font Awesome
- **Fonts**: Google Fonts (Playfair Display, Source Sans Pro)
- **Database**: SQLite (default), compatible with PostgreSQL for production
- **Markdown**: Python-Markdown for rendering

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/interim-intellectual-hub.git
   cd interim-intellectual-hub
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

7. Access the site at `http://127.0.0.1:8000/`

## Usage

### Creating Content
1. Sign up for an account or log in
2. Click on "Create Post" in the navigation bar
3. Fill in the title, content (using Markdown), select a category, and add tags
4. Click "Publish" to make your post visible to others

### Interacting with Content
- Like posts by clicking the heart icon (requires login)
- Comment on posts using the comment form at the bottom of each post
- Browse posts by categories or tags using the sidebar

### Using Markdown

The blog supports Markdown formatting. Here's a quick reference:

- **Bold**: `**text**`
- **Italic**: `*text*`
- **Headings**: `# H1`, `## H2`, `### H3`
- **Links**: `[text](URL)`
- **Images**: `![alt text](image URL)`
- **Lists**:
  ```
  * Item 1
  * Item 2
  
  1. Item 1
  2. Item 2
  ```
- **Blockquotes**: `> quoted text`
- **Code**: `` `code` `` or ````code block````

### Managing Your Account
- Edit your profile by clicking your username and selecting "Settings"
- View your public profile to see how others view your information
- Log out through the user dropdown menu

### Admin Functions
- Access the admin dashboard through the user dropdown (staff users only)
- View statistics about registered users
- Manage content through the Django admin interface at `/admin/`

## Customization

### Theme
The site supports both light and dark modes:
- Light mode: Intellectual theme with gold accents
- Dark mode: Deep black background with adjusted color palette for optimal readability

Users' theme preferences are stored in localStorage and applied automatically on return visits.

You can modify the color scheme in the `base.html` template:

```css
:root {
    /* Light Mode Colors */
    --color-primary: rgb(54, 69, 73);
    --color-secondary: rgb(72, 95, 97);
    /* Additional variables... */
}

[data-theme="dark"] {
    /* Dark Mode Colors */
    --color-primary: rgb(130, 152, 179);
    --color-secondary: rgb(165, 180, 199);
    /* Additional variables... */
}
```

### Adding Categories
To add new categories to the blog posts:
1. Edit the `models.py` file in the core app
2. Add your new category to the `CATEGORY_CHOICES` tuple
3. Run migrations to apply the changes

## License

[MIT License](LICENSE)

## Credits

- Developed by Dalton Omondi
- Special thanks to the Django community
- Icons from [Font Awesome](https://fontawesome.com/)
- Fonts from [Google Fonts](https://fonts.google.com/)

---

© 2025 Interim Intellectual Hub
