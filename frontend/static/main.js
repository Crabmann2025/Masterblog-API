async function loadPosts() {
    const baseUrl = document.getElementById("api-base-url").value;
    const response = await fetch(`${baseUrl}/posts`);
    const posts = await response.json();
    const container = document.getElementById("post-container");
    container.innerHTML = '';

    posts.forEach(post => {
        const div = document.createElement('div');
        div.className = 'post';
        div.innerHTML = `
            <h2>${post.title}</h2>
            <p>${post.content}</p>
            <button onclick="deletePost(${post.id})">Delete</button>
            <button onclick="editPost(${post.id})">Edit</button>
        `;
        container.appendChild(div);
    });
}

async function addPost() {
    const baseUrl = document.getElementById("api-base-url").value;
    const title = document.getElementById("post-title").value;
    const content = document.getElementById("post-content").value;

    if (!title || !content) {
        alert("Title and content cannot be empty!");
        return;
    }

    await fetch(`${baseUrl}/posts`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({title, content})
    });

    document.getElementById("post-title").value = '';
    document.getElementById("post-content").value = '';
    loadPosts();
}

async function deletePost(id) {
    const baseUrl = document.getElementById("api-base-url").value;
    await fetch(`${baseUrl}/posts/${id}`, { method: 'DELETE' });
    loadPosts();
}

async function editPost(id) {
    const baseUrl = document.getElementById("api-base-url").value;
    const newTitle = prompt("Enter new title:");
    const newContent = prompt("Enter new content:");

    if (!newTitle || !newContent) {
        alert("Title and content cannot be empty!");
        return;
    }

    await fetch(`${baseUrl}/posts/${id}`, {
        method: 'PUT',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({title: newTitle, content: newContent})
    });

    loadPosts();
}
