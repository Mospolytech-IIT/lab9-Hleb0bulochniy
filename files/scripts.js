document.addEventListener("DOMContentLoaded", function() {
    const fetchUsersBtn = document.getElementById("fetch-users");
    const createUserBtn = document.getElementById("create-user");
    const userForm = document.getElementById("user-form");
    const userTable = document.getElementById("user-table").getElementsByTagName("tbody")[0];
    const updateUserForm = document.getElementById("update-user-form");
    const updateUserBtn = document.getElementById("save-update-user");

    const fetchPostsBtn = document.getElementById("fetch-posts");
    const createPostBtn = document.getElementById("create-post");
    const postForm = document.getElementById("post-form");
    const postTable = document.getElementById("post-table").getElementsByTagName("tbody")[0];
    const userPostsView = document.getElementById("user-posts-view");
    const userPostsTable = document.getElementById("user-posts-table").getElementsByTagName("tbody")[0];

    const updatePostForm = document.getElementById("update-post-form");
    const saveUpdatePostBtn = document.getElementById("save-update-post");

    async function getAllUsers() {
        const response = await fetch("/users/");
        const data = await response.json();

        if (data.status === "success") {
            userTable.innerHTML = '';
            data.users.forEach(user => {
                const row = userTable.insertRow();
                row.insertCell(0).textContent = user.id;
                row.insertCell(1).textContent = user.username;
                row.insertCell(2).textContent = user.email;
                const actionsCell = row.insertCell(3);

                const viewPostsBtn = document.createElement("button");
                viewPostsBtn.textContent = "Показать посты";
                viewPostsBtn.onclick = () => viewUserPosts(user.id);
                actionsCell.appendChild(viewPostsBtn);

                const updateBtn = document.createElement("button");
                updateBtn.textContent = "Обновить";
                updateBtn.onclick = () => showUpdateUserForm(user);
                actionsCell.appendChild(updateBtn);

                const deleteBtn = document.createElement("button");
                deleteBtn.textContent = "Удалить";
                deleteBtn.onclick = () => deleteUser(user.id);
                actionsCell.appendChild(deleteBtn);
            });
        } else {
            alert(data.message);
        }
    }

    fetchUsersBtn.addEventListener("click", getAllUsers);

    createUserBtn.addEventListener("click", async () => {
        const user = {
            username: userForm.username.value,
            email: userForm.email.value,
            password: userForm.password.value
        };

        const response = await fetch("/users/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(user)
        });
        
        const data = await response.json();
        if (data.status === "success") {
            alert("Пользователь успешно создан");
            userForm.reset();
            getAllUsers();
        } else {
            alert(data.message);
        }
    });

    function showUpdateUserForm(user) {
        updateUserForm.style.display = "block";
        document.getElementById("update-user-id").value = user.id;
        document.getElementById("update-username").value = user.username;
        document.getElementById("update-email").value = user.email;
        document.getElementById("update-password").value = user.password;
    }

    updateUserBtn.addEventListener("click", async () => {
        const userId = document.getElementById("update-user-id").value;
        const updatedUser = {
            username: document.getElementById("update-username").value,
            email: document.getElementById("update-email").value,
            password: document.getElementById("update-password").value
        };

        const response = await fetch(`/users/${userId}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(updatedUser)
        });

        const data = await response.json();
        if (data.status === "success") {
            alert("Данные пользователя обновлены");
            getAllUsers();
            updateUserForm.style.display = "none";
        } else {
            alert(data.message);
        }
    });

    async function deleteUser(userId) {
        const response = await fetch(`/users/${userId}`, {
            method: "DELETE"
        });
        
        const data = await response.json();
        if (data.status === "success") {
            alert("Пользователь удалён");
            getAllUsers();
            fetchPostsBtn.click();
        } else {
            alert(data.message);
        }
    }

    fetchPostsBtn.addEventListener("click", async () => {
        const response = await fetch("/posts/");
        const data = await response.json();

        if (data.status === "success") {
            postTable.innerHTML = '';
            data.posts.forEach(post => {
                const row = postTable.insertRow();
                row.insertCell(0).textContent = post.id;
                row.insertCell(1).textContent = post.title;
                row.insertCell(2).textContent = post.content;
                row.insertCell(3).textContent = post.user_id;
                
                const actionsCell = row.insertCell(4);
                
                const updatePostBtn = document.createElement("button");
                updatePostBtn.textContent = "Обновить";
                updatePostBtn.onclick = () => showUpdatePostForm(post);
                actionsCell.appendChild(updatePostBtn);

                const deletePostBtn = document.createElement("button");
                deletePostBtn.textContent = "Удалить";
                deletePostBtn.onclick = () => deletePost(post.id);
                actionsCell.appendChild(deletePostBtn);
            });
        } else {
            alert(data.message);
        }
    });

    createPostBtn.addEventListener("click", async () => {
        const post = {
            title: postForm.title.value,
            content: postForm.content.value,
            user_id: postForm.user_id.value
        };

        const response = await fetch("/posts/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(post)
        });

        const data = await response.json();
        if (data.status === "success") {
            alert("Пост успешно создан");
            postForm.reset();
            fetchPostsBtn.click();
        } else {
            alert(data.message);
        }
    });

    async function viewUserPosts(userId) {
        const response = await fetch(`/posts/`);
        const data = await response.json();

        if (data.status === "success") {
            const userPosts = data.posts.filter(post => post.user_id === userId);
            userPostsTable.innerHTML = '';
            userPosts.forEach(post => {
                const row = userPostsTable.insertRow();
                row.insertCell(0).textContent = post.id;
                row.insertCell(1).textContent = post.title;
                row.insertCell(2).textContent = post.content;

                const actionsCell = row.insertCell(3);
                
                const updatePostBtn = document.createElement("button");
                updatePostBtn.textContent = "Обновить";
                updatePostBtn.onclick = () => showUpdatePostForm(post);
                actionsCell.appendChild(updatePostBtn);
                
                const deletePostBtn = document.createElement("button");
                deletePostBtn.textContent = "Удалить";
                deletePostBtn.onclick = () => deletePost(post.id);
                actionsCell.appendChild(deletePostBtn);
            });
            userPostsView.classList.remove("hidden");
        } else {
            alert(data.message);
        }
    }

    function showUpdatePostForm(post) {
        updatePostForm.style.display = "block";
        document.getElementById("update-post-id").value = post.id;
        document.getElementById("update-post-title").value = post.title;
        document.getElementById("update-post-content").value = post.content;
        document.getElementById("update-post-user-id").value = post.user_id;
    }

    saveUpdatePostBtn.addEventListener("click", async () => {
        const postId = document.getElementById("update-post-id").value;
        const updatedPost = {
            title: document.getElementById("update-post-title").value,
            content: document.getElementById("update-post-content").value,
            user_id: document.getElementById("update-post-user-id").value
        };

        const response = await fetch(`/posts/${postId}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(updatedPost)
        });

        const data = await response.json();
        if (data.status === "success") {
            alert("Пост обновлен");
            fetchPostsBtn.click();
            updatePostForm.style.display = "none";
        } else {
            alert(data.message);
        }
    });

    async function deletePost(postId) {
        const response = await fetch(`/posts/${postId}`, {
            method: "DELETE"
        });

        const data = await response.json();
        if (data.status === "success") {
            alert("Пост удалён");
            fetchPostsBtn.click();
        } else {
            alert(data.message);
        }
    }
});